recycle-kubernetes-deployments:
  schedule.present:
    - function: state.sls 
    - job_args:
        - states.kubernetes
    - seconds: '30'
    - maxrunning: 1

