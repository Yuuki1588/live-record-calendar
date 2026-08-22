# Djangoのユーザー新規登録フォームを使えるようにする
from django.contrib.auth.forms import UserCreationForm

# Djangoのユーザー情報を扱うUserモデルを使えるようにする
from django.contrib.auth.models import User


# 新規登録フォームを作成
class SignUpForm(UserCreationForm):

    # フォームの設定
    class Meta:

        # ユーザー情報を保存するモデルを指定
        model = User

        # 新規登録画面で使用する入力項目
        fields = ("username", "email", "password1", "password2")