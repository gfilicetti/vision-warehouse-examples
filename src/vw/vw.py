import os
import logging
import concurrent.futures

from argparse import ArgumentParser
from argparse import BooleanOptionalAction

from google.cloud import resourcemanager_v3 as resourcemanager

from visionai.python.gapic.visionai import visionai_v1
from visionai.python.net import channel
from visionai.python.warehouse.transformer import asset_indexing_transformer as ait
from visionai.python.warehouse.transformer import (ocr_transformer, speech_transformer, transformer_factory)
from visionai.python.warehouse.utils import (vod_asset, vod_corpus, vod_index_endpoint)

def get_project_number(name: str) -> str:
    rm = resourcemanager.ProjectsClient()
    project = rm.get_project(name=f"projects/{name}")

    # name comes back as "projects/5519466666", we only want to return the number
    return project.name.split('/')[1]

def main(args):

    ##########
    # Define CONSTANTS
    PROJECT_NUMBER_STR = get_project_number(args.project)
    
    # This was the original line, not sure why they took only the first number of the project number
    # PROJECT_NUMBER = int(PROJECT_NUMBER_STR[0])
    PROJECT_NUMBER = int(PROJECT_NUMBER_STR)

    # Only us-central1 is supported.
    # Please note that this region is for VisionAi services.
    REGION = "us-central1"

    CORPUS_DISPLAY_NAME = args.corpus
    CORPUS_DESCRIPTION = args.corpus_desc

    # External users can only access PROD environment.
    ENV = "PROD"

    INDEX_DISPLAY_NAME = args.index
    INDEX_ENDPOINT_DISPLAY_NAME = args.index_endpoint

    CLEAN_UP_ASSETS = args.clean_assets
    CLEAN_UP_INDEX = args.clean_index
    CLEAN_UP_CORPUS = args.clean_corpus

    # Because it takes ~1h to create and deploy index. A existing index can be specified to save time.

    # If CORPUS_ID is specified, skip creating a new corpus.
    CORPUS_ID = args.corpus_id
    # If DEPLOYED_INDEX_ID is specified, use existing index instead of creating and deploying a new index.
    DEPLOYED_INDEX_ID = args.index_id 

    

    ##########
    # Setup the array of files to ingest
    GCS_FILES = [
        "gs://cloud-samples-data/video/animals.mp4",
        "gs://cloud-samples-data/video/googlework_short.mp4",
        "gs://cloud-samples-data/video/chicago.mp4",
        (
            "gs://cloud-samples-data/video/Machine Learning Solving Problems"
            " Big, Small, and Prickly.mp4"
        ),
        "gs://cloud-samples-data/video/JaneGoodall.mp4",
        "gs://cloud-samples-data/video/gbikes_dinosaur.mp4",
        "gs://cloud-samples-data/video/pizza.mp4",
    ]

    

    ##########
    # Set up logging
    _logger = logging.getLogger(__name__)
    _logger.setLevel(logging.DEBUG)

    # Create a console handler
    handler = logging.StreamHandler()

    # Set the log format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    # Add the handler to the logger
    _logger.addHandler(handler)
    


    ##########
    # Create a warehouse client
    warehouse_endpoint = channel.get_warehouse_service_endpoint(channel.Environment[ENV])
    warehouse_client = visionai_v1.WarehouseClient(
        client_options={"api_endpoint": warehouse_endpoint}
    )

    

    ##########
    # Create or reuse a Corpus
    if CORPUS_ID is None:
        corpus_name = vod_corpus.create_corpus(
            warehouse_client,
            PROJECT_NUMBER,
            REGION,
            CORPUS_DISPLAY_NAME,
            CORPUS_DESCRIPTION,
        ).name
    else:
        corpus_name = visionai_v1.WarehouseClient.corpus_path(
            PROJECT_NUMBER_STR, REGION, CORPUS_ID
        )

    

    ##########
    # Create an executor to upload and transform assets in parallel.
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=8)

    

    ##########
    # Create and ingest assets
    new_asset_futures = []
    for gcs_file in GCS_FILES:
        new_asset_futures.append(
            executor.submit(
                vod_asset.create_and_upload_asset,
                warehouse_client,
                gcs_file,
                corpus_name,
            )
        )
    done_or_error, _ = concurrent.futures.wait(
        new_asset_futures, return_when="ALL_COMPLETED"
    )
    asset_names = []
    for done_future in done_or_error:
        try:
            asset_names.append(done_future.result())
            _logger.info("Create and upload asset succeeded %s", done_future.result())
        except Exception as e:
            _logger.exception(e)

    

    ##########
    # *** INDEX CREATION CAN TAKE A LONG TIME ***
    # Create index and index endpoint for the corpus, or use existing index
    # and index endpoint if specified.
    if DEPLOYED_INDEX_ID is None:
        # Creates index for the corpus.
        index_name = vod_corpus.index_corpus(
            warehouse_client, corpus_name, INDEX_DISPLAY_NAME
        )
        # Creates index endpoint and deploys the created index above to the index
        # endpoint.
        index_endpoint_name = vod_index_endpoint.create_index_endpoint(
            warehouse_client,
            PROJECT_NUMBER,
            REGION,
            INDEX_ENDPOINT_DISPLAY_NAME,
        ).name
        deploy_operation = warehouse_client.deploy_index(
            visionai_v1.DeployIndexRequest(
                index_endpoint=index_endpoint_name,
                deployed_index=visionai_v1.DeployedIndex(
                    index=index_name,
                ),
            )
        )
        _logger.info("Wait for index to be deployed %s.", deploy_operation.operation.name)
        # Wait for the deploy index operation. Depends on the data size to be
        # indexed, the timeout may need to be increased.
        deploy_operation.result(timeout=7200)
        _logger.info("Index is deployed.")
    else:
        index_name = "{}/indexes/{}".format(corpus_name, DEPLOYED_INDEX_ID)
        index = warehouse_client.get_index(visionai_v1.GetIndexRequest(name=index_name))
        _logger.info("Use existing index %s.", index)
        if index.state != visionai_v1.Index.State.CREATED:
            _logger.critical("Invalid index. The index state must be Created.")
        if not index.deployed_indexes:
            _logger.critical("Invalid index. The index must be deployed.")
        index_endpoint_name = index.deployed_indexes[0].index_endpoint
    
    

    ##########
    # Run Transforms
    ocr_config = ocr_transformer.OcrTransformerInitConfig(
        corpus_name=corpus_name,
        env=channel.Environment[ENV],
    )

    ml_config = transformer_factory.MlTransformersCreationConfig(
        run_embedding=True,
        speech_transformer_init_config=speech_transformer.SpeechTransformerInitConfig(
            corpus_name=corpus_name, language_code="en-US"
        ),
        ocr_transformer_init_config=ocr_config,
    )
    ml_transformers = transformer_factory.create_ml_transformers(
        warehouse_client, ml_config
    )
    # Creates indexing transformer to index assets.
    asset_indexing_transformer = ait.AssetIndexingTransformer(warehouse_client, index_name)
    # Runs the transformers for the assets.
    futures = []

    for asset_name in asset_names:
        futures.append(
            executor.submit(
                vod_asset.transform_single_asset,
                asset_name,
                ml_transformers,
                asset_indexing_transformer,
            )
        )
    done_or_error, _ = concurrent.futures.wait(futures, return_when="ALL_COMPLETED")
    for future in done_or_error:
        try:
            future.result()
        except Exception as e:
            _logger.exception(e)

    # GF: this is the original line and 3.12 complains about the + operator. 
    # GF: I'm going to try and just make a list of them
    # all_transformers = ml_transformers + [asset_indexing_transformer]
    all_transformers = [ml_transformers, asset_indexing_transformer]
    for transformer in all_transformers:
        transformer.teardown()

    

    ##########
    # Execute a search for: "dinosaur"
    search_response = warehouse_client.search_index_endpoint(
        visionai_v1.SearchIndexEndpointRequest(
            index_endpoint=index_endpoint_name,
            text_query="dinosaur",
            page_size=10,
        )
    )
    _logger.info("Search response: %s", search_response)

    

    ##########
    # Execute a search with Criteria for "river"
    cr = visionai_v1.Criteria(
        field="speech", text_array=visionai_v1.StringArray(txt_values=["kid"])
    )
    search_response = warehouse_client.search_index_endpoint(
        visionai_v1.SearchIndexEndpointRequest(
            index_endpoint=index_endpoint_name,
            text_query="river",
            criteria=[cr],
            page_size=100,
        )
    )
    _logger.info("Search response: %s", search_response)

    

    ##########
    # Execute another search with Criteria for "trees"
    cr = visionai_v1.Criteria(
        field="text", text_array=visionai_v1.StringArray(txt_values=["National Park"])
    )
    search_response = warehouse_client.search_index_endpoint(
        visionai_v1.SearchIndexEndpointRequest(
            index_endpoint=index_endpoint_name,
            text_query="trees",
            criteria=[cr],
            page_size=100,
        )
    )
    _logger.info("Search response: %s", search_response)

    

    ##########
    # Perform clean up if requested
    if CLEAN_UP_ASSETS:
        for asset_name in asset_names:
            warehouse_client.delete_asset(visionai_v1.DeleteAssetRequest(name=asset_name))
            _logger.info("Deleted asset %s", asset_name)

    if CLEAN_UP_INDEX:
        undeploy_operation = warehouse_client.undeploy_index(
            visionai_v1.UndeployIndexRequest(index_endpoint=index_endpoint_name)
        )
        _logger.info(
            "Wait for index to be undeployed %s.",
            undeploy_operation.operation.name,
        )
        # Wait for the undeploy index operation.
        undeploy_operation.result(timeout=1800)
        _logger.info("Index is undeployed.")
        warehouse_client.delete_index(visionai_v1.DeleteIndexRequest(name=index_name))
        _logger.info("Deleted index %s", index_name)
        warehouse_client.delete_index_endpoint(
            visionai_v1.DeleteIndexEndpointRequest(name=index_endpoint_name)
        )
        _logger.info("Deleted index endpoint %s", index_endpoint_name)

    if CLEAN_UP_CORPUS:
        warehouse_client.delete_corpus(visionai_v1.DeleteCorpusRequest(name=corpus_name))
        _logger.info("Deleted corpus %s", corpus_name)


