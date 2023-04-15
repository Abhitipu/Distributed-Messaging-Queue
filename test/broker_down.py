import random
import requests
from time import sleep

# Basically we test replication abilities here
# We need to produce to and consume from a single patition only
# We create replicas of the particular partition and
# make the corresponding brokers down to test both produce and consume

# Only when all of them are down, they should fail
# Else, it should work

# NOTE: Also check if the raft consensus is 
# maintained even after broker is down.
def test(HOST, PORT):
    base_url = f"http://{HOST}:{PORT}"
    print(f"Hitting the base url: {base_url}")
    
    # register broker (3): happens by default
    print("Run docker compose to start the brokers")
    _ = input("Press enter to continue")
    
    counter = 0
    # Register producer
    print("Testing the endpoint register producer (new topic)")
    url = base_url + "/producer/register"
    data = {
        "topic_name": "topic_1"
    }
    producer_id = None
    try:
        print(f"request = {data}")
        r = requests.post(url, json=data)
        r.raise_for_status()
        response = r.json()
        print("Response")
        producer_id = response["producer_id"]
        print(response)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    print()
    
    # Register consumer
    print("Testing the endpoint register consumer (partition level)")
    url = base_url + "/consumer/register"
    partition_id = input("Enter the partition_id")
    # TODO: we need to fix the partition to read from here 
    data = {
        "topic_name": "topic_1",
        "partition_id": partition_id
    }

    consumer_id = None
    try:
        print(f"request = {data}")
        r = requests.post(url, json=data)
        r.raise_for_status()
        response = r.json()
        print("Response")
        consumer_id = response['consumer_id']
        print(response)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    # Produce to topic
    print("Testing production to general partition (randomized)")
    
    num_of_messages = 10
    print(f"Pushing {num_of_messages} messages on Topic topic_1")
    
    # TODO: Always produce to a fixed partition 
    # IDEA: Maybe use 0 as id
    url = base_url + "/producer/produce"
    try:
        for i in range(num_of_messages):
            data = {
                "topic_name": "topic_1",
                "producer_id": producer_id,
                "partition_id": partition_id,
                "message": f"LOG MESSAGE {counter + 1}"
            }
            counter += 1
            print(f"request = {data}")
            r = requests.post(url, json=data)
            r.raise_for_status()
            response = r.json()
            print("Response")
            print(response)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    print()
    print(f"INSTRUCTION: Make broker 1 [Find parititon {partition_id} replicas first] down")
    _ = input("Press enter to continue...")
    
    # Make broker 1 down
    # Consume some messages from broker 2 and 3 (Basically the ones having a replica)
    # Also produce some messages to broker 2 and 3 (Should work again)
    print(f"Consuming messages using the consumer {consumer_id} and reporting size too")

    try:
        data = {
            "topic_name": "topic_1",
            "consumer_id": consumer_id,
        }
        print(f"request = {data}")
        for _ in range(num_of_messages):
            print()

            url = url = base_url + "/size"
            print(f"Size of topic_1 for given consumer")
            r = requests.get(url, json=data)
            response = r.json()
            print("Response")
            print(response)
            
            if response['size'] == 0:
                break
            
            print()
            print(f"Consuming messages")
            url = base_url + "/consumer/consume"
            
            r = requests.get(url, json=data)
            r.raise_for_status()
            response = r.json()
            print("Response")
            print(response)
            
            sleep(0.02)
            
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    print("Testing production to general partition (randomized)")
    
    print(f"Pushing {num_of_messages} messages on Topic topic_1")
    
    url = base_url + "/producer/produce"
    try:
        for i in range(num_of_messages):
            data = {
                "topic_name": "topic_1",
                "producer_id": producer_id,
                "message": f"LOG MESSAGE {counter + 1}",
                "partition_id": partition_id,
            }
            counter += 1
            print(f"request = {data}")
            r = requests.post(url, json=data)
            r.raise_for_status()
            response = r.json()
            print("Response")
            print(response)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    print("INSTRUCTION: Make broker 2 down")
    _ = input("Press enter to continue...")
    
    # Make broker 2 down
    # Consume some more messages from broker 3 (Should keep working)
    # Also produce some messages to broker 3 (Should keep working)
    print(f"Consuming messages using the consumer {consumer_id} and reporting size too")

    try:
        data = {
            "topic_name": "topic_1",
            "consumer_id": consumer_id,
        }
        print(f"request = {data}")
        for _ in range(num_of_messages):
            print()

            url = url = base_url + "/size"
            print(f"Size of topic_1 for given consumer")
            r = requests.get(url, json=data)
            response = r.json()
            print("Response")
            print(response)
            
            if response['size'] == 0:
                break
            
            print()
            print(f"Consuming messages")
            url = base_url + "/consumer/consume"
            
            r = requests.get(url, json=data)
            r.raise_for_status()
            response = r.json()
            print("Response")
            print(response)
            
            sleep(0.02)
            
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    print("Testing production to specific partition")
    
    print(f"Pushing {num_of_messages} messages on Topic topic_1")
    
    url = base_url + "/producer/produce"
    try:
        for i in range(num_of_messages):
            data = {
                "topic_name": "topic_1",
                "producer_id": producer_id,
                "message": f"LOG MESSAGE {counter + 1}",
                "partition_id": partition_id,
            }
            counter += 1
            print(f"request = {data}")
            r = requests.post(url, json=data)
            r.raise_for_status()
            response = r.json()
            print("Response")
            print(response)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    print("INSTRUCTION: Make broker 3 down")
    _ = input("Press enter to continue...")
    # Make broker 3 down
    # Should not be able to consume messages (since all replicas are down)
    # Produce should also fail
    print(f"Consuming messages using the consumer {consumer_id} and reporting size too")
    try:
        data = {
            "topic_name": "topic_1",
            "consumer_id": consumer_id,
        }
        print(f"request = {data}")
        print()

        url = url = base_url + "/size"
        print(f"Size of topic_1 for given consumer")
        r = requests.get(url, json=data)
        response = r.json()
        print("Response")
        print(response)
        
        print()
        print(f"Consuming messages")
        url = base_url + "/consumer/consume"
        
        r = requests.get(url, json=data)
        r.raise_for_status()
        response = r.json()
        print("Response")
        print(response)
        
        assert response['status'] == 'Failure'
        
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    print("Testing production to general partition (randomized)")
    
    print(f"Pushing 1 message on Topic topic_1")
    
    url = base_url + "/producer/produce"
    try:
        data = {
            "topic_name": "topic_1",
            "producer_id": producer_id,
            "message": f"LOG MESSAGE {counter + 1}"
            "partition_id": partition_id,
        }
        print(f"request = {data}")
        r = requests.post(url, json=data)
        r.raise_for_status()
        response = r.json()
        print("Response")
        print(response)
        assert response['status'] == 'Failure'
        
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)

    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    
    print("INSTRUCTION: Broker 3 up")
    _ = input("Press enter to continue...")
    
    # Make broker 3 up
    # Consume until you can
    print(f"Consuming messages using the consumer {consumer_id} and reporting size too")

    try:
        data = {
            "topic_name": "topic_1",
            "consumer_id": consumer_id,
        }
        print(f"request = {data}")
        while True:
            print()

            url = url = base_url + "/size"
            print(f"Size of topic_1 for given consumer")
            r = requests.get(url, json=data)
            response = r.json()
            print("Response")
            print(response)
            
            if response['size'] == 0:
                break
            
            print()
            print(f"Consuming messages")
            url = base_url + "/consumer/consume"
            
            r = requests.get(url, json=data)
            r.raise_for_status()
            response = r.json()
            if response['status'] == 'Failure':
                break
            print("Response")
            print(response)
            
            sleep(0.02)
            
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        
    print("INSTRUCTION: Broker 2 up")
    _ = input("Press enter to continue...")      
    # Make broker 2 up
    # Consume until you can
    
    print(f"Consuming messages using the consumer {consumer_id} and reporting size too")

    try:
        data = {
            "topic_name": "topic_1",
            "consumer_id": consumer_id,
        }
        print(f"request = {data}")
        while True:
            print()

            url = url = base_url + "/size"
            print(f"Size of topic_1 for given consumer")
            r = requests.get(url, json=data)
            response = r.json()
            print("Response")
            print(response)
            
            if response['size'] == 0:
                break
            
            print()
            print(f"Consuming messages")
            url = base_url + "/consumer/consume"
            
            r = requests.get(url, json=data)
            r.raise_for_status()
            response = r.json()
            print("Response")
            print(response)
            
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    
    print("INSTRUCTION: Broker 1 up")
    _ = input("Press enter to continue...")
    # Make broker 1 up
    # Consume until you can
    
    print(f"Consuming messages using the consumer {consumer_id} and reporting size too")

    try:
        data = {
            "topic_name": "topic_1",
            "consumer_id": consumer_id,
        }
        print(f"request = {data}")
        while True:
            print()

            url = url = base_url + "/size"
            print(f"Size of topic_1 for given consumer")
            r = requests.get(url, json=data)
            response = r.json()
            print("Response")
            print(response)
            
            if response['size'] == 0:
                break
            
            print()
            print(f"Consuming messages")
            url = base_url + "/consumer/consume"
            
            r = requests.get(url, json=data)
            r.raise_for_status()
            response = r.json()
            print("Response")
            print(response)
            
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
        

if __name__ == "__main__":
    # register broker: happens by default
    HOST = "localhost"
    PORT = 8080
    test(HOST, PORT)
    # broker1 down