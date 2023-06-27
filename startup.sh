docker build -t myimage .
docker run --rm --env-file ./.env -p 8000:8000 --name mycontainer myimage