## Design Choices

- Choice 1: Decide on the number of partitions for each topic
    - x/y of current healthy brokers (maybe 50% or 33%)
- Choice 2: Replication
    - Decision at manager level
    - In all messages add replica endpoints
    - Return from the requested endpoint only
- Choice 3: Implement RAFT at broker level 

### Ponder about
- Healthchecks: does raft sync work on revival -- sync via manager
- What if the other addresses are not up -- need to see if it gets stuck

### Bonus 
- Bonus: Manager raft to avoid single point of failure
