# Cloud-Tasker
Simple solution to run commands through event driven cloud solutions.
Currently support GCP PubSub Only

## Use Case:
For situaction where there is no ssh connection to machine, but some maintaince could be useful.
As long as machine has access to pubsub scope, it can be maintained this way.
It's also an alternative to startup script, since It can be runned as any user and does not require restart per change.

## Requirements :
  `python3 -m pip install --upgrade google-cloud-pubsub pyfiglet`

## Usage Client:
  `python3 client.py -n servername -t projects/sample-project/topics/yourtopic -s projects/sample-project/subscriptions/yourtopicservernameresult`
  
## Usage Server:

### Whitelist
You can pass json file in format:
`
{
    "whitelist" : [
        "sample-cmd1",
        "cmd2"
    ]
}`

as config param -c. Server will only run cmd same as whitelist.
This is optional parameter. Server will allow every other cmd otherwise.

### Running
Server will create subscription and list you name (yourtopic-servername-result).

  `python3 server.py -n servername -t projects/sample-project/topics/yourtopic -c whitelist.json`

## Screenshot:

### Server:
![image](https://user-images.githubusercontent.com/7016538/143961024-2e944760-8393-486a-a417-81aac2227e8b.png)

### Client:
![image](https://user-images.githubusercontent.com/7016538/143961091-3d22c557-2ec4-4ef2-8970-6aac21607466.png)

