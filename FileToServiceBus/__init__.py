import datetime
import logging
import os
import azure.functions as func
from azure.servicebus import QueueClient, Message
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    # if mytimer.past_due:
    #    logging.info('The timer is past due!')
    queue_name = os.getenv('service_bus_queue_name')
    queue_client = QueueClient.from_connection_string(os.getenv('service_bus_connection'), queue_name)

    connect_str = os.getenv('source_files_connection')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client('fake-date-files')

    blob_list = container_client.list_blobs()
    count = 0
    for blob in blob_list:
        # print("\t" + blob.name)
        # print(count)
        msg = Message('{0}'.format(blob.name))
        logging.info(msg='({0}) {1} added to queue {2}'.format(count, blob.name, queue_name))
        queue_client.send(msg)
        count += 1
