/etc/salt/minion.d/engines.conf:
  file.managed:
    - source: salt://states/salt/engines.conf
    - user: root
    - group: root
    - mode: 644
