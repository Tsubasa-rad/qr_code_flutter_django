from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid


# データベースの構造の定義

class UserManager(BaseUserManager):
    # 新規のユーザーの設定（email、password）
    def create_user(self, email, password=None):
        if not email:
            # emailがない時のエラー処理
            raise ValueError('email is must')
        # emailの正規化を行う
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    # スーパーユーザー
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# userモデル
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


# プロフィールクラス
class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickName = models.CharField(max_length=20)
    userProfile = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='userProfile',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    login_on = models.BooleanField(default=False)

    def __str__(self):
        return self.nickName


# Loginクラス
class LoginData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userLogin = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userLogin',
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.id