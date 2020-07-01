import datetime
import logging
import os
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.storage.queue import QueueServiceClient, QueueClient, QueueMessage, TextBase64EncodePolicy

def main(req: func.HttpRequest) -> func.HttpResponse:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    connect_str = os.getenv('source_files_connection')
    target_connect_str = os.getenv('target_files_connection')

    queue_client = QueueClient.from_connection_string(conn_str=target_connect_str, queue_name='scalequeue2', message_encode_policy=TextBase64EncodePolicy())
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client('fake-date-files')

    blob_list = container_client.list_blobs()
    count = 0
    for blob in blob_list:
        logging.info(blob.name)
        queue_client.send_message(content=blob.name)
        count += 1