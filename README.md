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
![image](https://user-images.githubusercontent.com/7016538/143961024-2e944760-8393-486a-a417-81aac2227e8b.png)

Client:
![image](https://user-images.githubusercontent.com/7016538/143961091-3d22c557-2ec4-4ef2-8970-6aac21607466.png)

