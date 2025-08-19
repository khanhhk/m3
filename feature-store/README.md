# How-to Guide

## Prerequisites
Create our virtual environment
```shell
conda create -n fs python=3.9
conda activate fs
pip install -r requirements.txt
```

## Provision the infrastructure
In this lab, we are going to use Kafka, PostgreSQL and Redis, in which:
- Kafka is used to freshen features in PostgreSQL
- PostgreSQL is used as an offline store
- Redis is used as an online store

You can go with another type of offline store from [here](https://docs.feast.dev/reference/offline-stores), or online store from [here](https://docs.feast.dev/reference/online-stores)


Now, launch our infrastructure using `docker compose`
```shell
docker compose -f docker-compose.yaml up -d
```

## Generate master data
This step initialize the offline store with some random values

```shell
cd master_data_producer
python create_table.py
python insert_table.py
```

## Create a feature repository
In this step, we will create a feature repository called `driver_fs`, feel free to use any name you want.
```shell
feast init driver_fs
```
The `driver_fs` repository has the following structure
```shell
driver_fs
├── feature_repo
│   ├── data
│   │   └── driver_stats.parquet
│   ├── example_repo.py
│   ├── feature_store.yaml
│   ├── __init__.py
│   └── test_workflow.py
├── __init__.py
└── README.md
```

For educational purposes, I have changed the name of the folder `driver_fs` to `feature_repos`, and `feature_repo` to `quickstart` so that I can create a new feature repository later in the same repository `feature_repos`.

## Quickstart

```shell
cd feature_repos/quickstart
feast apply
```

Retrieve the training data
```shell
cd feature_retrieval/quickstart
python retrieve_training_data.py
```

Ingest batch features into your online store
```shell
bash materialize.sh
``` 

Retrieve data for inference from online store
```shell
python retrieve_online_features.py
```

To retrieve from online store, you can also retrieve from feature service. First open another terminal and type the following commands to register Feast objects and provision infrastructure. Note that, setting `provider` to any of cloud providers will incur costs.

```shell
cd feature_repos/quickstart
feast apply
```
Run the below command to get the online features
```shell
cd feature_retrieval/quickstart
python retrieve_online_features_by_fs.py
```

## Devices
Similar to the above quickstart, we can retrieve training data and online features from the feature store.

However, you can also freshen the online features using     Kafka stream by using the following command

```shell
cd feature_retrieval/devices
python ingest_stream_to_online_store.py
```
