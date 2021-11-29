# Cloud-Tasker
Simple solution to run commands through event driven cloud solutions.
Currently support GCP PubSub Only

### Requirements :
  python3 -m pip install --upgrade pip setuptools wheel
  python3 -m pip install --upgrade google-cloud-pubsub pyfiglet

### Usage Client:
Server will create subscription and list you name, but it will be in format: your-topic-server-name-result
  python3 client.py -n server-name -t projects/sample-project/topics/your-topic -s projects/sample-project/subscriptions/your-topic-server-name-result
  
### Usage Server:
  python3 server.py -n server-name -t projects/sample-project/topics/your-topic

### Screenshot:

Server:
  ![image](https://user-images.githubusercontent.com/7016538/142743261-333497d9-0915-4b34-b4d8-a9c8f1dc0d31.png)
