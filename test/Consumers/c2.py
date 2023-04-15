import time
from ...Part2.ServiceConsumers import MyConsumer

HOST = "localhost"
PORT = 8080
base_url = f"http://{HOST}:{PORT}"
from time import sleep
import random

sleep(5)
c2 = MyConsumer(topics=["T-1",  "T-3"], broker=base_url, partition_ids=[None, None])

start = time.time()
for _ in range(5):
    print(c2.get_next("T-1"))
    # sleep(random.uniform(0, 0.5))
    print(c2.get_next("T-3"))
    # sleep(random.uniform(0, 0.5))

end = time.time()

print(f"Time taken: {end-start} seconds")