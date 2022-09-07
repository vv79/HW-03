from news.models import *
from django.utils.lorem_ipsum import paragraphs, words
from random import randint

user_list = [
    User.objects.create_user('ivanov', password='ivanov'),
    User.objects.create_user('petrov', password='petrov')
]

author_list = [Author.objects.create(user=user_list[0]), Author.objects.create(user=user_list[1])]

category_list = []
for i in range(4):
    category_list.append(Category.objects.create(name=f'Category {i+1}'))


news_list = []
for i in range(100):
    news_list.append(Post.objects.create(
        author=author_list[randint(0, 1)],
        type=article if randint(0, 1) == 0 else news,
        title=words(randint(5, 8)),
        content=words((i+1)*10)
    ))


for news_one in news_list:
    news_one.categories.add(category_list[randint(0, 3)])

news_list[0].categories.add(category_list[0])
news_list[0].categories.add(category_list[1])

comment_list = []
for i in range(100):
    comment_list.append(Comment.objects.create(
        post=news_list[randint(0, 2)],
        user=user_list[randint(0, 1)],
        content=words(randint(3, 10))
    ))

for user in user_list:
    for news_one in news_list:
        if randint(0, 1):
            news_one.like()
        else:
            news_one.dislike()

    for comment in comment_list:
        if randint(0, 1):
            comment.like()
        else:
            comment.dislike()

for author in author_list:
    author.update_rating()

print('==================== Best author ======================')
print(Author.objects.all().order_by('-rating').first())
print('==================== Best post ========================')
print(Post.objects.all().order_by('-rating').first())
print('==================== All comments ====================')
for comment in Comment.objects.all():
    print(comment)
