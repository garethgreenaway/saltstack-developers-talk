#
# message of the day
#

{% set film_id = '1' %}

/etc/motd:
  file.managed:
    - contents: "{{ salt['swapi.films'](film_id)['opening_crawl'] }}"

