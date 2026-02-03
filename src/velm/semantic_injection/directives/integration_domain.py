from textwrap import dedent
from typing import Dict, Any

from ..contract import BaseDirectiveDomain
from ..loader import domain


@domain("integration")
class IntegrationDomain(BaseDirectiveDomain):
    """
    The Bridge to External Services (Payments, Storage, Comms).
    """

    @property
    def namespace(self) -> str:
        return "integration"

    def help(self) -> str:
        return "Generates SaaS boilerplate (Stripe, S3, SendGrid)."

    def _directive_stripe_webhook(self, context: Dict[str, Any], secret_env: str = "STRIPE_WEBHOOK_SECRET",
                                  lang: str = "python", *args, **kwargs) -> str:
        """
        @integration/stripe_webhook(secret_env="STRIPE_KEY")
        Generates a secure webhook handler with signature verification.
        """
        if lang == "python":
            return dedent(f"""
                import stripe
                from fastapi import APIRouter, Request, HTTPException, Header
                import os

                router = APIRouter()

                # Gnostic Requirement: pip install stripe
                stripe.api_key = os.getenv("STRIPE_API_KEY")
                endpoint_secret = os.getenv("{secret_env}")

                @router.post("/webhook")
                async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
                    payload = await request.body()

                    try:
                        event = stripe.Webhook.construct_event(
                            payload, stripe_signature, endpoint_secret
                        )
                    except ValueError as e:
                        raise HTTPException(status_code=400, detail="Invalid payload")
                    except stripe.error.SignatureVerificationError as e:
                        raise HTTPException(status_code=400, detail="Invalid signature")

                    # Handle the event
                    if event['type'] == 'payment_intent.succeeded':
                        payment_intent = event['data']['object']
                        print(f"Payment for {{payment_intent['amount']}} succeeded.")

                    return {{"status": "success"}}
            """).strip()
        return "# Language not supported for Stripe yet."

    def _directive_s3(self, context: Dict[str, Any], bucket_env: str = "AWS_BUCKET_NAME", *args, **kwargs) -> str:
        """
        @integration/s3
        Generates a robust S3 client wrapper (boto3).
        """
        return dedent(f"""
            import boto3
            from botocore.exceptions import ClientError
            import os
            import logging

            class StorageService:
                def __init__(self):
                    self.s3 = boto3.client(
                        's3',
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                        region_name=os.getenv('AWS_REGION', 'us-east-1')
                    )
                    self.bucket = os.getenv("{bucket_env}")

                def upload_file(self, file_obj, object_name=None):
                    \"\"\"Upload a file-like object to S3.\"\"\"
                    try:
                        self.s3.upload_fileobj(file_obj, self.bucket, object_name)
                        return f"https://{{self.bucket}}.s3.amazonaws.com/{{object_name}}"
                    except ClientError as e:
                        logging.error(e)
                        return None

                def generate_presigned_url(self, object_name, expiration=3600):
                    \"\"\"Generate a presigned URL to share a private file.\"\"\"
                    try:
                        response = self.s3.generate_presigned_url('get_object',
                                                                    Params={{'Bucket': self.bucket, 'Key': object_name}},
                                                                    ExpiresIn=expiration)
                        return response
                    except ClientError as e:
                        logging.error(e)
                        return None
        """).strip()

    def _directive_smtp(self, context: Dict[str, Any], *args, **kwargs) -> str:
        """
        @integration/smtp
        Generates a standard SMTP email sender.
        """
        return dedent("""
            import smtplib
            import ssl
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            import os

            def send_email(receiver_email, subject, html_content):
                sender_email = os.getenv("SMTP_EMAIL")
                password = os.getenv("SMTP_PASSWORD")
                smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
                port = int(os.getenv("SMTP_PORT", 465))

                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = sender_email
                message["To"] = receiver_email
                message.attach(MIMEText(html_content, "html"))

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
        """).strip()