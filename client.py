import argparse
from google.cloud import pubsub_v1
import tkinter as tk

# Input Arg parse
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

# Setup variables
server_id = results.server_id
topic_id = results.topic_id
sub_id = results.resultSub_id
project_id = topic_id.split("/")[1]
topic_name = topic_id.split("/")[3]

# Init Publisher client
publisher = pubsub_v1.PublisherClient()

# Send cmd action
def sendCmd():
    x = cmdEntry.get()
    publisher.publish(topic_id, x.encode(), serverid=server_id)

# Action on result msg
def callback(message: pubsub_v1.subscriber.message.Message) -> None:
    result = message.data.decode()
    resultText.delete(1.0, tk.END)
    resultText.insert(1.0, result)
    message.ack()

# GUI Define
win = tk.Tk()
win.title("Cloud-Tasker Client")
win.geometry("600x360+10+10")
servLbl2=tk.Label(win, text="Sending to:")
servLbl=tk.Label(win, text=server_id)
cmdLbl=tk.Label(win, text='Command:')
resultLbl=tk.Label(win, text='Result:')
cmdEntry=tk.Entry(win, bd=2, width=67)
resultText=tk.Text(win, bd=2,width=50, height=15)
sendBtn=tk.Button(win, text="Send", command=sendCmd)

# GUI Placement
servLbl2.place(x=15,y=10)
servLbl.place(x=90,y=10)
cmdLbl.place(x=15,y=40)
cmdEntry.place(x=90, y=40)
sendBtn.place(x=530,y=37)
resultLbl.place(x=15,y=80)
resultText.place(x=90,y=81)

# Main loop
with pubsub_v1.SubscriberClient() as subscriber:
    # Async msg pull
    streaming_pull_future = subscriber.subscribe(sub_id, callback=callback)
    # Window main loop
    win.mainloop()