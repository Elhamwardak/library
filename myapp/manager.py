from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class CutomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        if not username or username is None:
            raise ValidationError("User must have username")
        if not email or email is None:
            raise ValidationError("User must have email address")
        extra_fields['email'] = self.normalize_email(email)
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, email="admin@gmail.com", **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('group_id', 1)

        return self.create_user(username, email, password , **extra_fields)