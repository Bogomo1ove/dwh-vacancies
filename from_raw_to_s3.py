from parsers.headhunter import HeadHunter
from minio_conn import Bucket, Object
import io
import json
from datetime import datetime


def from_source_to_s3(source, date, **kwargs):
    if source.bucket_name not in Bucket.list_buckets():
        Bucket.create(source.bucket_name)
    data = io.BytesIO(
        json.dumps(source.get_vacancies(**kwargs), ensure_ascii=False).encode("utf-8")
    )
    Object.upload(
        source.bucket_name, f"{date.replace(microsecond=0).isoformat()}.json", data
    )


hh = HeadHunter()

from_source_to_s3(hh, datetime.today(), date_to=datetime.now())
