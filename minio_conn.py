from minio import Minio
from config import access_key,secret_key
from typing import Any


class MinioConnector:
    minio_client = Minio(
        endpoint="localhost:9000",
        access_key=access_key,
        secret_key=secret_key,
        secure=False)

class Bucket:

    @staticmethod
    def create(bucket_name) -> None:
        MinioConnector.minio_client.make_bucket(bucket_name)
        print(f"Bucket {bucket_name} created")

    @staticmethod
    def list_buckets():
        return [bucket.name for bucket in MinioConnector.minio_client.list_buckets()]


    @staticmethod
    def remove(bucket_name: str) -> None:
        MinioConnector.minio_client.remove_bucket(bucket_name)
        print(f"Bucket {bucket_name} removed")



class Object:

    @staticmethod
    def upload(bucket_name: str,
               object_name: str,
               data: Any) -> None:
        MinioConnector.minio_client.put_object(bucket_name, object_name, data, length=-1, part_size=5*1024*1024)

    @staticmethod
    def download(bucket_name: str,
                        file_path: str,
                        object_name: str) -> None:
        MinioConnector.minio_client.fget_object(bucket_name, file_path, object_name)
        print(f"File '{object_name}' downloaded")

    @staticmethod
    def remove(bucket_name: str, object_name: str) -> None:
        MinioConnector.minio_client.remove_object(bucket_name, object_name)
        print(f"Object '{object_name}' deleted")
