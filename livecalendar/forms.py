# Djangoのユーザー新規登録フォームを使えるようにする
from django.contrib.auth.forms import UserCreationForm

# Djangoのユーザー情報を扱うUserモデルを使えるようにする
from django.contrib.auth.models import User

# Djangoのモデルを使ったフォームを作成するために読み込む
from django import forms

# ライブ予定のLiveScheduleモデルを読み込む
from .models import LiveSchedule


# 新規登録フォームを作成
class SignUpForm(UserCreationForm):

    # フォームの設定
    class Meta:

        # ユーザー情報を保存するモデルを指定
        model = User

        # 新規登録画面で使用する入力項目
        fields = ("username", "email", "password1", "password2")


 # ライブ予定を登録するフォームを作成
class LiveScheduleForm(forms.ModelForm):


    # 対バンアーティストを入力する欄
    opponent_artists = forms.CharField(
        required=False,
        label="対バンアーティスト",
        help_text="例：Saucy Dog, ONE OK ROCK"
                    )

    # フォームの設定
    class Meta:
            
            # LiveScheduleモデルに入力内容を保存
        model = LiveSchedule


            # ライブ予定登録画面で入力する項目
        fields = (
            "artist",
            "festival_name",
            "event_name",
            "event_date",
            "open_time",
            "start_time",
            "venue",
            "memo",
            )


            # 日付と時間を選択できるようにする
        widgets = {
                "event_date": forms.DateInput(attrs={"type": "date"}),
                "open_time": forms.TimeInput(attrs={"type": "time"}),
                "start_time": forms.TimeInput(attrs={"type": "time"}),
            }