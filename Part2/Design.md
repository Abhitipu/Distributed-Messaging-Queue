## Design Choices

- Choice 1: Decide on the number of partitions for each topic
    - 50 % of current healthy brokers
- Choice 2: Replication
    - Repl Factor: 3
    - Choose 3 brokers and create 3 replicas. Decide addresses at the manager level and do the creation below.
- Choice 3: Implement RAFT at the partition level 
    - Create a separate class for each partition 

### Ponder about
- Healthchecks: does raft sync work on revival
- What if the other addresses are not up
- Bonus: Manager raft to avoid single point of failure