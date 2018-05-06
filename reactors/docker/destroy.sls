#!py


def run():

    kwargs = {'start': 6,
              'end': 7,
              'red': 255,
              'blue': 255,
              'green': 0,
              'timeout': 5}

    return {
        'docker_destroy': {
            'local.blinkt.range_rgb': [
                {'tgt': data['id']},
                {'kwarg': kwargs},
            ]
        }
    }
