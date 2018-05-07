salt-minion:
  kubernetes.deployment_present:
    - namespace: default
      spec:
        replicas: 0
        template:
          metadata:
            generateName: salt-minion-
            labels:
              run: salt-minion
          spec:
            hostAliases:
            - ip: '192.168.0.12'
              hostnames:
              - 'salt'
            containers:
            - name: salt-minion
              image: garethgreenaway/ubuntu_systemd_saltminion:latest
              securityContext:
                privileged: True
                allowPrivilegeEscalation: True
