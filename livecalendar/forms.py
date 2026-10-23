# 新規登録フォームとログインフォームを使えるようにする
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Djangoのユーザー情報を扱うUserモデルを使えるようにする
from django.contrib.auth.models import User

# Djangoのモデルを使ったフォームを作成するために読み込む
from django import forms

# ライブ予定・ライブ記録・記録写真.セットリストのモデルを読み込む
from .models import LiveSchedule, LiveRecord, RecordPhoto, SetList, Profile

from django.forms import modelformset_factory

# ファイル入力欄の表示を日本語にするために読み込む
from django.forms.widgets import ClearableFileInput



# メールアドレスでログインするためのフォーム
class EmailLoginForm(AuthenticationForm):

    # ログイン画面の入力欄をメールアドレスにする
    username = forms.EmailField(
        label="メールアドレス",
        widget=forms.EmailInput(
            attrs={"autocomplete": "email"}
        )
    )

    # 入力されたメールアドレスからユーザーを探す
    def clean(self):
        email = self.cleaned_data.get("username")

        if email:
            # メールアドレスが一致するユーザーを取得する
            users = User.objects.filter(email__iexact=email)

            # 同じメールアドレスのユーザーが1人だけの場合
            if users.count() == 1:
                self.cleaned_data["username"] = users.first().username

        # Django標準のパスワード認証を実行する
        return super().clean()


# 新規登録フォームを作成
class SignupForm(UserCreationForm):

    # パスワードの項目名を日本語にする
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput
    )

    # パスワード確認用の項目名を日本語にする
    password2 = forms.CharField(
        label="パスワード（確認用）",
        widget=forms.PasswordInput
    )

    # フォームの設定
    class Meta:

        # ユーザー情報を保存するモデルを指定
        model = User

        # 新規登録画面で使用する入力項目
        fields = ("username", "email", "password1", "password2")

        # 新規登録画面の項目名を日本語にする
        labels = {
            "username": "ユーザー名",
            "email": "メールアドレス",
        }

    # メールアドレスの重複をチェックする
    def clean_email(self):

        # 入力されたメールアドレスを取得する
        email = self.cleaned_data.get("email")

        # メールアドレスの前後の空白を削除する
        email = email.strip()

        # 同じメールアドレスが登録されているか確認する
        if User.objects.filter(email__iexact=email).exists():

            # すでに登録されている場合はエラーにする
            raise forms.ValidationError(
                "このメールアドレスはすでに登録されています。"
            )

        # 問題がなければメールアドレスを返す
        return email


 # ライブ予定を登録するフォームを作成
class LiveScheduleForm(forms.ModelForm):


    # 対バンアーティストを入力する欄
    opponent_artists = forms.CharField(
        required=False,
        label="対バンアーティスト"
                    )

    # フォームの設定
    class Meta:
            
        # LiveScheduleモデルに入力内容を保存
        model = LiveSchedule

        # ライブ予定登録画面で入力する項目
        fields = (
            "event_date",
            "artist",
            "festival_name",
            "event_name",
            "open_time",
            "start_time",
            "venue",
            "memo",
        )

        # 各入力項目の表示名を日本語にする
        labels = {
            "event_date": "公演日",
            "artist": "アーティスト名",
            "festival_name": "フェス名",
            "event_name": "公演名",
            "open_time": "開場時間",
            "start_time": "開演時間",
            "venue": "会場",
            "memo": "メモ",
        }


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

        # 入力項目の表示名を日本語にする
        labels = {
            "emotion": "感情",
            "impression": "感想",
            "is_favorite": "お気に入り",
        }


# 写真選択欄の英語表示を日本語に変更する
class JapaneseClearableFileInput(ClearableFileInput):
    initial_text = "現在"
    input_text = "変更"
    clear_checkbox_label = "削除"


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

        # 写真の表示名を日本語にする
        labels = {
            "photo": "写真",
        }

        # ファイル選択欄の表示を日本語にする
        widgets = {
            "photo": JapaneseClearableFileInput()
        }

# 写真を最大3枚まで入力できるようにする
RecordPhotoFormSet = modelformset_factory(
    RecordPhoto,
    form=RecordPhotoForm,
    extra=3,
    max_num=3,
    validate_max=True,
)

# セットリストを入力するフォーム
class SetListForm(forms.ModelForm):

    # フォームの設定
    class Meta:

        # SetListモデルに入力内容を保存
        model = SetList

        # 入力する項目
        # 曲順は自動で設定するため、曲名だけ入力する
        fields = (
            "song_name",
        )

        # セットリストの表示名を日本語にする
        labels = {
            "song_name": "曲名",
        }


# セットリストを複数曲入力できるようにする
SetListFormSet = modelformset_factory(
    SetList,
    form=SetListForm,
    extra=3,
    can_delete=True
)


# プロフィール画像を登録・変更するためのフォーム
class ProfileForm(forms.ModelForm):

    # フォームの設定
    class Meta:

        # Profileモデルを使用する
        model = Profile

        # プロフィール画像だけを編集できるようにする
        fields = ("profile_image",)