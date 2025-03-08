# install dependencies for flask
```sh
pip install -r requirements.txt
```

# for use case 1 ml model
```sh
pip install -U diffusers accelerate transformers -q
```

# run MongoDB and Kafka locally in docker
```sh
docker compose up -d
```

## enter the Kafka container
```sh
docker exec --workdir /opt/bitnami/kafka/bin/ -it kafka_mediainsight sh
```

## create a topic
```sh
./kafka-topics.sh --bootstrap-server :9092 --create --topic text2image
./kafka-topics.sh --bootstrap-server :9092 --create --topic generate-description
./kafka-topics.sh --bootstrap-server :9092 --create --topic generate-text
```

# backend api endpoint
DEBUG mode, localhost on port 5000
Running on http://127.0.0.1:5000

e.x.
# create the text-to-image task
```sh
curl --header "Content-Type: application/json" \
  -X POST \
  --data '{"text": "robot"}' \
  http://127.0.0.1:5000/api/v1/generate-image
```
# get the task result
```sh
curl -X GET http://127.0.0.1:5000/api/v1/generate-image/${task_id}
```

