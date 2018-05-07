salt-minion:
  kubernetes.deployment_present:
    - namespace: default
      spec:
        replicas: {{ range(1, 8) | random }}
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
