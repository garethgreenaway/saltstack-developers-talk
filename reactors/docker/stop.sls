#!py


def run():

    work = {}

    kwargs = {'start': 4,
              'end': 5,
              'red': 255,
              'blue': 0,
              'green': 0,
              'timeout': 20}

    work['docker_stop'] = {
        'local.blinkt.range_rgb': [
            {'tgt': data['id']},
            {'kwarg': kwargs},
            ]
    }

    return work
