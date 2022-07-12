$image = "service"
docker build . -t project/server
docker tag project/server registryd.avantrio.xyz/project/server
docker push registryd.avantrio.xyz/project/server