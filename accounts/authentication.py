from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError


class RetryAndLimitAuthentications(ModelBackend):
    MAX_LOGIN_ATTEMPTS_BEFORE_LOCK = 3

    def authenticate(self, request, username=None, password=None, **kwargs):

        user = super().authenticate(request, username=username, password=password, **kwargs)

        login_attempts = request.session.get('login_attempts', 0)

        if not user:
            if login_attempts >= self.MAX_LOGIN_ATTEMPTS_BEFORE_LOCK:
                raise ValidationError('You have exceeded the number of failed password attempts.')

            request.session['login_attempts'] = login_attempts + 1
        else:
            request.session['login_attempts]'] = 0

        return user
