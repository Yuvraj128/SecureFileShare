from cryptography.fernet import Fernet
import base64
import logging
import traceback
from django.conf import settings

def encrypt(txt):
    
    """
    This is for encrypting the file id.
    
    """
    
    txt = str(txt)
    cipher_suite = Fernet(settings.ENCRYPT_KEY)
    encrypted_text = cipher_suite.encrypt(txt.encode('ascii'))
    encrypted_text = base64.urlsafe_b64encode(encrypted_text).decode("ascii") 
    return encrypted_text


def decrypt(txt):
    
    """
    This is for decrypting the ecrypted the file id to its original form.
    
    """
    
    txt = base64.urlsafe_b64decode(txt)
    cipher_suite = Fernet(settings.ENCRYPT_KEY)
    decoded_text = cipher_suite.decrypt(txt).decode("ascii")     
    return decoded_text