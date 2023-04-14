@echo off
docker compose down
call folder.cmd
sleep 5
docker build . -t atm:latest
docker compose up -d db_one db_two db_three db_four
sleep 90
docker compose up -d atm_one atm_two atm_three atm_four