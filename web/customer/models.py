from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class CustomerManager(BaseUserManager):
    def create_user(self, phone_number, name_customer, date_of_birth, gt, password=None):
        if not phone_number:
            raise ValueError('phone number is required')
        if not name_customer:
            raise ValueError('name is required')
        if not date_of_birth:
            raise ValueError('date of birth is required')
        if not gt:
            raise ValueError('is required')

        user=self.model(
            phone_number=phone_number,
            name_customer=name_customer,
            date_of_birth=date_of_birth,
            gt=gt
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name_customer, date_of_birth, gt, password=None):
        user=self.create_user(
            phone_number=phone_number,
            name_customer=name_customer,
            date_of_birth=date_of_birth,
            gt=gt,
            password=password
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser):
    phone_number = models.CharField(max_length=10, default='', primary_key=True)
    name_customer = models.CharField(max_length=100, default='')
    date_of_birth = models.CharField(max_length=10, default='')
    gt = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True, null=True)
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name_customer', 'date_of_birth', 'gt']

    object=CustomerManager()

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True