from django.contrib.auth.backends import ModelBackend
from users.models import CustomUser
import uuid

class CustomAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username:
            try:
                try:
                    uuid_obj = uuid.UUID(username)
                    user = CustomUser.objects.get(uuid=uuid_obj)
                except ValueError:
                    user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return None

            if user.check_password(password):
                return user
        return None