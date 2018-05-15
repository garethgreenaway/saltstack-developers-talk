# nginx deployment as specified inside of sls file
#        replicas: {{ range(2, 40) | random }}
my-nginx:
  kubernetes.deployment_present:
    - namespace: default
      spec:
        replicas: {{ range(2, 40) | random }}
        template:
          metadata:
            labels:
              run: my-nginx
          spec:
            containers:
            - name: my-nginx
              image: garethgreenaway/nginx:latest
              ports:
              - containerPort: 80
