clear-out-my-nginx-pods:
  kubernetes.deployment_present:
    - name: my-nginx
    - namespace: default
      spec:
        replicas: 0
        template:
          metadata:
            labels:
              run: nginx
          spec:
            containers:
            - name: my-nginx
              image: nginx

delete-my-nginx-deployment:
  kubernetes.deployment_absent:
    - name: my-nginx
    - require:
      - kubernetes: clear-out-my-nginx-pods
