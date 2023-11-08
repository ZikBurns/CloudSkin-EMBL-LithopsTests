import uuid

import boto3
import json
import time
from flask import Flask, request
app = Flask(__name__)

region_name = 'us-east-1'
aws_access_key_id='ASIA4ZTYB6XMPTWJHOVF'
aws_secret_access_key='WCWVdwBKVMb80FB3Hy5DV0gz0FtvooWfH7HW55eR'
aws_session_token='IQoJb3JpZ2luX2VjEMn//////////wEaCXVzLWVhc3QtMSJHMEUCIQCznuC44JLi65Prj/pFVPmfJRyRmjDxHXhqoo3i4mvPTgIgB2V/dnM3ijhkaFCjsHuzEjH3+02bUCsikSQeevCBYPAq9AIIQhAAGgw4Nzk2NDYzNDA1NjgiDCtphEM36lDHwsb9tirRAsvAI7WB/RxVkhYeu73ba6xal+uzD05BxVPifHsYZ2NwUsHADDhAM8WfzOF9AUVCyLHE9NTC7xidHVx/N84SN3zaRJLIiUxuGAi5oX8gx/Y80CPy6PN+OtAwG5R/TiRhVBBUtYCTNTB5U97qqJzhHpFfTf8qXyjZAwPnTjY+9aKsbByTZW1tn1IOvgjwpeNIpw5qtPBoiepYc3p9AoCz/U1gew2IW9QyuS5ZOdPASxSP1iZGp5Y5hF5WjIhmx8f9wOizrLnZvGhvysyyIsVIzfh3ZQAgrBLk6yWRISesyZBjRjeTsvDYxb5ncdoWxBNjlmezXVVQ3ZgqthNL1EfHVQiOg6XWUwrUgseYKSwWom3nAS/56l9hNcGVgKqgqCw3V8oP8bSGLuBrfffS8pIdruLe2CCWXSiiTDl1FDbSZWvYf97QxMM+OCwRP7HAP+ABW08w1/WZpQY6pwGBDsQnGvqz/FEv+10C7s+aBPiz4otxMnlIZ2b1UQEMmjIBM/lIuG5w0oKREPnZgkAxN6z5dFLLNbHfqQkKVHYJqNMp1mt4dJ6IUr13QtEK87A+rDXFPo0///pQPkkdAPnN2+tQspex1NZ9z6BnxR6gQ3METqrk3TtmiEjN+mwr3Vt1MA5TveOhVp8jVcmBMAYUW0Whagl2qTSCF9tBKR72v+5aGT37hw=='
aws_session = boto3.Session(region_name=region_name,
                            aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key,
                            aws_session_token=aws_session_token)
# Create an SQS client
sqs_client = aws_session.client('sqs')

# Create an SNS client
sns_client = aws_session.client('sns')

# Define the SQS queue URL
queue_url = 'https://sqs.us-east-1.amazonaws.com/879646340568/TestingSQSLambdaSNS.fifo'

# Define the SNS topic ARN
topic_arn = 'arn:aws:sns:us-east-1:879646340568:TestingSQSLambda'


# Function to send a message to the SQS queue
def send_message_to_sqs_queue(user_id, message):
    # Prepare the message payload with user information
    payload = {
        'user_id': user_id,
        'message': message,
        'region_name': region_name,
        'aws_access_key_id':aws_access_key_id,
        'aws_secret_access_key':aws_secret_access_key,
        'aws_session_token':aws_session_token,
        'queue_url': queue_url,
        'topic_arn':topic_arn
    }
    message_deduplication_id = str(uuid.uuid4())
    # Send the message to the SQS queue
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(payload),
        MessageGroupId=message_deduplication_id,
        MessageDeduplicationId= message_deduplication_id
    )

    # Return the response containing the message ID
    return response['MessageId']


# Function to subscribe the user to the SNS topic
def subscribe_user_to_sns_topic(user_id):
    # Subscribe the user to the SNS topic
    response = sns_client.subscribe(
        TopicArn=topic_arn,
        Protocol='application',  # Adjust the protocol based on your notification needs
        Endpoint=user_id  # Provide the user identifier or contact details as the endpoint
    )

    # Return the subscription ARN
    return response['SubscriptionArn']


# Function to wait for the SNS notification
# Route to handle incoming SNS notifications in the Flask server
@app.route('/sns-notification', methods=['POST'])
def handle_sns_notification():
    notification = request.get_json()
    # Process the SNS notification
    # You can access the notification content from the 'notification' object
    print(f"Received SNS notification: {notification}")
    # Return a response if needed
    return 'OK'

# Example usage
def main():
    # User ID and message information
    user_id = 'USER_ID'
    message = 'Hello, this is my message!'

    # Send the message to the SQS queue
    message_id = send_message_to_sqs_queue(user_id, message)
    print(f"Message sent to SQS with ID: {message_id}")

    # List all the platform applications
    response = sns_client.list_platform_applications()

    # Iterate over the applications and print their ARNs
    for app in response['PlatformApplications']:
        platform_application_arn = app['PlatformApplicationArn']
        print(f"Platform Application ARN: {platform_application_arn}")

    # # Subscribe the user to the SNS topic
    # subscription_arn = subscribe_user_to_sns_topic(user_id)
    # print(f"User subscribed to SNS topic with ARN: {subscription_arn}")

    # # Wait for the SNS notification
    # result = wait_for_sns_notification(subscription_arn)
    # print(f"Received SNS notification: {result}")
    app.run()

# Run the example
if __name__ == '__main__':
    main()