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

@register.filter
def hide_forbidden(value):
    words = value.split()
    result = []
    for word in words:
        if word in CENSORED_WORDS.keys():
            result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)
