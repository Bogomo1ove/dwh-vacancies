from parser_hh import get_vacancies_hh
from parser_geekjob import get_vacancies_geekjob, URL
from minio_conn import upload_object
from datetime import datetime


def from_raw_hh_to_s3():
    hh_bucket_name = 'headhuntervacancies'
    hh_file_name = get_vacancies_hh(datetime.now().isoformat())
    hh_file_path = hh_file_name
    upload_object(hh_bucket_name,
                  hh_file_path,
                  hh_file_name)

def from_raw_gj_to_s3():
    gj_bucket_name = 'geekjobvacancies'
    get_vacancies_geekjob(URL)
    gj_file_name = f"{datetime.now().replace(microsecond=0).isoformat()}.json"
    gj_file_path = gj_file_name
    upload_object(gj_bucket_name,
                  gj_file_path,
                  gj_file_name)
