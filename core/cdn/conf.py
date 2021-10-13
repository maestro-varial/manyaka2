import os

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = "manyaka"
AWS_S3_ENDPOINT_URL = "https://nyc3.digitaloceanspaces.com/"
AWS_LOCATION = "https://manyaka.nyc3.digitaloceanspaces.com/"
AWS_S3_OBJECT_PARACMETERS = {
    'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'core.cdn.backends.MediaRootS3Boto3Storage'
STATICFILES_STORAGE = 'core.cdn.backends.StaticRootS3Boto3Storage'