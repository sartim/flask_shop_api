import os
import boto3

from app.core.app import app


def upload_file(file, bucket_name, acl="public-read"):
    """
    Uploads a file object to S3 bucket and returns the url for
    the path of the uploaded file
    """
    _s3 = boto3.client('s3')
    try:
        _s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )
    except Exception as e:
        app.logger.exception('Exception occurred. {}'.format(str(e)))
        return False
    else:
        return "{}{}".format(os.environ.get("S3_URL"), file.filename)


def delete_file(key):
    """
    Delete key from S3 bucket
    """
    s3 = boto3.resource('s3')
    try:
        r = s3.Object(os.environ.get('S3_BUCKET'), key).delete()
        if r['ResponseMetadata']['RetryAttempts'] > 0:
            return True
    except Exception as e:
        app.logger.exception('Exception occurred. {}'.format(str(e)))
    return False
