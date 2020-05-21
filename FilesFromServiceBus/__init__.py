import logging
import os
from io import BytesIO
import azure.functions as func
from azure.storage.blob import BlobServiceClient, BlobClient

def main(msg: func.ServiceBusMessage):
    blob_name = msg.get_body().decode('utf-8')
    logging.info('%s trigger processed', blob_name)

    connect_str = os.getenv('source_files_connection')
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)

    connect_target_str = os.getenv('target_files_connection')
    blob_target_service_client = BlobServiceClient.from_connection_string(connect_target_str)

    blob_client = blob_service_client.get_blob_client(container='fake-date-files', blob=blob_name)
    blob_target_client = blob_target_service_client.get_blob_client(container='fake-date-files', blob=blob_name.replace('.fake','.copy.fake'))

    #local_path = "./data"
    #download_file_path = os.path.join(local_path, blob_name)
    #with open(download_file_path, "wb") as download_file:
    #    download_file.write(blob_client.download_blob().readall())
    #    logging.info('%s downloaded', blob_name)
    
    with BytesIO() as input_blob:
        blob_client.download_blob().download_to_stream(input_blob)
        input_blob.seek(0)
        logging.info('%s trigger downloaded from source', blob_name)
        blob_target_client.upload_blob(input_blob)
        logging.info('%s trigger uploaded to target', blob_name)

        





