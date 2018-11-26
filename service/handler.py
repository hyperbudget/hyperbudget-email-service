import json
from service.emailer import send_email as deliver_email, get_email


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
        elif body['type'] == 'reset_password':
            email = get_email(
                email_type='reset_password',
                name=body.get('name'),
                token=body['token'],
                userId=body['userId']
            )
            result = deliver_email(
                recipient=body['email'],
                body_html=email['html'],
                body_text=email['text'],
                subject=email['subject'],
                sender='info@hyperbudget.net'
            )
            if result.get('error'):
                print(f"ERROR: {result['error']}")
        else:
            print("ERROR: unknown type")
            return {"statusCode": 400}

    response = {
        "statusCode": 200,
        "body": "OK"
    }

    print(f"event called")
    print(event)

    return response
