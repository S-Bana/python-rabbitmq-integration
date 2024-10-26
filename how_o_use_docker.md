# download, run and setup rabbitmq in docker

'''
docker run -d
    --hostname my-rabbit
    --name some-rabbit
    -e RABBITMQ_DEFAULT_USER=bob
    -e RABBITMQ_DEFAULT_PASS=bob
    -p 5672:5672
    -p 15672:15672
    rabbitmq:3-management
'''

# url for connect rabitmq management 
http://localhost:15672/

# run rabbitmq at docker in interactive mode 
docker exec -it some-rabbit bash

# stop docker container rabbitmq
docker container stop some-rabbit

# remove a docker container
docker container rm some-rabbit

# remove an image from docker
docker rmi rabbitmq:3-management
