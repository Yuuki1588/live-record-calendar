# Djangoのユーザー新規登録フォームを使えるようにする
from django.contrib.auth.forms import UserCreationForm

# Djangoのユーザー情報を扱うUserモデルを使えるようにする
from django.contrib.auth.models import User

# Djangoのモデルを使ったフォームを作成するために読み込む
from django import forms

# ライブ予定・ライブ記録・記録写真.セットリストのモデルを読み込む
from .models import LiveSchedule, LiveRecord, RecordPhoto, SetList


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

# ライブ参戦後の記録を入力するフォーム
class LiveRecordForm(forms.ModelForm):

    # フォームの設定
    class Meta:

        # LiveRecordモデルに入力内容を保存
        model = LiveRecord

        # 記録画面で入力する項目
        fields = (
        "emotion",
        "impression",
        "is_favorite",
    )

# ライブ記録の写真を追加するフォーム
class RecordPhotoForm(forms.ModelForm):

    # フォームの設定
    class Meta:

        # RecordPhotoモデルに写真を保存
        model = RecordPhoto

        # 写真を選択する項目
        fields = (
            "photo",
        )

# セットリストを入力するフォーム
class SetListForm(forms.ModelForm):

    # フォームの設定
    class Meta:

        # SetListモデルに入力内容を保存
        model = SetList

        # 入力する項目
        fields = (
            "song_name",
            "song_order",
        )


from django.forms import modelformset_factory


# セットリストを複数曲入力できるようにする
SetListFormSet = modelformset_factory(
    SetList,
    form=SetListForm,
    extra=5
)