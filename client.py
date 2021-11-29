import sys
from google.cloud import pubsub_v1
import tkinter as tk                    
from tkinter import ttk

publisher = pubsub_v1.PublisherClient()
topicPath = ""


if len(sys.argv) == 2:
    project_id = sys.argv[1].split("/")[1]
    topicPath = sys.argv[1]

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

def drawServerTabs(servers):
    serverTabs = {}
    for server in servers:
        x = {}
        x["input"] = tk.StringVar()
        y = ttk.Frame(tabControl)
        ttk.Label(y, 
        text ="Input:").grid(
            column = 0, 
            row = 0)
        ttk.Label(y,
        text ="Result:").grid(
            column = 2, 
            row = 0)
        ttk.Entry(y, textvariable = x["input"]).grid(
        column = 0, 
        row = 1)
        r = tk.Text(y).grid(
        column=1, row=1)
        x["result"] = r
        x["tab"] = y
    serverTabs[server] = x
    for x in serverTabs.keys():
        tabControl.add(serverTabs[x]["tab"], text=x)
        

  
root = tk.Tk()
root.title("Cloud-Tasker Client")

tabControl = ttk.Notebook(root)
  
SettingsTab = ttk.Frame(tabControl)

topic_id = tk.StringVar()
topic_id.set(topicPath)

ttk.Label(SettingsTab, 
    text ="Input your topic path:").grid(
        column = 0, 
        row = 0,
        padx = 10,
        pady = 20)
ttk.Entry(SettingsTab, textvariable=topic_id).grid(
        column = 1, 
        row = 0,
        padx = 10,
        pady = 20)

ttk.Button(SettingsTab, text ="Connect", command = detectServers).grid(
        column = 1, 
        row = 1,
        padx = 10,
        pady = 20)
  
tabControl.add(SettingsTab, text ='Settings')
tabControl.pack(expand = 1, fill ="both")

root.mainloop()









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