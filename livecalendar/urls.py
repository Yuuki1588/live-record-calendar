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
    # ライブ予定追加画面
    path('live/add/', views.live_create, name='live_create'),
    # ライブ予定を編集
    path("live/<int:pk>/edit/", views.live_edit, name="live_edit"),
    # ライブ予定を削除する画面
    path("live/<int:pk>/delete/", views.live_delete, name="live_delete"),
    # ライブ参戦後の記録を追加する画面
    path("live/<int:pk>/record/add/",views.live_record_create,name="live_record_create"),
]
