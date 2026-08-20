from django.contrib import admin

# Register your models here.

# 管理画面で使用するモデルを読み込む
from .models import (
    Artist,
    LiveVenue,
    LiveSchedule,
    OpponentArtist,
    FavoriteArtist,
    LiveRecord,
    RecordPhoto,
    SetList,
)

# アーティストを管理画面に登録する
admin.site.register(Artist)

# ライブ会場を管理画面に登録する
admin.site.register(LiveVenue)

# ライブ予定を管理画面に登録する
admin.site.register(LiveSchedule)

# 対バンアーティストを管理画面に登録する
admin.site.register(OpponentArtist)

# お気に入りアーティストを管理画面に登録する
admin.site.register(FavoriteArtist)

# ライブ記録を管理画面に登録する
admin.site.register(LiveRecord)

# ライブ記録の写真を管理画面に登録する
admin.site.register(RecordPhoto)

# セットリストを管理画面に登録する
admin.site.register(SetList)