from django.db import models

# Djangoのユーザー情報を使えるようにする
from django.contrib.auth.models import User

# Create your models here.

# アーティスト情報を保存するモデル
class Artist(models.Model):
    artist_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        # 管理画面などでアーティスト名を表示する
    def __str__(self):
        return self.artist_name



# ライブ会場の情報を保存するモデル
class LiveVenue(models.Model):
    venue_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        # 管理画面などでライブ会場名を表示する
    def __str__(self):
        return self.venue_name

#ライブの予定情報を保存するモデル
class LiveSchedule(models.Model):

    #この予定を登録したユーザー
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 出演するアーティスト
    artist = models.ForeignKey(
    Artist,
    on_delete=models.CASCADE,
    null=True,
    blank=True
    )

    # フェス名
    festival_name = models.CharField(
    max_length=255,
    null=True,
    blank=True
    )

    # 公演名・ツアー名
    event_name = models.CharField(
    max_length=255,
    null=True,
    blank=True
    )

    # ライブ・フェスの公演日
    event_date = models.DateField()

    # 開場時間
    open_time = models.TimeField(
    null=True,
    blank=True
    )

    # 開演時間
    start_time = models.TimeField()

    # ライブ・フェスの会場
    venue = models.ForeignKey(
    LiveVenue,
    on_delete=models.CASCADE
    )

    # ライブ予定についてのメモ
    memo = models.TextField(
    blank=True
    )

    # 登録日時
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

     # 公演名があれば公演名、なければフェス名を表示する
    def __str__(self):
        return self.event_name or self.festival_name or "名称未設定"

# 対バンアーティストを保存するモデル
class OpponentArtist(models.Model):

    # どのライブ予定の対バンなのか
    live_schedule = models.ForeignKey(
        LiveSchedule,
        on_delete=models.CASCADE
    )

    # 対バンするアーティスト
    artist = models.ForeignKey(
    Artist,
    on_delete=models.CASCADE
    )   

    # 登録日時
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

    # 管理画面などで対バンアーティスト名を表示する
    def __str__(self):
        return str(self.artist)


# お気に入りアーティストを保存するモデル
class FavoriteArtist(models.Model):

    # お気に入り登録したユーザー
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # お気に入り登録したアーティスト
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE
    )

    # 登録日時
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

     # 管理画面などでお気に入りアーティスト名を表示する
    def __str__(self):
        return str(self.artist)


# ライブ参戦後の記録を保存するモデル
class LiveRecord(models.Model):

    # どのライブ予定に対する記録なのか
    live_schedule = models.OneToOneField(
        LiveSchedule,
        on_delete=models.CASCADE
    )

    # 感情の選択肢
    EMOTION_CHOICES = [
        ("最高", "最高"),
        ("楽しかった", "楽しかった"),
        ("感動", "感動"),
        ("普通", "普通"),
        ("残念", "残念"),
    ]

    # ライブに対する感情
    emotion = models.CharField(
        max_length=20,
        choices=EMOTION_CHOICES,
    )

    # ライブの感想
    impression = models.TextField(
        blank=True
    )

    # このライブ記録がお気に入りかどうか
    is_favorite = models.BooleanField(
    default=False
    )

    # 登録日時
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

     # 管理画面などでライブ記録の公演名を表示する
    def __str__(self):
        return str(self.live_schedule)


# ライブ記録の写真を保存するモデル
class RecordPhoto(models.Model):

    # どのライブ記録の写真なのか
    live_record = models.ForeignKey(
        LiveRecord,
        on_delete=models.CASCADE
    )

    # ライブ記録の写真
    photo = models.ImageField(
    upload_to="record_photos/",
    blank=True,
    null=True
    )

    # 登録日時
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

    # 管理画面などで写真に紐づくライブ名を表示する
    def __str__(self):
        return str(self.live_record)


# セットリストを保存するモデル
class SetList(models.Model):

    # どのライブ記録のセットリストなのか
    live_record = models.ForeignKey(
        LiveRecord,
        on_delete=models.CASCADE
    )

        # 曲名
    song_name = models.CharField(
        max_length=255
    )

    # セットリスト内の曲順
    song_order = models.IntegerField()

        # 登録日時
    created_at = models.DateTimeField(auto_now_add=True)

    # 更新日時
    updated_at = models.DateTimeField(auto_now=True)

    # 管理画面などでセットリストの曲名を表示する
    def __str__(self):
        return f"{self.song_order}. {self.song_name}"