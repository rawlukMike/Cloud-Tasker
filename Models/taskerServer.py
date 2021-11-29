import subprocess
import shlex
from google.cloud import pubsub_v1
from concurrent.futures import TimeoutError

class CloudTaskerServer:
    def __init__(self, serverId, listenSub, resultTop):
        self.serverId = serverId
        self.listenSub = listenSub
        self.resultTop = resultTop

    def callback(self, message: pubsub_v1.subscriber.message.Message) -> None:
        cmd = message.data.decode()
        print(f"************\nGOT MSG: {cmd}.")
        message.ack()
        command = shlex.split(cmd)
        cmder = None
        try:
            cmder = subprocess.run(command, stdout=subprocess.PIPE)
            result = f"COMMAND:\n{cmd} \nRESULT: \n"+cmder.stdout.decode()
            print(result)
            self.publisher.publish(self.resultTop, data=result.encode(), result="OK", serverid=self.serverId)
            print("PUBLISHED RESULTS")
        except subprocess.CalledProcessError:
            self.publisher.publish(self.resultTop, data=b"Command failed during execution: PROCESS ERROR", result="FAILED", serverid=self.serverId)
            print("PROCESS ERROR")
        except PermissionError:
            self.publisher.publish(self.resultTop, data=b"Command failed during execution: PERMISSION ERROR", result="FAILED", serverid=self.serverId)
            print("PERMISSION ERROR")
        except:
            self.publisher.publish(self.resultTop, data=b"Command failed during execution: ERROR", result="FAILED", serverid=self.serverId)
        finally:
            print("************")
    
    def run(self):
        self.publisher = pubsub_v1.PublisherClient()
        self.subscriber = pubsub_v1.SubscriberClient()
        streaming_pull_future = self.subscriber.subscribe(self.listenSub, callback=self.callback)
        print(f"Listening for messages on {self.listenSub}..\n")
        with self.subscriber:
            try:
                streaming_pull_future.result()
            except TimeoutError:
                streaming_pull_future.cancel()
                streaming_pull_future.result()