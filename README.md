# redis-message-queue-example

## Table of Contents

<!-- vim-markdown-toc GFM -->

* [Bootstrap](#bootstrap)
* [Spin up a local Redis instance](#spin-up-a-local-redis-instance)
* [Connect to Redis](#connect-to-redis)
* [Create a consumer group](#create-a-consumer-group)
* [Exec virtualenv](#exec-virtualenv)
* [Publish message](#publish-message)
* [Consume message](#consume-message)

<!-- vim-markdown-toc -->

## Bootstrap

```bash
./install
```

## Spin up a local Redis instance

```bash
cd docker
docker compose up -d
```

## Connect to Redis

```bash
redis-cli -u redis://127.0.0.1:6379/0
```

## Create a consumer group

```bash
XGROUP CREATE demo consumer_group 0 MKSTREAM
```

## Exec virtualenv

```bash
. ./venv/bin/activate.fish
```

## Publish message

```bash
python3 publisher.py
```

## Consume message

```bash
python3 consumer.py
```
