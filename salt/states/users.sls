#
# add users
#

{% set user = salt['swapi.people'](10) %}
{% set username_parts = user['name'].lower().split(' ') %}
{% set username = username_parts[0].first() + username_parts[1] %}

{{ username }}:
  user.present:
    - fullname: {{ user['name'] }}
