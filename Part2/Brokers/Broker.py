
from typing import Dict, List, Tuple, Set
from BrokerModels import ReplicatedTopicName, ReplicatedTopicMessage
import requests
from time import sleep
import sys 
class LoggingQueue():
    def __init__(self):
        self.ReplicatedTopicName_obj = ReplicatedTopicName()
        self.ReplicatedTopicMessage_obj = ReplicatedTopicMessage()

    # def set_app(self,app):
    #     self.ReplicatedTopicName_obj.set_app(app)
    #     self.ReplicatedTopicMessage_obj.set_app(app)

    def wait_till_ready(self):
        print("hi before bind 1 ",file=sys.stderr)
        self.ReplicatedTopicName_obj.waitBinded()
        print("hi before read 1 ",file=sys.stderr)
        self.ReplicatedTopicName_obj.waitReady()
        print("hi before bind 2 ",file=sys.stderr)
        
        self.ReplicatedTopicMessage_obj.waitBinded()
        print("hi before read 2 ",file=sys.stderr)
        
        self.ReplicatedTopicMessage_obj.waitReady()
        print("hi after read 2 ",file=sys.stderr)
        
    def heartbeat(self, ip: str, port: int, broker_id, self_port) -> None:
        data = {"broker_id": broker_id, "port": self_port}
        send_url = f"http://{ip}:{port}/broker/receive_beat"

        while True:
            try:
                r = requests.post(send_url, json=data)
                # print("sending beat")
                r.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            sleep(0.05)

    def create_topic(self, topic_name: str, partition_id) -> None:
        if not self.ReplicatedTopicName_obj.CheckTopic(topic_name=topic_name, partition_id=partition_id):
            self.ReplicatedTopicName_obj.CreateTopic(topic_name=topic_name,
                                  partition_id=partition_id,sync=True)
            print(f"Topic {topic_name} with partition {partition_id} created.")
            return 1
        else:
            print(
                f"Topic {topic_name} with partition {partition_id} already exists.")
            return -1

    def list_topics(self) -> List[Tuple[str, str]]:
        topic_part_list = self.ReplicatedTopicName_obj.ListTopics()
        return topic_part_list
    
    def enqueue(self, message: str, topic: str, partition_id: int, broker_ids) -> int:
        # check if (topic, partition_id) exists else create it
        if not self.ReplicatedTopicName_obj.CheckTopic(topic_name=topic, partition_id=partition_id):
            status = self.ReplicatedTopicName_obj.CreateTopic(topic_name=topic, partition_id=partition_id, broker_ids=broker_ids, sync=True)
            if status == 1:
                print(f"Topic {topic} with partition {partition_id} created.")
            else:
                print("Topic creation not meant for this broker")

        status = self.ReplicatedTopicMessage_obj.addMessage(
            topic_name=topic, partition_id=partition_id, message=message, broker_ids=broker_ids, sync=True)
        if status == 1:
            print(
                f"Message '{message}' added to topic {topic} with partition {partition_id}.")
            return 1
        elif status == 2:
            print(
                f"Message not meant for this broker")
            return 1
        else:
            print(
                f" {status} Message '{message}' could not be added to topic {topic} with partition {partition_id}.")
            return -1

    def dequeue(self, topic_name: str, partition_id: int, offset: int, *args, **kwargs) -> str:

        if not self.ReplicatedTopicName_obj.CheckTopic(topic_name=topic_name, partition_id=partition_id):
            print(
                f"Topic {topic_name} with partition {partition_id} does not exist.")
            return -1

        message = self.ReplicatedTopicMessage_obj.retrieveMessage(topic_name=topic_name, partition_id=partition_id,
                                               offset=offset)
        if (isinstance(message, str)):
            print(
                f"Message '{message}' from topic {topic_name}, partition {partition_id}.")
            return message
        elif message == -1:
            print(f"No message in queue!!!")
            return -2

    def size(self, topic_name: str, partition_id: str, offset) -> int:
        if not self.ReplicatedTopicName_obj.CheckTopic(topic_name=topic_name, partition_id=partition_id):
            print(
                f"Topic {topic_name} with partition {partition_id} does not exist.")
            return -1
        return self.ReplicatedTopicMessage_obj.getSizeforTopic(topic_name=topic_name, partition_id=partition_id, offset=offset)

    # def set_details(self, broker_id, ip, port):
    #     self.DetailsDB.addBrokerDetails(broker_id=broker_id, ip=ip, port=port)

    # def get_details(self):
    #     broker = self.DetailsDB.getBrokerDetails()
    #     if broker == -1:
    #         print("No broker details found.")
    #     return broker   # -1 if broker does not exist


