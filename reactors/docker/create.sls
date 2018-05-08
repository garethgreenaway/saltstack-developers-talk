#!py


def run():

    kwargs = {'start': 0,
              'end': 1,
              'red': 0,
              'blue': 255,
              'green': 0,
              'timeout': 30}

    return {
        'docker_destroy': {
            'local.blinkt.range_rgb': [
                {'tgt': data['id']},
                {'kwarg': kwargs},
            ]
        }
    }
