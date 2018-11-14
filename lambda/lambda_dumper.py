"""
Python 3
Script to dump AWS Lambda functions
pip install boto3 requests
aws configure

configure your AWS credentials
you should have permission for listing and downloading Lambda functions
"""
import os
import boto3
import requests
import zipfile
import shutil


class LambdaDumper:

    def __init__(self, out_dir):
        self.out_dir = out_dir
        self.client = boto3.client('lambda')
        self.funcs = []

    def get_lambda_functions(self):
        res = self.client.list_functions(
            FunctionVersion='ALL',
            MaxItems=1000
        )
        self.funcs = [f["FunctionName"] for f in res["Functions"]]

    def download_functions(self):
        for func in self.funcs:
            print(f'[INFO] - Downloading Function: {func}')
            response = self.client.get_function(
                FunctionName=func,
            )
            url = response["Code"]["Location"]
            lang = response["Configuration"]["Runtime"]
            r = requests.get(url, allow_redirects=True)
            path = os.path.join(self.out_dir, f'{func}_{lang}.zip')
            open(path, 'wb').write(r.content)

    def unzip_files(self):
        for item in os.listdir(self.out_dir):
            print(f'[INFO] Unzipping: {item}')
            if item.endswith(".zip"):
                file_name = os.path.join(self.out_dir, item)
                out_func_dir = os.path.join(
                    self.out_dir, item.replace(".zip", "", -1))
                with zipfile.ZipFile(file_name) as zip_ref:
                    zip_ref.extractall(out_func_dir)
                os.remove(file_name)

if __name__ == "__main__":
    print("LambdaDumper: Script for dumping AWS Lambda Functions - Ajin Abraham")
    out_dir = './lambda_functions/'
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    else:
        shutil.rmtree(out_dir)
        os.makedirs(out_dir)
    lmdump = LambdaDumper(out_dir)
    funcs = lmdump.get_lambda_functions()
    lmdump.download_functions()
    lmdump.unzip_files()
    print(f'[INFO] Finished Dumping Lambda Functions to {out_dir}')
