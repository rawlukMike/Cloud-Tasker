# Cloud-Tasker
Simple solution to run commands through event driven cloud solutions.
Currently support GCP PubSub Only

### Requirements :
  python3 -m pip install --upgrade pip setuptools wheel
  python3 -m pip install --upgrade google-cloud-pubsub


### Usage Client:
  python3 client.py <tasker topic> <result subscription>
  
### Usage Server:
  python3 server.py <tasker topic> <listener subscription>

### Screenshot:
  ![image](https://user-images.githubusercontent.com/7016538/142743261-333497d9-0915-4b34-b4d8-a9c8f1dc0d31.png)
