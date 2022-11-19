import json
import logging
import mimetypes
import sys

import boto3
import requests

from helpers.utils import get_s3_link

logger = logging.getLogger()
logger.setLevel("INFO")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def add_offchain_data(token_id: int,  name: str):
    s3 = boto3.client('s3')

    try:
        image_response = requests.get("https://source.unsplash.com/random/500x500", stream=True).raw
        content_type = image_response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)

        s3.upload_fileobj(image_response, "ticketrust-develop", 'assets/' + str(token_id) + extension)

        file_s3_url = get_s3_link(bucket_name="ticketrust-develop", key=f'assets/{str(token_id)}{extension}')

        json_data = {
            "name": name,
            "image": file_s3_url,
        }

        s3.put_object(Body=json.dumps(json_data), Bucket="ticketrust-develop", Key=f"metadata/{str(token_id)}.json")

        metadata_url = get_s3_link(bucket_name="ticketrust_develop", key=f'metadata/{str(token_id)}.json')

        logger.info("Done :)")

        return metadata_url

    except FileNotFoundError:
        print("The file was not found")
        return False
    except Exception as e:
        logger.info(e)
