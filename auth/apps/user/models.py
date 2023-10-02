from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from slugify import slugify
import os, re, json, uuid
from core.producer import producer

# Create your models here.

class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        def create_slug(username):
            pattern_special_characters = r'\badmin\b|[!@#$%^~&*()_+-=[]{}|;:",.<>/?]|\s'

            if re.search(pattern_special_characters, username):
                raise ValueError('Username contains invalid characters')
            username = re.sub(pattern_special_characters, '', username)
            return slugify(username)

        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        extra_fields['slug'] = create_slug(extra_fields['username'])
        user = self.model(email=email, **extra_fields)
        user.set_password = password
        user.save(using=self._db)

        # Gửi yêu cầu HTTP tới microservice Cart chứa dữ liệu người dùng để microservice giỏ hàng có thể tạo giỏ hàng cho người dùng này

        item = {'id': str(user.id), 'email': user.email, 'username': user.username}
        producer.produce(
            os.environ.get('KAFKA_TOPIC'),
            key='create_user',
            value=json.dumps(item).encode('utf-8') # Điều này tuần tự hóa item từ điển thành một chuỗi JSON
        )
        producer.flush() # Điều này xóa mọi tin nhắn đang chờ xử lý trong nhà sản xuất
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.role = 'Admin'
        user.verified = True
        user.become_seller = True
        user.save(using=self._db)

        return user

    


class UserAccount(AbstractBaseUser, PermissionsMixin):
    roles = (
        ('customer', 'Customer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('helper', 'Helper'),
        ('editor', 'Editor'),
        ('owner', 'Owner'),

    )

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True)  # unique=True Dam bao tinh duy nhat cua cac gia tri, primary_key=True truong nay se la khoa chinh cua mo hinh
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    role = models.CharField(max_length=20, choices=roles, default='customer')
    verified =  models.BooleanField(default=False)
    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        counter = 1
        while UserAccount.objects.filter(slug=self.slug).exists():
            self.slug = f"{self.slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)


    def __str__(self):
        return self.email
