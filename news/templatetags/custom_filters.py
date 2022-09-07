from django import template

register = template.Library()

CENSORED_WORDS = {
    'lorem': 'l****',
    'tempor': 't*****',
    'sit': 's**'
}


@register.filter(name='censor')
def censor(value):
    """
   value: the value to apply the filter to
   """
    if not isinstance(value, str):
        raise ValueError

    for text, censored in CENSORED_WORDS.items():
        value = value.replace(text, censored)

    return value
