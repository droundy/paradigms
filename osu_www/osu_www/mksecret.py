import os

def generate_secret_key (filepath):
    from django.core.management.utils import get_random_secret_key

    key = get_random_secret_key()
    secret_file = open(filepath, "w")
    secret = "SECRET_KEY= " + "\""+ key + "\"" + "\n"
    secret_file.write(secret)
    secret_file.close()
    return key

def get_secret_key():
    try:
        from .secret_key import SECRET_KEY
        return SECRET_KEY
    except:
        SETTINGS_DIR = os.path.abspath(os.path.dirname(__file__))
        return generate_secret_key(os.path.join(SETTINGS_DIR, 'secret_key.py'))
