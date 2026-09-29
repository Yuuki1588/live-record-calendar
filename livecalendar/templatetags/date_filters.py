# Djangoのテンプレート機能を読み込む
from django import template


# テンプレートタグを登録するための準備
register = template.Library()


# 日付を「2026年9月29日（火）」の形式に変換するフィルター
@register.filter
def japanese_date(value):

    # 曜日を日本語に対応させる
    weekdays = ["月", "火", "水", "木", "金", "土", "日"]

    # 日付と日本語の曜日を組み合わせて返す
    return f"{value.year}年{value.month}月{value.day}日（{weekdays[value.weekday()]}）"