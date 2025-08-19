# How-to guide

## 1. Deploy prometheus
```shell
kubectl create ns monitoring
helm upgrade --install kube-prometheus ../infra/kube-prometheus
```

If your `node-exporter` pod is `Pending`, it's probably because of another `node-exporter` exists in the cluster, for example, in the namespace `knative-monitoring`. Please remove all of this to fix the problem. The easiest way to delete anothe `node-exporter` in `knative-monitoring` is to delete the whole cluster with the following command `kubectl delete ns knative-monitoring`.

## 2. Deploy the mm-operator

Build and push the operator image
```shell
bash build.sh
```

Create a new ServiceAccount with its rolebindings
```shell
kubectl apply -f role.yaml
```

Create the operator
```shell
kubectl apply -f mm_controller.yaml
```
