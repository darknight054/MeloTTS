

if __name__ == '__main__':

    from melo.api import TTS
    device = 'auto'
    models = {
        'EN': TTS(language='EN', device=device),
    }