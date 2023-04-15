import time
from time import sleep
import random
from ...Part2.ServiceConsumers import MyConsumer
HOST = "localhost"
PORT = 8080
base_url = f"http://{HOST}:{PORT}"

sleep(5)
c1 = MyConsumer(topics=["T-1", "T-2", "T-3"], broker=base_url, partition_ids=[None, None, None])

start = time.time()

for _ in range(5):
    print(c1.get_next("T-1"))
    # sleep(random.uniform(0, 0.5))
    print(c1.get_next("T-2"))
    # sleep(random.uniform(0, 0.5))
    print(c1.get_next("T-3"))
    # sleep(random.uniform(0, 0.5))

end = time.time()

print(f"Time taken: {end-start} seconds")