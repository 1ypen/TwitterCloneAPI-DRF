from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, login, name, password=None):
        """
        Creates and saves a User with the given email, login
        bane and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        if not login:
            raise ValueError('Users must have an login')

        user = self.model(
            email=self.normalize_email(email),
            login=login,
            name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, login, password=None):
        """
        Creates and saves a superuser with the given email, name
        login and password.
        """
        user = self.create_user(
            email,
            name=name,
            login=login,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    name = models.CharField(max_length=125)
    email = models.EmailField()
    login = models.CharField(max_length=125, unique=True)
    about = models.CharField(max_length=160, blank=True, null=True)
    avatar = models.ImageField(upload_to='images/avatars', blank=True, null=True)
    cover = models.ImageField(upload_to='images/covers', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Relationship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followings')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
