from modeltranslation.translator import translator, TranslationOptions
from .models import Category, Post


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'content',)


translator.register(Post, PostTranslationOptions)
