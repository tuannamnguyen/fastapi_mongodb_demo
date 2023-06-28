docker build -t myimage .
docker run -d --rm -p 6379:6379 --name myredis --network fastapi-demo redis
docker run -d --rm --env-file ./.env -p 8000:8000 --name mycontainer --network fastapi-demo myimage 