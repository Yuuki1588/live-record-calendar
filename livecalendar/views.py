# 月間カレンダーを作るための機能を使えるようにする
import calendar

# 今日の日付を取得するための機能を使えるようにする
from datetime import date

# HTMLを表示したり、別のページへ移動したりするための機能
from django.shortcuts import render, redirect

# 作成した新規登録フォームを使えるようにする
from .forms import SignUpForm

# ライブ予定のデータを使えるようにする
from .models import LiveSchedule

# ログインしているユーザーだけ画面を見られるようにする
from django.contrib.auth.decorators import login_required

# ホーム画面を表示する
@login_required
def index(request):

    # 今日の日付を取得する
    today = date.today()

    # URLから表示したい年と月を取得する
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))

    # カレンダーで選択された日を取得する
    selected_day = request.GET.get('day')

    # 日付が選択されている場合は数字に変換する
    if selected_day:
        selected_day = int(selected_day)

    # 現在の月のカレンダーを作成する
    month_calendar = calendar.monthcalendar(year, month)

    # 前の月を計算する
    if month == 1:
        prev_year = year - 1
        prev_month = 12
    else:
        prev_year = year
        prev_month = month - 1

    # 次の月を計算する
    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1
    
    # 表示している年月のライブ予定だけを取得する
    live_schedules = LiveSchedule.objects.filter(
    user=request.user,
    event_date__year=year,
    event_date__month=month
    )

    # 日付が選択されている場合、その日のライブ予定だけを取得する
    if selected_day:
        selected_schedules = live_schedules.filter(
            event_date__day=selected_day
        )
    else:
        selected_schedules = live_schedules

    # ライブ予定を日付ごとにまとめる
    schedules_by_day = {}

    for schedule in live_schedules:
        day = schedule.event_date.day

        if day not in schedules_by_day:
            schedules_by_day[day] = []

        schedules_by_day[day].append(schedule)

     # カレンダーの日付と、その日のライブ予定をセットにする
    calendar_data = []

    # 1週間ずつ処理する
    for week in month_calendar:
        week_data = []

        # 1週間の中の日付を1日ずつ処理する
        for day in week:
            schedules = schedules_by_day.get(day, [])

            # 日付と、その日のライブ予定をセットにする
            week_data.append({
            'day': day,
            'schedules': schedules,
            })

        # 完成した1週間分をカレンダーに追加する
        calendar_data.append(week_data)

    # 取得したライブ予定をindex.htmlに渡す
    return render(
    request,
    'livecalendar/index.html',
    {
    'live_schedules': live_schedules,
    'selected_schedules': selected_schedules,
    'selected_day': selected_day,
    'month_calendar': month_calendar,
    'schedules_by_day': schedules_by_day,
    'calendar_data': calendar_data,
    'year': year,
    'month': month,
    # 前の月の情報をHTMLに渡す
    'prev_year': prev_year,
    'prev_month': prev_month,

    # 次の月の情報をHTMLに渡す
    'next_year': next_year,
    'next_month': next_month,
    }
    )


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


# ライブ詳細画面を表示する
@login_required
def live_detail(request, schedule_id):

    # 選択されたライブ予定を取得する
    schedule = LiveSchedule.objects.get(
        id=schedule_id,
        user=request.user
    )

    # ライブ詳細画面を表示する
    return render(
        request,
        'livecalendar/live_detail.html',
        {
            'schedule': schedule,
        }
    )