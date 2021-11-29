import sys
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

if len(sys.argv) != 3:
    print("Cloud tasker Client usage: python3 server.py <tasker topic>")
    print("Tasker topic format: projects/#PROJECT-ID#/topics/#TOPIC-ID#")

sub_result_id = sys.argv[2]
pub_cmd_id = sys.argv[1]

global subscriber
global publisher

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

def sendCmd():
    cmd = input("\n*********\nINPUT COMMAND:\n\t")
    publisher.publish(pub_cmd_id, cmd.encode())

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    result = message.data.decode()
    print(f"\nReceived:\n {result}.\n")
    message.ack()
    sendCmd()

print(f"Listening for results on {sub_result_id}..\n")
streaming_pull_future = subscriber.subscribe(sub_result_id, callback=callback)

sendCmd()

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()
