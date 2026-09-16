from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using
    either their username or email address (case-insensitive).
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        if not username or not password:
            return None

        # Search for user by case-insensitive username or email
        try:
            user = User.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except User.DoesNotExist:
            # Run password hasher once to reduce timing difference
            User().set_password(password)
            return None
        except User.MultipleObjectsReturned:
            # If multiple users have the same email, fallback to exact username
            try:
                user = User.objects.get(username__iexact=username)
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
