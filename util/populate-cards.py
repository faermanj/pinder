#!/usr/bin/env python3

from time import sleep
from random import random
import urllib.request
import time
import boto3
import uuid
import json

print("hello")
cards_bucket = "pinder-cards-4-cardsbucket-1omm8ewi2ym3b"
cards_table = "pinder-cards-4-CardsTable-1DE0AOORZO9EP"
while True:
    print("fetch image")
    rand_uuid = str(uuid.uuid4())
    url = "https://source.unsplash.com/collection/1424240/500x500?uuid=" + rand_uuid
    file_key = rand_uuid + ".png"
    filename = "./temp/" + file_key
    urllib.request.urlretrieve(url, filename)

    print("upload [" + filename + "] to s3://" + cards_bucket + "/" + file_key)
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(filename, cards_bucket, file_key)

    print("detect lables")
    rekognition = boto3.client('rekognition')

    response = rekognition.detect_labels(
        Image={'S3Object': {
            'Bucket': cards_bucket,
            'Name': file_key
        }},
        MaxLabels=3)
    _confident = lambda l: l.Confidence > 80
    labels = response["Labels"]
    goodlabels = filter(_confident, labels)
    _name = lambda l: l["Name"]
    label_names = list(map(_name, labels))
    print(str(label_names))

    print("index in dynamodb")
    card_item = {
        "uuid": rand_uuid,
        "rand": round(random() * 10000),
        "bucket": cards_bucket,
        "key": file_key,
        "labels": label_names
    }
    dynamodb = boto3.resource('dynamodb')
    cards_ddb_table = dynamodb.Table(cards_table)
    cards_ddb_table.put_item(Item=card_item)

    print("done")
    print(json.dumps(card_item))
    print("wait for next image")
    sleep(10)
print("done")