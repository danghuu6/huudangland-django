from django.contrib.auth.backends import BaseBackend
from customer.models import Customer


class LoginAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Customer.objects.get(phone_number=username)
            if password == getattr(user, 'password'):
                return user
            else:
                return None
        except Customer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None


