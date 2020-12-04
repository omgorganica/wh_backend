from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.conf import settings

'''
Custom user manager
'''


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


'''
Custom user model
'''


class User(AbstractUser):

    username = None

    wms_id = models.CharField(max_length=5, blank=False, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=False, unique=True)
    current_balance = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', default='None')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['wms_id']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.wms_id} '


class FileUploader(models.Model):
    file = models.FileField(upload_to='files/', default='None')
    upload_date = models.DateTimeField(auto_now=True, db_index=True)


class ShiftResult(models.Model):
    date = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shift_results')
    picking = models.IntegerField()
    transportations = models.IntegerField()
    loading = models.IntegerField()
    result = models.DecimalField(max_digits=3, decimal_places=1, default=0)

    def __str__(self):
        return f'{self.date} {self.user} '


class Good(models.Model):
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/', default='None')

    def __str__(self):
        return f'{self.name} {self.price}'


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    good = models.ForeignKey(Good, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f'{self.user} {self.good}'


class BalanceModifier(models.Model):
    name = models.CharField(max_length=255)
    delta = models.IntegerField()
    image = models.ImageField(upload_to='images/', default='None')
    for_shift_result = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.delta}'


class BalanceModifierHistory(models.Model):
    User = get_user_model()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_to')
    assigned_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='assigned_by', null=True)
    modifier = models.ForeignKey(BalanceModifier, on_delete=models.CASCADE)
    comment = models.TextField(max_length=300, blank=True)

    def __str__(self):
        return f'{self.assigned_to} {self.modifier}'
