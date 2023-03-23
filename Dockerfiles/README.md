File `etcd_test.yaml` sets up a test etcd cluster 
## Steps 
1. `docker compose -f etcd_test.yaml up`
2. `docker exec -it {container id}`
3. inside the container use the following two commands 
    1.  `etcdctl put key value`
    2.    `etcdctl get key`

Check container id with `docker container ls`