import random
import string

def generate_invite_code(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=length))
