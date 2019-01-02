import argparse
import json
import helpermethods

parser = argparse.ArgumentParser()

parser.add_argument("--option", help="Available options: create, copy, retrieve, update")
parser.add_argument("--stackName", help="Name or id of the CloudFormation stack")
parser.add_argument("--source", help="Name or id of the CloudFormation stack to copy from")
parser.add_argument("--template", help="Path to template to update")
parser.add_argument("--timeout", help="Length of time to wait before cancelling and exiting.", type=int, default=20)

parser.add_argument("--params", help="Parameters in format of <key>=<value>", nargs="+")
parser.add_argument("--tags", help="Tags in format of <key>=<value>",nargs="+")
parser.add_argument("--execute", help="By default, only change set is created. Set this flag to execute the change set by default", type=bool, default=False,nargs="+")
parser.add_argument("--region")

args = parser.parse_args()
params = {}
tags = {}

helper = helpermethods.HelperMethods(regionName=args.region)

if args.params is not None:
    for i in range(len(args.params)):
        d = args.params[i].split(":")
        kv = {d[0]:d[1]}
        params.update(kv)
if args.tags is not None:
    for i in range(len(args.tags)):
        d = args.tags[i].split(":")
        kv = {d[0]:d[1]}
        tags.update(kv)

if args.option == "copy":
    helper.copy()
if args.option == "update":
    helper.update(stackName=args.stackName, templateBody=args.template, params=params)