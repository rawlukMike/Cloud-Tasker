import sys
import argparse
from pyfiglet import Figlet
from google.cloud import pubsub_v1
from Models.taskerServer import CloudTaskerServer


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-n', action='store',
                    dest='server_id',
                    help='Server Name',
                    required=True)

parser.add_argument('-t', action='store',
                    dest='topic_id',
                    help='Tasker topic format: projects/#PROJECT-ID#/topics/#TOPIC-NAME#',
                    required=True)

parser.add_argument('-m', action='store_true',
                    default=False,
                    dest='multiple_mode',
                    help='If server should work in many instances mode')

parser.add_argument('--version', action='version',
                    version='%(prog)s 1.0')

results = parser.parse_args()

server_id = results.server_id
topic_id = results.topic_id
multiple_servers = results.multiple_mode
project_id = topic_id.split("/")[1]
topic_name = topic_id.split("/")[3]
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
figlet = Figlet(font='slant')

serverSub_listener_name = f"{topic_name}-{server_id}-listener"
serverSub_result_name = f"{topic_name}-{server_id}-result"

serverSub_listener = f"projects/{project_id}/subscriptions/{topic_name}-{server_id}-listener"
serverSub_result = f"projects/{project_id}/subscriptions/{topic_name}-{server_id}-result"


print(figlet.renderText('Cloud Tasker'))
print(f"# Server Name: {server_id}")
print(f"# Topic path: {topic_id}")
print(f"# Listener Sub name: {serverSub_listener_name}")
print(f"# Result Sub Name: {serverSub_result_name}")
print(f"# Multiple servers: {str(multiple_servers)}")

# For Handling Sub Close on Exit
def exiter(multiple_servers):
    if not multiple_servers:
        try:
            print("# Deleting listener subcription.")
            subscriber = pubsub_v1.SubscriberClient()
            with subscriber:
                subscriber.delete_subscription(request={"subscription": serverSub_listener})
        except:
            print(f"ERROR: Not able to delete: {serverSub_listener}")
        try:
            print("# Deleting result subcription.")
            subscriber = pubsub_v1.SubscriberClient()
            with subscriber:
                subscriber.delete_subscription(request={"subscription": serverSub_result})
        except:
            print(f"ERROR: Not able to delete: {serverSub_result}")
        print("# Subscriptions deleted")


try:
    print("# PreRun check of subcriptions")
    # CHECK IF SUBS ALREADY IN PLACE WHICH INDACATES OTHER SERVERS ARE OPERATIONAL
    # TODO: server cmds to handle closing and ping
    # TODO: Don't fail on create if multiple mode
    for sub in publisher.list_topic_subscriptions(request={"topic": topic_id}):
        if serverSub_listener==sub:
            if not multiple_servers: raise Exception("### ERROR: Listener subscription already exists. No multiple mode, stopping server")
        if serverSub_result==sub:
            if not multiple_servers: raise Exception("### ERROR: Result subscription already exists. No multiple mode, stopping server")


    # CREATE SUBS
    print("# Creating Subscriptions")

    filterResult = f'attributes:result AND attributes.serverid = "{server_id}"'
    filterListener = f'NOT attributes:result AND attributes.serverid = "{server_id}"'

    with subscriber:
        subscriber.create_subscription(
            request={
                "name": serverSub_listener,
                "topic": topic_id,
                "filter": filterListener
                }
        )
        print("\tListener Subscription: Created")
        subscriber.create_subscription(
            request={
                "name": serverSub_result,
                "topic": topic_id,
                "filter": filterResult
                }
        )
        print("\tResult Subscription: Created")

    # RUN SERVER    
    server = CloudTaskerServer(server_id, serverSub_listener, topic_id)
    server.run()
except Exception as e:
    print (e)

finally:
    exiter(multiple_servers)
    sys.exit()

