from core.env import config



# aws default access
AWS_DEFAULT_ACL = "public-read"


# aws bucket name and aws endpoint url
# the url from linode object storage is "micro-ecommerce.ap-south-1.linodeobjects.com"
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME", default=None)
AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL", default=None)


AWS_S3_USE_SSL = True
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID", default=None)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", default=None)
AWS_S3_SIGNATURE_VERSION = config("AWS_S3_SIGNATURE_VERSION", default=None)


# file upload storage default
# we set its value to the class "MediaStorage" in the backends.py in the storage folder in the core folder
DEFAULT_FILE_STORAGE = "core.storages.backends.MediaStorage"


# staticfiles
# we set its value to the class "StaticFileStorage" in the backends.py in the storage folder in the core folder
STATICFILES_STORAGE = "core.storages.backends.StaticFilesStorage"