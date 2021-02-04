from storages.backends.s3boto3 import S3Boto3Storage
import os

class PublicMediaStorage(S3Boto3Storage):
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    location = 'media'
    # default_acl = 'public-read'
    file_overwrite = False

class StaticStorage(S3Boto3Storage):
    bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
    location = 'static'
    # default_acl = 'public-read'