import boto3
from botocore.exceptions import ClientError


def send_email(*args, **kwargs):
    client = boto3.client('ses', region_name=kwargs.get('region', 'eu-west-1'))

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    kwargs['recipient'],
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': 'UTF-8',
                        'Data': kwargs.get('body_html', '')
                    },
                    'Text': {
                        'Charset': 'UTF-8',
                        'Data': kwargs.get('body_text', '')
                    },
                },
                'Subject': {
                    'Charset': 'UTF-8',
                    'Data': kwargs.get('subject', ''),
                },
            },
            Source=kwargs['sender']
        )
    except ClientError as e:
        return {
            'error': e.response['Error']['Message']
        }
    else:
        return {
            'message_id': response['MessageId']
        }


def get_email(email_type='reset_password', name=None):
    email_map = {
        'reset_password': {
            'subject': f"Password reset email{' for name' if name else ''}",
            'html': f"""
                <p>Dear {name if name else 'User'},</p>
                <p>
                You have request a password reset for your account.
                If it was requested by you click here: <a href="https://hyperbudget.net/TO-DO">Reset password</a>.
                Else, please ignore the email.
                </p>""", # noqa E501
            'text': f"""
                Dear {name if name else 'User'},

                You have requested a password reset for your account.
                If it was requested by yourself, please copy and paste this link: https://hyperbudget.net/TO-DO
                Else, please ignore this email.
                """ # noqa E501
        }
    }

    return email_map[email_type]
