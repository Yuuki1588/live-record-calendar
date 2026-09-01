# 月間カレンダーを作るための機能を使えるようにする
import calendar

# 今日の日付を取得するための機能を使えるようにする
from datetime import date

# HTMLを表示したり、別のページへ移動したりするための機能
from django.shortcuts import render, redirect

# 新規登録・ライブ予定・ライブ記録のフォームを使えるようにする
from .forms import SignUpForm, LiveScheduleForm, LiveRecordForm, RecordPhotoForm

# ライブ予定・アーティスト・対バンアーティスト・ライブ記録のデータを使えるようにする
from .models import LiveSchedule, Artist, OpponentArtist, LiveRecord

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

    # このライブに保存されている記録を取得する
    record = LiveRecord.objects.filter(
        live_schedule=schedule
    ).first()

    # ライブ詳細画面を表示する
    return render(
        request,
        'livecalendar/live_detail.html',
        {
            'schedule': schedule,
            'record': record,
        }
    )


@login_required
def live_create(request):

    # 登録ボタンが押された場合
    if request.method == "POST":
        form = LiveScheduleForm(request.POST)

        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()

            # 対バンアーティストを取得
            opponent_names = form.cleaned_data["opponent_artists"]

            # カンマで1組ずつ分ける
            for opponent_name in opponent_names.split(","):
                opponent_name = opponent_name.strip()

                if opponent_name:
                    opponent_artist, created = Artist.objects.get_or_create(
                        artist_name=opponent_name
                    )

                    OpponentArtist.objects.create(
                        live_schedule=schedule,
                        artist=opponent_artist
                    )

            # 全対バンの登録が終わってから戻る
            return redirect("home")

    # 最初にライブ予定追加画面を開いた場合
    else:
        form = LiveScheduleForm()

    # ライブ予定追加画面を表示する
    return render(
        request,
        "livecalendar/live_create.html",
        {
            "form": form,
        }
    )

# ライブ予定を編集する
@login_required
def live_edit(request, pk):

    # 編集するライブ予定を取得する
    schedule = LiveSchedule.objects.get(
        pk=pk,
        user=request.user
        )

    # 保存ボタンが押された場合
    if request.method == "POST":
        form = LiveScheduleForm(
            request.POST,
            instance=schedule
        )

        # 入力内容に問題がない場合
        if form.is_valid():

            # ライブ予定の編集内容を保存する
            form.save()

            # 今まで登録されていた対バン情報を削除する
            OpponentArtist.objects.filter(
                live_schedule=schedule
            ).delete()

            # 編集画面に入力された対バンアーティストを取得する
            opponent_names = form.cleaned_data["opponent_artists"]

            # カンマで区切って、対バンアーティストを1組ずつ取り出す
            for opponent_name in opponent_names.split(","):

                # 名前の前後にある余分な空白を削除する
                opponent_name = opponent_name.strip()

                # 名前が入力されている場合
                if opponent_name:

                    # 同じ名前のアーティストを探す
                    # 登録されていなければ新しくArtistテーブルに登録する
                    opponent_artist, created = Artist.objects.get_or_create(
                        artist_name=opponent_name
                    )

                    # このライブ予定の対バンアーティストとして保存する
                    OpponentArtist.objects.create(
                        live_schedule=schedule,
                        artist=opponent_artist
                    )

            # 保存後はライブ詳細画面へ戻る
            return redirect(
                "live_detail",
                schedule_id=schedule.pk
            )

    # 最初に編集画面を開いた場合
    else:

        # 現在登録されている対バンアーティスト名を取得する
        opponent_names = ", ".join(
            opponent.artist.artist_name
            for opponent in schedule.opponentartist_set.all()
        )

        # 現在のライブ情報を編集フォームに表示する
        form = LiveScheduleForm(
            instance=schedule,
            initial={
                "opponent_artists": opponent_names
            }
        )

    # 編集画面を表示する
    return render(
        request,
        "livecalendar/live_edit.html",
        {
            "form": form,
            "schedule": schedule,
        }
    )


# ライブ予定を削除する
@login_required
def live_delete(request, pk):

    # ログイン中のユーザーのライブ予定を取得する
    schedule = LiveSchedule.objects.get(
        pk=pk,
        user=request.user
    )

    # 削除ボタンが押された場合
    if request.method == "POST":

        # ライブ予定を削除する
        schedule.delete()

        # 削除後はカレンダー画面へ戻る
        return redirect("home")

    # 削除確認画面を表示する
    return render(
        request,
        "livecalendar/live_delete.html",
        {
            "schedule": schedule,
        }
    )


# ライブ参戦後の記録を追加する
@login_required
def live_record_create(request, pk):

    # ログイン中のユーザーのライブ予定を取得する
    schedule = LiveSchedule.objects.get(
        pk=pk,
        user=request.user
    )

    # 保存ボタンが押された場合
    if request.method == "POST":
        form = LiveRecordForm(request.POST,request.FILES)

        # 写真を登録するフォーム
        photo_form = RecordPhotoForm(request.POST,request.FILES)

        # 入力内容に問題がなければ保存する
        if form.is_valid() and photo_form.is_valid():
            record = form.save(commit=False)

            # どのライブの記録なのかを設定する
            record.live_schedule = schedule

            # ライブ記録を保存する
            record.save()

            # 写真をライブ記録に紐づけて保存する
            photo = photo_form.save(commit=False)

            photo.live_record = record

            photo.save()

            # 保存後はライブ詳細画面へ戻る
            return redirect(
                "live_detail",
                schedule_id=schedule.pk
            )

    # 最初に記録画面を開いた場合
    else:
        form = LiveRecordForm()

        # 写真を登録するフォーム
        photo_form = RecordPhotoForm()

    # ライブ記録追加画面を表示する
    return render(
        request,
        "livecalendar/live_record_create.html",
        {
            "form": form,
            "photo_form": photo_form,
            "schedule": schedule,
        }
    )