from ...Part2.ServiceConsumers import MyProducer
import random
import time

HOST = "localhost"
PORT = 8080
base_url = f"http://{HOST}:{PORT}"

p4 = MyProducer(topics=["T-2"], broker=base_url)

start = time.time()
with open("test/test_asgn1/producer_4.txt", "r") as f:
    for line in f:
        line=line.strip()
        topic = line.split('\t')[-1]
        message= '\t'.join(line.split('\t')[:-1])
        while True:
            response = p4.send(topic_name=topic, message=message)
            if response is not None and response["status"] == "Success":
                break
        # time.sleep(random.uniform(0,1))

end = time.time()
print("Time taken: ", end-start, " seconds")