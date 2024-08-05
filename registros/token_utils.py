from django.conf import settings
from itsdangerous import URLSafeSerializer


def generate_token(user_id):
    serializer = URLSafeSerializer(settings.SECRET_KEY)
    return serializer.dumps(user_id, salt=settings.SECRET_KEY)


def verify_token(token, max_age=3600):
    serializer = URLSafeSerializer(settings.SECRET_KEY)
    try:
        user_id = serializer.loads(token, salt=settings.SECRET_KEY, max_age=max_age)
    except Exception:
        return None
    return user_id
