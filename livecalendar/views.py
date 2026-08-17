# HTMLを表示したり、別のページへ移動したりするための機能
from django.shortcuts import render, redirect

# 作成した新規登録フォームを使えるようにする
from .forms import SignUpForm

# ログインしているユーザーだけ画面を見られるようにする
from django.contrib.auth.decorators import login_required

# ホーム画面を表示する
@login_required
def index(request):
    return render(request, 'livecalendar/index.html')


# 新規登録画面の処理
def signup(request):

    # 登録ボタンが押された場合
    if request.method == "POST":
        form = SignUpForm(request.POST)

        # 入力内容に問題がなければユーザーを登録する
        if form.is_valid():
            form.save()

            # 登録完了後、ログイン画面へ移動する
            return redirect("login")

    # 最初に新規登録画面を開いた場合
    else:
        form = SignUpForm()

    # signup.htmlに新規登録フォームを渡して表示する
    return render(request, "livecalendar/signup.html", {"form": form})