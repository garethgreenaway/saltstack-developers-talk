recycle-kubernetes-deployments:
  schedule.present:
    - function: state.sls 
    - job_args:
        - kubernetes
    - seconds: '30'
    - maxrunning: 1

