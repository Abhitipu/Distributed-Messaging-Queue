# IP="127.1"
# PORT=8081
# For this we simply put a timer in all the individual files
# test.Producers and test.Consumers

# Then to measure the times we simply take a max
# Of all the times
python -m test.Producers.p1 > log_p1&
python -m test.Producers.p2 > log_p2& 
python -m test.Producers.p3 > log_p3& 
python -m test.Producers.p4 > log_p4& 
python -m test.Producers.p5 > log_p5& 
python -m test.Consumers.c1 > log_c1& 
python -m test.Consumers.c2 > log_c2& 
python -m test.Consumers.c3 > log_c3&