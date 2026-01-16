from minio import Minio
from minio.error import S3Error
from config import access_key,secret_key


minio_client = Minio(
    endpoint="localhost:9000",
    access_key=access_key,
    secret_key=secret_key,
    secure=False  
)


def create_bucket(bucket_name) -> None:
    minio_client.make_bucket(bucket_name)
    print(f"Bucket {bucket_name} created")

def list_buckets():
    try:
        buckets = minio_client.list_buckets()
        for bucket in buckets:
            print(bucket.name, bucket.creation_date)
    except S3Error as err:
        print(err)

def upload_object(bucket_name: str,
                  file_path: str,
                  object_name: str) -> None:
    minio_client.fput_object(bucket_name, object_name, file_path)
    print(f"File '{file_path}' uploaded")

def download_object(bucket_name: str,
                  file_path: str,
                  object_name: str) -> None:
    minio_client.fget_object(bucket_name, file_path, object_name)
    print(f"File '{object_name}' downloaded")

def remove_object(bucket_name: str, object_name: str) -> None:
    minio_client.remove_object(bucket_name, object_name)
    print(f"Object '{object_name}' deleted")

def remove_bucket(bucket_name: str) -> None:
    minio_client.remove_bucket(bucket_name)
    print(f"Bucket {bucket_name} removed")

