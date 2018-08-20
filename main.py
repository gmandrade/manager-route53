#!/usr/bin/env python3.5

import boto3, sys, argparse
from pprint import pprint
from botocore.errorfactory import ClientError
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser(description='Manager Route53')
required_argument = parser.add_argument_group('required arguments')

required_argument.add_argument(
    '--profile',
    help="aws cli profile in you machine",
    type=str, 
	required=True
)

required_argument.add_argument(
    '--zone',
    help="zone in AWS",
    type=str, 
	required=True
)

required_argument.add_argument(
    '--action',
    help="action in route53",
    type=str, 
	required=True
)

parser.add_argument(
    '--resourcezone',
    help="resource zone DNS if you want to manipulate",
    type=str
)

parser.add_argument(
    '--dns',
    help="source dns",
    type=str
)

parser.add_argument(
    '--type',
    help="type of resource",
    type=str
)

parser.add_argument(
    '--ttl',
    help="time to live for your dns",
    type=int
)

parser.add_argument(
    '--target',
    help="target dns",
    type=str
)

args  = parser.parse_args()

try:
	session =  boto3.Session(profile_name=args.profile)
	client = session.client(
		service_name="route53",
		region_name = args.zone,
	)

except Exception as error:
	print("ERRO - %s " % str(error))
	sys.exit(1)
	
try:
	list_zones = client.list_hosted_zones()
except Exception as error:
	print("ERRO - %s " % str(error))
	sys.exit(1)

zones_dict = {}
zones_arr = []
for hosts in list_zones["HostedZones"]:
	zones    = hosts["Name"]
	zones_id = hosts["Id"]
	zones_arr.append(zones)
	zones_dict.update({zones:zones_id})

if args.action != "GETZONES":
	if args.resourcezone not in zones_dict.keys():
		print("\nERRO - %s is not in HostedZones\n" % args.resourcezone)
		print("Available Zones :")
		pprint(zones_arr)
		print("\n")
		sys.exit(1)

action_list = ["GETZONES", "GET", "CREATE", "DELETE", "UPSERT"]

if args.action not in action_list:
	print("\nERRO - %s is not in Action List\n" % args.action)
	sys.exit(1)

if args.action == "GETZONES":
	print("\nZones:")
	pprint(zones_arr)
	print("\n")

elif args.action == "GET":
	select_zone_id = zones_dict.get(args.resourcezone)

	try: 
		list_resource = client.list_resource_record_sets(
			HostedZoneId=select_zone_id
		)
	except Exception as error:
		print("\nERRO - %s\n" % error)
		sys.exit(1)

	record_sets_name = [i["Name"] for i in list_resource["ResourceRecordSets"]]
	print("\nRecord Sets:")
	pprint(record_sets_name)

elif args.action == "CREATE" or args.action == "UPSERT":

	try: 
		action_resource = client.change_resource_record_sets(
			HostedZoneId=zones_dict.get(args.resourcezone),
			ChangeBatch={
				"Changes":[{
					'Action': args.action,
					'ResourceRecordSet': {
						'Name': args.dns,
						'Type': args.type,
						'TTL': args.ttl,
						'ResourceRecords': [{'Value': args.target}]
					}
				}]
			}
		)

		print("\nINFO - Record successfully updated/created\n")
		sys.exit(0)

	except ClientError as error:
		if "but it already exists" in str(error):
			print("\nERROR - resource already exists\n")
		elif "ARRDATAIllegalIPv4Address" in str(error):
			print("\nERROR - invalid ipv4\n")
		elif "InvalidInput" in str(error):
			print("\nERROR - invalid type of dns\n")
		sys.exit(1)

	except Exception as error:
		print("\nERRO - %s\n" % error)
		sys.exit(1)

elif args.action == "DELETE":

	try:
		record = client.list_resource_record_sets(
			HostedZoneId=zones_dict.get(args.resourcezone),
			StartRecordName=args.dns
		)
	except Exception as error:
		print("\nERRO - %s\n" % error)
		sys.exit(1)

	for resource in record["ResourceRecordSets"]:
		name = resource["Name"]
		if name.replace(".","") == args.dns.replace(".",""):
			resource_type   = resource["Type"]
			resource_ttl    = resource["TTL"]
			resource_target = [i["Value"] for i in resource["ResourceRecords"]]
	try:
		action_resource = client.change_resource_record_sets(
			HostedZoneId=zones_dict.get(args.resourcezone),
			ChangeBatch={
				"Changes":[{
					'Action': args.action,
					'ResourceRecordSet': {
						'Name': args.dns,
						'Type': resource_type,
						'TTL': int(resource_ttl),
						'ResourceRecords': [{'Value': resource_target[0]}]
					}
				}]
			}
		)

		print("\nINFO - Record successfully deleted\n")
		sys.exit(0)

	except NameError as error:
		print("\nERRO - DNS not found\n")
		sys.exit(1)

	except Exception as error:
		print("\nERRO - %s\n" % error)
		sys.exit(1)