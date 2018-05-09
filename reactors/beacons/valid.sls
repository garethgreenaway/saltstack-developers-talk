#!py

def run():

    kwargs = {'red': 0,
              'blue': 0,
              'green': 255,
              }

    return {
        'valid_login': {
            'local.blinkt.all_rgb': [
                {'tgt': data['id']},
                {'kwarg': kwargs},
            ]
        }
    }

