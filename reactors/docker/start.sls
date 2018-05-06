#!py


def run():

    work = {}

    kwargs = {'start': 2,
              'end': 3,
              'red': 0,
              'blue': 0,
              'green': 255,
              'timeout': 20}

    work['docker_start'] = {
        'local.blinkt.range_rgb': [
            {'tgt': data['id']},
            {'kwarg': kwargs},
        ]
    }

    return work
