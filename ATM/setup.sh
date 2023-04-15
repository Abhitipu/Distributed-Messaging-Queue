
sudo docker compose down
sudo rm -rf ../data/*
sudo mkdir -p  ../data/db_one
sudo mkdir -p  ../data/db_two
sudo mkdir -p ../data/db_three
sudo mkdir -p ../data/db_four
sleep 5
sudo docker build . -t atm:latest
sudo docker compose up -d db_one db_two db_three db_four
sleep 15
sudo docker compose up atm_one atm_two atm_three atm_four