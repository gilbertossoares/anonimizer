from azure.storage.blob import BlobServiceClient

class AzureBlobService:
    def __init__(self, connection_string):
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    def upload_file(self, container_name, file_name, file_path):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=file_name)
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        print(f"Arquivo {file_name} carregado para o container {container_name}.")

    def download_file(self, container_name, blob_name, download_path):
        blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        with open(download_path, "wb") as data:
            data.write(blob_client.download_blob().readall())
        print(f"Arquivo {blob_name} baixado do container {container_name}.")
