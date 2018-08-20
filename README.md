# Manager route53 rules

## Prerequisite
> Boto3 in version 1.7.2

> python version >= 3

## Install Boto3
```bash
$ pip3.5 install -r requirements.txt
```

## Help Function
```bash
$ ./main.py -h
usage: main.py [-h] --profile PROFILE --zone ZONE --action ACTION
               [--resourcezone RESOURCEZONE] [--dns DNS] [--type TYPE]
               [--ttl TTL] [--target TARGET]

Manager Route53

optional arguments:
  -h, --help            show this help message and exit
  --resourcezone RESOURCEZONE
                        resource zone DNS if you want to manipulate
  --dns DNS             source dns
  --type TYPE           type of resource
  --ttl TTL             time to live for your dns
  --target TARGET       target dns

required arguments:
  --profile PROFILE     aws cli profile in you machine
  --zone ZONE           zone in AWS
  --action ACTION       action in route53
```

## GET hosted zones
```bash
$ ./main.py --zone us-east-1 --action GETZONES --profile dev
```

## GET resources
```bash
$ ./main.py --zone us-east-1 --action GET --profile dev --resourcezone my.hosted.address.com.
```

## Create A resource
```bash
$ ./main.py --zone us-east-1 --action CREATE --dns node02.teste.my.hosted.address.com --profile dev --resourcezone my.hosted.address.com. --ttl 30 --type A --target 10.10.10.9
```

## Update A resource
```bash
$ ./main.py --zone us-east-1 --action UPSERT --dns node02.teste.my.hosted.address.com --profile dev --resourcezone my.hosted.address.com. --ttl 30 --type A --target 10.10.10.10
```

## Create CNAME resource
```bash
$ ./main.py --zone us-east-1 --action CREATE --dns node02.teste.my.hosted.address.com --profile dev --resourcezone my.hosted.address.com. --ttl 30 --type CNAME --target my.address.com
```

## Update CNAME resource
```bash
$ ./main.py --zone us-east-1 --action UPSERT --dns node02.teste.my.hosted.address.com --profile dev --resourcezone my.hosted.address.com. --ttl 30 --type CNAME --target my.another.address.com
```

## DELETE resource
```bash
$ ./main.py --zone us-east-1 --action DELETE --dns node02.teste.my.hosted.address.com --profile dev --resourcezone my.hosted.address.com.
```

### Author: Gabriel Martins Andrade <gabrielandrade21@hotmail.com>