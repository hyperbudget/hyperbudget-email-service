import json
from service.email import send_email as deliver_email, get_email


def send_email(event, context):
    if 'Records' not in event:
        return {"statusCode": 400}

    for record in event['Records']:
        body = json.loads(record['body'])

        if 'email' not in body:
            print("ERROR: email not in body")
            return {"statusCode": 400}
        elif 'type' not in body:
            print("ERROR: type not in body")
            return {"statusCode": 400}
        else:
            email = get_email(
                email_type='reset_password',
                name=body.get('name')
            )
            result = deliver_email(
                {
                    'recipient': body['email'],
                    'body_html': email['html'],
                    'body_text': email['text'],
                    'subject': email['subject'],
                    'sender': 'info@hyperbudget.net'
                }
            )
            if result.get('error'):
                print(f"ERROR: {result['error']}")

    response = {
        "statusCode": 200,
        "body": "OK"
    }

    print(f"event called")
    print(event)

    return response


"""
{'Records': [{'messageId': '99aa6189-314b-4f47-b233-6a90a118c6ec',
'receiptHandle': '',
'body': '{\n"hello": "world"\n}', 'attributes': {'ApproximateReceiveCount':
'1', 'SentTimestamp': '1542058224358', 'SenderId': '504193536768',
'ApproximateFirstReceiveTimestamp': '1542058224364'}, 'messageAttributes':
{}, 'md5OfBody': '1f899303b925051f07ad75090dde35f9', 'eventSource':
'aws:sqs', 'eventSourceARN':
'...',
'awsRegion': 'eu-west-2'}]}
"""
