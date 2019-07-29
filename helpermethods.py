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
        usePreviousTemplate = True
        if templateBody is not None: 
            with open(templateBody, 'r') as readFile:
                templateBodyString = readFile.read()

            usePreviousTemplate = False

        else:
            templateBodyString = self.client.get_template(StackName=currentStackId)
  
        templateSummary = self.client.get_template_summary(TemplateBody=templateBodyString["TemplateBody"])

        templateParameters = templateSummary["Parameters"]
        currentStackParameters = currentStack["Stacks"][0]["Parameters"]

        stackParams = []
        for i in range(len(templateParameters)):

            if templateParameters[i]["ParameterKey"] in params.keys():
                
                lTemplateParameters = templateParameters[i]
                matchedParams = params[lTemplateParameters["ParameterKey"]]

                param = {
                        "ParameterKey": templateParameters[i]["ParameterKey"],
                        "ParameterValue": "",
                        "UsePreviousValue": True
                }

                for j in range(len(currentStackParameters)):

                    if currentStackParameters[j]["ParameterKey"] == lTemplateParameters["ParameterKey"] and currentStackParameters[j]["ParameterValue"] != matchedParams :

                        param = {
                            "ParameterKey": templateParameters[i]["ParameterKey"],
                            "ParameterValue": matchedParams,
                            "UsePreviousValue": False
                        }
                        break

                stackParams.append(param)

            else:

                param = {
                    "ParameterKey": templateParameters[i]["ParameterKey"],
                    "ParameterValue": "",
                    "UsePreviousValue": True
                }
                
                stackParams.append(param)
        
        templateBodyString = templateBodyString["TemplateBody"]
        response = None

        if usePreviousTemplate :

            response = self.client.update_stack(
                StackName=stackName,
                Parameters=stackParams,
                UsePreviousTemplate=True,
                Capabilities=["CAPABILITY_IAM"]
            )

        else :

            response = self.client.update_stack(
                StackName=stackName,
                Parameters=stackParams,
                TemplateBody=templateBodyString,
                UsePreviousTemplate=Fals,
                Capabilities=["CAPABILITY_IAM"]
            )
        
        print(response)

    def copy(self):
        print("bah")

