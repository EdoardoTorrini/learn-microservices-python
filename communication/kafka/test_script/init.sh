#!/bin/bash

apt update && apt install -y openjdk-21-jre-headless tmux vim wget unzip

wget https://downloads.apache.org/kafka/3.8.1/kafka_2.13-3.8.1.tgz
tar -xvzf kafka_2.13-3.8.1.tgz

rm *.tgz

cd kafka_2.13-3.8.1
