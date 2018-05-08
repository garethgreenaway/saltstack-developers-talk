#!py

def run():

    kwargs = {'r': 255,
              'b': 0,
              'g': 0,
              }

    return {
        'invalid_login': {
            'local.blinkt.all_rgb': [
                {'tgt': data['id']},
                {'kwarg': kwargs},
            ]
        }
    }

