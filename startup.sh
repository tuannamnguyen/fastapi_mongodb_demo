docker build -t tuannamnguyen290602/fastapi-demo .
docker run -d --rm -p 6379:6379 --name myredis --network fastapi-demo redis
docker run -d --rm --env-file ./.env -p 8000:8000 --name mycontainer --network fastapi-demo tuannamnguyen290602/fastapi-demo
docker run --name mongo --rm -p 1234:27017 mongodb/mongodb-community-server:latest
