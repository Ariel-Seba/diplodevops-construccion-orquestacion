
```
k3d cluster create diplodevops-lab12 --config 12-k3d-setup-lab.yaml --kubeconfig-switch-context
k3d kubeconfig write diplodevops-lab12

alias update-k8s-diplo-06='export KUBECONFIG=$HOME/.config/k3d/kubeconfig-diplodevops-lab12.yaml'
alias unset-k8s-diplo-06='unset KUBECONFIG'

```



```
k3d cluster delete diplodevops-lab12
```