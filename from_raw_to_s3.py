from minio_conn import Bucket, Object
import io
import json


def from_source_to_s3(source, date,  **kwargs):
    if source.bucket_name in Bucket.list_buckets():
        data = io.BytesIO(json.dumps(source.get_vacancies(**kwargs), ensure_ascii=False).encode('utf-8'))
        Object.upload(source.bucket_name, f'{date.replace(microsecond=0).isoformat()}.json', data)
    else:
        Bucket.create(source.bucket_name)
        data = io.BytesIO(json.dumps(source.get_vacancies(**kwargs), ensure_ascii=False).encode('utf-8'))
        Object.upload(source.bucket_name, f'{date.replace(microsecond=0).isoformat()}.json', data)
        
