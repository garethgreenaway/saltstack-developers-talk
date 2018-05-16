#
# remove groups
#

rebels:
  group.absent

empire:
  group.absent

#
# remove users
#

{% set users = {'10': {'groups': ['rebels']},
                '4': {'groups': ['empire']}
				} %}

{% for id in users %}
{% set user = salt['swapi.people'](id) %}
{% set username_parts = user['name'].split() %}
{% set username = username_parts[0]|first|lower + username_parts[1]|lower %}

{{ username }}:
  user.absent
{% endfor %}
