from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):  # Проверяем, что dictionary — это словарь
        return dictionary.get(key, '')
    return ''  # Возвращаем пустую строку, если dictionary не является словарем


@register.filter
def format_date(value, date_format="%d.%m.%Y"):
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d")
    return value.strftime(date_format)