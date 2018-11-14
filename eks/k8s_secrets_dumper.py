"""
Python 3
Script to dump Kubernetes Secrets
pip install kubernetes

Ensure that kubectl is configured to your cluster by running
kubectl config current-context
"""
from base64 import b64decode
from kubernetes import client, config


def k8s_secret_dumper():
    config.load_kube_config()
    v1 = client.CoreV1Api()
    ret = v1.list_secret_for_all_namespaces(watch=False)
    for elm in ret.items:
        print(f'Name: {elm.metadata.name} in Namespace: {elm.metadata.namespace}')
        print("==============================SECRETS============================")
        for key, value in elm.data.items():
            print(f'Key: {key}\nDecoded Secret: {b64decode(value).decode()}\n')
        print("=================================================================\n")

if __name__ == "__main__":
    print("k8s_secret_dumper: Script for dumping Kubernetes Secrets - Ajin Abraham\n")
    k8s_secret_dumper()