if __name__ == "__main__":
    parser = ArgumentParser(description="Vision Warehouse Asset Ingest")
    parser.add_argument("--project", type=str, help="The Google Cloud project to use", default=os.getenv("GOOGLE_CLOUD_PROJECT", "vision-warehouse-pilot"))
    parser.add_argument("--corpus", type=str, help="The name of the Corpus to create", default=os.getenv("VW_CORPUS_NAME", "my_vw_corpus_name"))
    parser.add_argument("--corpus-desc", type=str, help="A description of this Corpus", default=os.getenv("VW_CORPUS_DESC", "This is my VW Corpus"))
    parser.add_argument("--index", type=str, help="The name of the Index to create", default=os.getenv("VW_INDEX_NAME", "my_vw_index"))
    parser.add_argument("--index-endpoint", type=str, help="The name of the Index Endpoint to create", default=os.getenv("VW_INDEX_ENDPOINT_NAME", "my_vw_endpoint"))
    parser.add_argument("--corpus-id", type=str, help="The id of an existing Corpus, if given we skip creation", default=None)
    parser.add_argument("--index-id", type=str, help="The id of an existing Index, if given we skip creation", default=None)
    parser.add_argument("--clean-corpus", help="Clean up Corpus", action=BooleanOptionalAction)
    parser.add_argument("--clean-assets", help="Clean up Assets", action=BooleanOptionalAction)
    parser.add_argument("--clean-index", help="Clean up Index", action=BooleanOptionalAction)

    main(parser.parse_args())

