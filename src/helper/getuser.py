from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

def get_user_from_token(token_key):
    try:
        token = Token.objects.get(key=token_key)
        user = token.user
        return user
    except Token.DoesNotExist:
        return None
