sudo rm -rf ../data
mkdir -p ../data
docker compose -f cockroachdb_test.yaml down
docker compose -f cockroachdb_test.yaml up -d cockroach1
docker compose -f cockroachdb_test.yaml up -d cockroach2
docker compose -f cockroachdb_test.yaml up -d cockroach3
docker exec -ti cockroach1 ./cockroach init --insecure
