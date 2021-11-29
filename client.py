import sys, argparse
from google.cloud import pubsub_v1
import tkinter as tk                    
from tkinter import ttk


parser = argparse.ArgumentParser(add_help=True)
parser.add_argument('-n', action='store',
                    dest='server_id',
                    help='Server Name',
                    required=True)

parser.add_argument('-t', action='store',
                    dest='topic_id',
                    help='Tasker topic format: projects/#PROJECT-ID#/topics/#TOPIC-NAME#',
                    required=True)

parser.add_argument('-s', action='store',
                    dest='resultSub_id',
                    help='Result Sub format: projects/#PROJECT-ID#/subscriptions/#subscription-NAME#',
                    required=True)

parser.add_argument('--version', action='version',
                    version='%(prog)s 1.0')

results = parser.parse_args()

server_id = results.server_id
topic_id = results.topic_id
sub_id = results.resultSub_id
project_id = topic_id.split("/")[1]
topic_name = topic_id.split("/")[3]

subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

def sendCmd():
    x = cmdEntry.get()
    publisher.publish(topic_id, x.encode(), serverid=server_id)

win = tk.Tk()
win.title("Cloud-Tasker Client")
win.geometry("700x300+10+10")
servLbl=tk.Label(win, text=server_id)
cmdLbl=tk.Label(win, text='Command:')
resultLbl=tk.Label(win, text='Result:')
cmdEntry=tk.Entry(win, bd=2, width=67)
resultText=tk.Text(win, bd=2,width=50)
sendBtn=tk.Button(win, text="Send", command=sendCmd)

servLbl.place(x=180,y=10)
cmdLbl.place(x=15,y=40)
cmdEntry.place(x=90, y=40)
sendBtn.place(x=530,y=37)
resultLbl.place(x=15,y=80)
resultText.place(x=90,y=81)

def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    result = message.data.decode()
    resultText.delete(tk.INSERT, tk.END)
    resultText.insert(1.0, result)
    message.ack()

streaming_pull_future = subscriber.subscribe(sub_id, callback=callback)


win.mainloop()






'''
def detectServers():
    subscriber = pubsub_v1.SubscriberClient()
    servers = set()
    with subscriber:
        for subscription in subscriber.list_subscriptions(
            request={"project": "projects/"+project_id}):
            if "cloudtasker" in subscription.labels.keys():
                servers.add(subscription.labels["cloudtasker"])
    print(servers)
    drawServerTabs(servers)
'''


'''
if len(sys.argv) != 3:
    print("Cloud tasker Client usage: python3 client.py <tasker topic>")
    print("Tasker topic format: projects/#PROJECT-ID#/topics/#TOPIC-ID#")

sub_result_id = sys.argv[2]
pub_cmd_id = sys.argv[1]

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
'''