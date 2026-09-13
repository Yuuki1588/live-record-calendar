from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='livecalendar/login.html'
        ),
        name='login'
    ),
    #ホーム画面を表示するためのURL
    path('home/', views.index, name='home'),

    #新規登録画面
    path('signup/',views.signup, name='signup'),
    #ログアウト
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # ライブ予定追加画面
    path('live/add/', views.live_create, name='live_create'),
    # ライブ詳細画面
    path('live/<int:schedule_id>/', views.live_detail, name='live_detail'),
    # ライブ予定を編集
    path("live/<int:pk>/edit/", views.live_edit, name="live_edit"),
    # ライブ予定を削除する画面
    path("live/<int:pk>/delete/", views.live_delete, name="live_delete"),
    # ライブ参戦後の記録を追加する画面
    path("live/<int:pk>/record/add/",views.live_record_create,name="live_record_create"),
    # ライブ記録を削除する画面
    path("live/<int:pk>/record/delete/", views.live_record_delete, name="live_record_delete"),
    # ライブ記録を編集する画面
    path("live/<int:pk>/record/edit/",views.live_record_edit,name="live_record_edit"),
    # ライブ記録の履歴画面
    path("history/", views.history, name="history"),
    # 統計画面
    path("stats/", views.stats, name="stats"),
    # マイページ
    path("mypage/", views.mypage, name="mypage"),
    # プロフィール編集
    path("mypage/profile/edit/", views.profile_edit, name="profile_edit"),
    # お気に入りアーティスト管理
    path("mypage/favorites/",views.favorite_artist_manage,name="favorite_artist_manage"),
    # お気に入りアーティスト追加
    path("mypage/favorites/add/",views.favorite_artist_add,name="favorite_artist_add"),
    # お気に入りアーティスト削除
    path("mypage/favorites/<int:pk>/delete/",views.favorite_artist_delete,name="favorite_artist_delete"),
    # メールアドレス変更
    path("mypage/email/change/",views.email_change,name="email_change"),
    # パスワード変更
    path("mypage/password/change/",views.password_change,name="password_change"),
    # ログアウト
    path("logout/",views.logout_view,name="logout"),
    # ログアウト確認
    path("logout/confirm/",views.logout_confirm,name="logout_confirm"),
]
