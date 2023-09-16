from datetime import datetime, timedelta

import pytest
from django.conf import settings

from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Author')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Headline',
        text='Some news text.',
    )
    return news


@pytest.fixture
def comment_text():
    return (
        'Some comment text.',
        'Some new text.',
    )


@pytest.fixture
def comment(author, news, comment_text):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=comment_text[0],
    )
    return comment


@pytest.fixture
def news_id(news):
    return news.pk,


@pytest.fixture
def comment_id(comment):
    return comment.pk,


@pytest.fixture
def form_data(comment_text):
    return {'text': comment_text[1]}


@pytest.fixture
def multiple_news():
    news = []
    today = datetime.today()
    for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news_piece = News.objects.create(
            title=f'News{index}',
            text=f'Some text {index}.',
            date=today - timedelta(days=index),
        )
        news.append(news_piece)
    return news


@pytest.fixture
def multiple_comments(author, news):
    now = datetime.now()
    comments = []
    for index in range(2):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text=f'Some comment {index}.',
            created=now + timedelta(hours=index)
        )
        comments.append(comment)
    return comments
