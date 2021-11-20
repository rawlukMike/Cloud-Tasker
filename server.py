import sys
import os
import shlex, subprocess
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1

global subscriber
global publisher

if len(sys.argv) != 3:
    print("Cloud tasker server usage: python3 server.py <tasker topic> <listener subscription>")
    print("Tasker topic format: projects/#PROJECT-ID#/topics/#TOPIC-ID#")
    print("Listener subscription format: projects/#PROJECT-ID#/subscriptions/#SUBSCRIPTION-ID#")

sub_listener_id = sys.argv[2]
pub_result_id = sys.argv[1]

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    cmd = message.data.decode()
    print(f"************\nGOT MSG: {cmd}.")
    message.ack()
    command = shlex.split(cmd)
    cmder = None
    try:
        cmder = subprocess.run(command, stdout=subprocess.PIPE)
        result = f"COMMAND:\n{cmd} \nRESULT: \n"+cmder.stdout.decode()
        print(result)
        publisher.publish(pub_result_id, data=result.encode(), result="OK")
        print("PUBLISHED RESULTS")
    except subprocess.CalledProcessError:
        publisher.publish(pub_result_id, data=b"Command failed during execution: PROCESS ERROR", result="FAILED")
        print("PROCESS ERROR")
    except PermissionError:
        publisher.publish(pub_result_id, data=b"Command failed during execution: PERMISSION ERROR", result="FAILED")
        print("PERMISSION ERROR")
    print("************")

streaming_pull_future = subscriber.subscribe(sub_listener_id, callback=callback)
print(f"Listening for messages on {sub_listener_id}..\n")
print(os.getuid())

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

