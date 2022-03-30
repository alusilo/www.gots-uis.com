import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from config.storage import OverwriteStorage


def post_image_filename(instance, file):
    filename, extension = file.split('.')
    return 'user/{}.{}'.format(instance.pk, extension)


class UserManager(BaseUserManager):
    """
    creating a manager for a custom user model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example
    """
    def create_user(self, email, username, password=None):
        """
        Create and return a `User` with an email, username and password.
        """
        if not email:
            raise ValueError('Users Must Have an email address')

        if not username:
            raise ValueError('Users Must Have an username')

        user = self.model(
            username=username.lower(),
            email=self.normalize_email(email).lower(),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email.lower(), username, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    PROFESSOR = 0
    ASSOCIATED_PROFESSOR = 1
    ASSISTANT_PROFESSOR = 2
    POSTDOC = 3
    PHD_STUDENT = 4
    MSC_STUDENT = 5
    BSC_STUDENT = 6
    SUPPORT_STAFF = 7
    GUEST = 8

    ROLE_CHOICES = (
        (PROFESSOR, 'Profesor'),
        (ASSOCIATED_PROFESSOR, 'Profesor Asociado'),
        (POSTDOC, 'Investigador Postdoctoral'),
        (PHD_STUDENT, 'Estudiante de Doctorado'),
        (MSC_STUDENT, 'Estudiante de Maestría'),
        (BSC_STUDENT, 'Estudiante de Pregrado'),
        (SUPPORT_STAFF, 'Staff de Soporte'),
        (GUEST, 'Estudiante Invitado')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=45, null=True, blank=True)
    last_name = models.CharField(max_length=45, null=True, blank=True)
    username = models.CharField(verbose_name='username', max_length=45, unique=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=13, null=True, blank=True)
    office_number = models.CharField(verbose_name='office number', max_length=10, null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    picture = models.ImageField('Foto', upload_to=post_image_filename, storage=OverwriteStorage(), null=True)
    school = models.CharField(max_length=45)
    description = models.TextField(max_length=200)
    html_page = models.TextField(blank=True)
    email = models.EmailField(verbose_name='email address', max_length=45, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        """
        to set table name in database
        """
        db_table = "user"
