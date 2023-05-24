from django import template

register = template.Library()

@register.filter
def censor(value):
    censored_words = ['bad_word1', 'bad_word2', 'bad_word3']
    for word in censored_words:
        value = value.replace(word, '*' * len(word))
    return value