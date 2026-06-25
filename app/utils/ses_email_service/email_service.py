import boto3
from app.core.config.config import settings

ses_client = boto3.client(
    'ses',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.REGION
)

class EmailService:

    @staticmethod
    def send_email(receiever_mail: str, subject: str, body: str):
        ses_client.send_email(
            Source=f'Team Cohort <{settings.SES_SENDER_MAIL}>',
            Destination={'ToAddresses': [receiever_mail]},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Text': {'Data': body}
                    }
                }
            )