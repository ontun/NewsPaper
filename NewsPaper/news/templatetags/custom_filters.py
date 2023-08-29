from django import template

register = template.Library()

CENSOR_SYMBOLS = ['Редиск', 'редиск', 'Новост', 'новост']


@register.filter()
def censor(value):
    if isinstance(value, str):
        for i in CENSOR_SYMBOLS:
            censored_value = i[0] + '*' * (len(i))
            value = value.replace(i, censored_value)

    return f'{value}'
