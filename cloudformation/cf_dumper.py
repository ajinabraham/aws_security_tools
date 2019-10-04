"""
Python 3
Script to dump CloudFormation templates
aws configure

configure your AWS credentials
you should have permission for listing and downloading CloudFormation stacks
"""
import os
import boto3
import requests
import yaml
import shutil
from cfn_flip import to_json


class CFNDumper:

    def __init__(self, out_dir):
        self.out_dir = out_dir
        self.client = boto3.client('cloudformation')
        self.cf_templates = []

    def get_cfns(self):
        res = self.client.list_stacks(
            StackStatusFilter=['UPDATE_COMPLETE'])
        self.cf_templates = [f["StackName"] for f in res["StackSummaries"]]

    def get_templates(self):
        for stack in self.cf_templates:
            out = self.client.get_template(
                StackName=stack,
                TemplateStage='Processed')
            yaml_out = out['TemplateBody']
            json_out = to_json(yaml_out)
            open(f'./cf_templates/{stack}.yaml', 'w').write(yaml_out)
            open(f'./cf_templates/{stack}.json', 'w').write(json_out)

if __name__ == "__main__":
    print("CloudFormationDumper: Script for dumping CloudFormation templates - Ajin Abraham")
    out_dir = './cf_templates/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        shutil.rmtree(out_dir)
        os.makedirs(out_dir)
    cfnd = CFNDumper(out_dir)
    cfnd.get_cfns()
    cfnd.get_templates()
    print(f'[INFO] Finished Dumping CloudFormation templates to {out_dir}')
