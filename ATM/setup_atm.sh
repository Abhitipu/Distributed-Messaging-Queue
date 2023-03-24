sudo rm -rf ../data
sudo docker build . -t atm:latest
mkdir -p ../data
docker compose down
docker compose up -d cockroach1
docker compose up -d cockroach2
docker compose up -d cockroach3
docker exec -ti cockroach1 ./cockroach init --insecure
docker compose up