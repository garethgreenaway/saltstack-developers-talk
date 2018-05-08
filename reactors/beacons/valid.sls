#!py

def run():

    kwargs = {'r': 0,
              'b': 0,
              'g': 255,
              }

    return {
        'valid_login': {
            'local.blinkt.all_rgb': [
                {'tgt': data['id']},
                {'kwarg': kwargs},
            ]
        }
    }

