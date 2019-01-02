import boto3
import botocore
import json

class HelperMethods:

    client = None

    def __init__(self, regionName):
        self.client = boto3.client('cloudformation', regionName)

    def update(self, stackName, templateBody, params):

        currentStack = self.client.describe_stacks(StackName=stackName)
        currentStackId = currentStack["Stacks"][0]["StackId"]

        templateBodyString = ""
        if templateBody is not None: 
            with open(templateBody, 'r') as readFile:
                templateBodyString = readFile.read()
        else:
            templateBodyString = self.client.get_template(StackName=currentStackId)
  
        tempSummary = self.client.get_template_summary(TemplateBody=templateBodyString["TemplateBody"])
        tempSummaryParams = tempSummary["Parameters"]
        
        currentStackParameters = currentStack["Stacks"][0]["Parameters"]

        stackParams = []
        for i in range(len(tempSummaryParams)):
            if tempSummaryParams[i]["ParameterKey"] in params.keys():

                paramsValue = params[tempSummaryParams[i]["ParameterKey"]]
                currentStackParameterValue = currentStackParameters[0]
                
                print (paramsValue)
                print (currentStackParameterValue)
                print (currentStackParameterValue.keys())

                if paramsValue == currentStackParameterValue :
                    param = {
                        "ParameterKey": tempSummaryParams[i]["ParameterKey"],
                        "ParameterValue": None,
                        "UsePreviousValue": False
                    }

                param = {
                    "ParameterKey": params[tempSummaryParams[i]["ParameterKey"]],
                    "ParameterValue": params[tempSummaryParams[i]["ParameterKey"]],
                    "UsePreviousValue": False
                }
                stackParams.append(param)
            else:    
                param = {
                    "ParameterKey": tempSummaryParams[i]["ParameterKey"],
                    "ParameterValue": None,
                    "UsePreviousValue": False
                }
                stackParams.append(param)
            

    def copy(self):
        print("bah")

