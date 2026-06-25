import boto3
from app.core.config.config import settings


s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.REGION
)

class S3_service:

    @staticmethod
    def upload_file(file_name: str, file_path: str, file_type: str):
        response = s3_client.upload_file(f"{file_path}", settings.BUCKET_NAME, key:=f"{file_type}/{file_name}")
        return key
    

    @staticmethod
    def generate_presigned_url(key: str):
        response = s3_client.generate_presined_url('get_object',
                                            Params={
                                                'Bucket':"cohort-storage",
                                                'Key': key 
                                            },
                                            ExpiresIn=settings.AWS_PRESIGNED_URL_EXP
                                            )
        return response