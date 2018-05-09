#!py

def run():

    kwargs = {'red': 255,
              'blue': 0,
              'green': 0,
              }

    return {
        'invalid_login': {
            'local.blinkt.all_rgb': [
                {'tgt': data['id']},
                {'kwarg': kwargs},
            ]
        }
    }

