## Create a Topic
```bash
$ bin/kafka-topics.sh --create --topic <topic_name> --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1

$ bin/kafka-topics.sh --list --bootstrap-server kafka:9092
```

## Producer
```bash
$ bin/kafka-console-producer.sh --broker-list kafka:9092 --topic <topic_name>
> Message
```

## Consumer
```bash
$ bin/kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic <topic_name> --from-beginning
```