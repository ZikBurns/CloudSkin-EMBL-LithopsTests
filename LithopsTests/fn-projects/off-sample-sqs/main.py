import json
import uuid

from lithops.serve.serve import LithopsServe
import boto3
if __name__ == '__main__':
    with open('datasets/2016-09-21_16h06m49s__6.csv') as f:
        urls = f.read().splitlines()
    urls.pop(0)
    urls = urls[0:10]
    # payload_complete = {
    #     "chunk_size": 1,
    #     "images": urls
    # }
    # messages=[]
    # for url in urls:
    #     messages.append(
    #         {
    #             "chunk_size": 1,
    #             "image": url
    #         }
    #     )


    # to_be_chunked = payload_complete["images"]
    # max_functions = 1000
    # chunked = [to_be_chunked[i:i + max_functions] for i in range(0, len(to_be_chunked), max_functions)]
    # messages = []
    # for chunk in chunked:
    #     messages.append(
    #         {
    #             "chunk_size": 1,
    #             "images": chunk
    #         }
    #     )
    max_batch = 999
    chunked_messages = [urls[i:i + max_batch] for i in range(0, len(urls), max_batch)]

    sqs = boto3.client('sqs', region_name='us-east-1',
                            aws_access_key_id='ASIA4ZTYB6XMN6KGTEV5',
                            aws_secret_access_key='hmlsIhTq+YEEuEwWq4I8hLhrevycutrp5c2DJCD+',
                            aws_session_token='IQoJb3JpZ2luX2VjEOL//////////wEaCXVzLWVhc3QtMSJIMEYCIQDJGH/h47ZnkWS9UbxotxKFiS6ckBD6RgcgnuHB7YpcGwIhAJK1Lwxd3MtkeipibNzQyA3CnLOgH3eKqaKYPjZywew1KvQCCFsQABoMODc5NjQ2MzQwNTY4IgxLNnBofgY/3zg9uZAq0QLQQPD+E509CtZeVZDxcu/7gSnFERtJrnJ7OeikU55zTlZ1san4/NkGvZoEHL0WOL2NXmlJVWq+gn6f9p8hJ+0v35tPyNOfKyf+MSTnz+4A/EP/GF0TuRizJLd8thK3Gvd1a+Qa0gt4wdmr7uGpP+Y/rpDx25JyKut9ctF/D2xpHzYcGKNchODkNwYTK8t6OusoxWdfQlEiT3Q5Z8JY1zlQYvOxqcT0xIHIlVTo5Q042YF8rXDBuXRq+fkRvz6rZPweTBQj8UKZYZDgWi2jBDGIgvVzRxZc/TlX3T+mwb77Pkpllm3Un+80wudzw0L5hMlZHutElU9AHUMnfqlVDUyAWoSHhu8WzZXLmp06drnLfRA0AHKoHwRaA5j14Sn8n5ZSoOK9YnlmFuHoKxGLKYRyBeYELbJFU6DYMuOHixdZDa/iM5b6XAx0fa5XhNi9ieeyMJa1n6UGOqYBk8/8mkYmYECdIGEHnCAHP3pylpsOt/ZBDJ70QDy4+gFJCGF8icuvIyT8+9kzNtJQTTT/jV2mObGWdIKbhHV9KzZnXqDbxhGncVudaTHpLlLufbvJD6pqpYsQji92dc646bwLK6kayUxYvWTI5lT0InOOWSdh02BPkqNf823TwAuAvBG5PS6xduNFb0139wUQ+VGI5JLDzqWb8X6qog79LSyjIOKWGA==')
    queue_url = "https://sqs.us-east-1.amazonaws.com/879646340568/FIFOtest.fifo"
    entries = []
    for i, message in enumerate(chunked_messages):
        print(i)
        string_message=json.dumps(message)
        message_deduplication_id = str(uuid.uuid4())
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=string_message,
            MessageGroupId = str(i),
            MessageDeduplicationId = message_deduplication_id
        )

    print(response)
    with open('results.txt', 'w') as file:
      file.write(json.dumps(response, indent=4))
