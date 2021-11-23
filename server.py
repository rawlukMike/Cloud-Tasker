import sys
import os
import shlex, subprocess
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from time import sleep
global subscriber
global publisher

if len(sys.argv) != 3:
    print("Cloud tasker server usage: python3 server.py server-name tasker-topic")
    print("Tasker topic format: projects/#PROJECT-ID#/topics/#TOPIC-ID#")

server_id = sys.argv[1]
topic_id = sys.argv[2]
project_id=topic_id.split("/")[1]
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()

# MSG RECEIVED FUNCTION
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
    except:
        publisher.publish(pub_result_id, data=b"Command failed during execution: ERROR", result="FAILED")
    finally:
        print("************")


listernerSub_id = f"projects/{project_id}/subscriptions/cloud-tasker-{server_id}-listener"
resultSub_id = f"projects/{project_id}/subscriptions/cloud-tasker-{server_id}-results"

# Killing old servers same name, 
for sub in subscriber.list_subscriptions(request={"project": f"projects/{project_id}"}) :
    if sub.topic_id==topic_id:
        if listernerSub_id==sub.name:
            print("Deleting existing lister sub")
            #TODO: Send Kill, delete sub
        if resultSub_id==sub.name:
            print("Deleting existing result sub")
            #TODO: delete sub
sleep(5)



streaming_pull_future = subscriber.subscribe(sub_listener_id, callback=callback)
print(f"Listening for messages on {sub_listener_id}..\n")
print(os.getuid())

with subscriber:
    try:
        streaming_pull_future.result()
    except TimeoutError:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

