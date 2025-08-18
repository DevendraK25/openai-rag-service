# sources/azure_blob.py
from azure.storage.blob import BlobServiceClient
from sources.base import BaseSource
import os

class AzureBlobSource(BaseSource):
    def __init__(self, connection_string=None, container=None, prefix=""):
        connection_string = connection_string or os.getenv("AZURE_BLOB_CONNECTION_STRING")
        self.blob_service = BlobServiceClient.from_connection_string(connection_string)
        self.container = container
        self.prefix = prefix

    def list_files(self):
        container_client = self.blob_service.get_container_client(self.container)
        return [blob.name for blob in container_client.list_blobs(name_starts_with=self.prefix)]

    def read_file(self, blob_name):
        container_client = self.blob_service.get_container_client(self.container)
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall().decode("utf-8")
