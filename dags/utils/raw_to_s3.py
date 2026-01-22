from .minio_conn import Bucket, Object
import io
import json
from datetime import timedelta


def source_to_s3(source, date):
    if source.bucket_name not in Bucket.list_buckets():
        Bucket.create(source.bucket_name)
    data = io.BytesIO(
        json.dumps(source.get_vacancies(date), ensure_ascii=False).encode("utf-8")
    )
    Object.upload(
        source.bucket_name, f"{date.strftime('%d.%m.%Y')}.json", data
    )
