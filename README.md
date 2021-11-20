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
