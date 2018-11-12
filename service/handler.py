import json


def send_email(event, context):
    if 'Records' not in event:
        return {"statusCode": 400}

    for record in event['Records']:
        body = json.loads(record['body'])
        print(f"Record {body}")

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
