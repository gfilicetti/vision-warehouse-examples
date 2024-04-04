import os
import io
import sys
import time
import random
import csv
import datetime

from argparse import ArgumentParser
from argparse import BooleanOptionalAction

from google.cloud import resourcemanager_v3 as resourcemanager

def get_project_number():
    rm = resourcemanager.ProjectsClient()
    project = rm.get_project(name="projects/vision-warehouse-pilot")

    # name comes back as "projects/5519466666", we only want to return the number
    return project.name.split('/')[1]

def main(args):
    yay = "Yes!"
    print(f"You made it inside. {yay}")

    PROJECT_NUMBER_STR = get_project_number()
    PROJECT_NUMBER = int(PROJECT_NUMBER_STR[0])

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

    

if __name__ == "__main__":
    parser = ArgumentParser(description="Vision Warehouse Asset Ingest")
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

