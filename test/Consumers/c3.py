from ...Part2.ServiceConsumers import MyConsumer
from time import sleep
import random
import time

HOST = "localhost"
PORT = 8080
base_url = f"http://{HOST}:{PORT}"
#  Regitering to partition 0

sleep(5)
c3 = MyConsumer(topics=["T-1", "T-3"], broker=base_url, partition_ids = [0, None])

start = time.time()
for _ in range(5):
    print(c3.get_next("T-1"))
    # sleep(random.uniform(0, 0.5))
    print(c3.get_next("T-3"))
    # sleep(random.uniform(0, 0.5))

end = time.time()
print(f"Time taken: {end-start} seconds")