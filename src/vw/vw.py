import os
import io
import sys
import time
import random
import csv
import datetime

from argparse import ArgumentParser
from argparse import BooleanOptionalAction

from google.cloud import 

def get_project_number():
    projects_client = resourcemanager.ProjectsClient()
    current_project = projects_client.get_project() 
    return current_project.number

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

if __name__ == "__main__":
    parser = ArgumentParser(description="Vision Warehouse Asset Ingest")
    parser.add_argument("--corpus", type=str, help="The name of the Corpus to create", default=os.getenv("VW_CORPUS_NAME", "my_vw_corpus_name"))
    parser.add_argument("--corpus-desc", type=str, help="A description of this Corpus", default=os.getenv("VW_CORPUS_DESC", "This is my VW Corpus"))
    parser.add_argument("--index", type=str, help="The name of the Index to create", default=os.getenv("VW_INDEX_NAME", "my_vw_index"))
    parser.add_argument("--index-endpoint", type=str, help="The name of the Index Endpoint to create", default=os.getenv("VW_INDEX_ENDPOINT_NAME", "my_vw_endpoint"))
    parser.add_argument("--clean-corpus", help="Clean up Corpus", action=BooleanOptionalAction)
    parser.add_argument("--clean-assets", help="Clean up Assets", action=BooleanOptionalAction)
    parser.add_argument("--clean-index", help="Clean up Index", action=BooleanOptionalAction)

    main(parser.parse_args())

