from django.conf import settings
from django.urls import reverse
import pytest
from pytest import lazy_fixture


@pytest.mark.django_db
@pytest.mark.usefixtures('multiple_news')
def test_news_on_one_page(client):
    """Test if there are no more than CONST news on main page."""
    url = reverse('news:home')
    response = client.get(url)
    news_count = len(response.context['object_list'])
    assert news_count == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.django_db
@pytest.mark.usefixtures('multiple_news')
def test_news_order(client):
    """Test if news are shown in right order."""
    url = reverse('news:home')
    response = client.get(url)
    news_dates = [news.date for news in response.context['object_list']]
    ordered_dates = sorted(news_dates, reverse=True)
    assert news_dates == ordered_dates


@pytest.mark.usefixtures('multiple_comments')
def test_comments_order(client, news_id):
    """Test if comments are shown in right order."""
    url = reverse('news:detail', args=news_id)
    response = client.get(url)
    all_comments = response.context['news'].comment_set.all()
    assert all_comments[0].created < all_comments[1].created


@pytest.mark.parametrize(
    'parametrized_client, form_is_shown',
    (
        (lazy_fixture('author_client'), True),
        (lazy_fixture('client'), False),
    )
)
@pytest.mark.django_db
def test_form_is_shown_to_correct_user(
    parametrized_client,
    form_is_shown,
    news_id,
):
    """Test if create comment form is shown only to authorized user."""
    url = reverse('news:detail', args=news_id)
    response = parametrized_client.get(url)
    assert ('form' in response.context) == form_is_shown
