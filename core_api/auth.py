import datetime
import jwt

from django.conf import settings
from functools import wraps

from django.contrib.auth.models import User
from django.http import JsonResponse

def generate_token(user):
    payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm="HS256",
    )

    return token


def verify_token(token):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
        )

        return payload

    except jwt.ExpiredSignatureError:
        return None

    except jwt.InvalidTokenError:
        return None


def jwt_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return JsonResponse(
                {
                    "error": "Authorization header is required."
                },
                status=401,
            )

        if not auth_header.startswith("Bearer "):
            return JsonResponse(
                {
                    "error": "Invalid authorization header."
                },
                status=401,
            )

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"],
            )

            request.user = User.objects.get(id=payload["user_id"])

        except jwt.ExpiredSignatureError:
            return JsonResponse(
                {
                    "error": "Token has expired."
                },
                status=401,
            )

        except jwt.InvalidTokenError:
            return JsonResponse(
                {
                    "error": "Invalid token."
                },
                status=401,
            )

        except User.DoesNotExist:
            return JsonResponse(
                {
                    "error": "User not found."
                },
                status=401,
            )

        return view_func(request, *args, **kwargs)

    return wrapper