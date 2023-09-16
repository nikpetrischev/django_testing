from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest import lazy_fixture
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'url_name, url_args',
    (
        ('news:home', None),
        ('news:detail', lazy_fixture('news_id')),
        ('users:signup', None),
        ('users:login', None),
        ('users:logout', None),
    )
)
@pytest.mark.django_db
def test_page_availability_for_anon(client, url_name, url_args):
    """
    Testing if unauthorized user can access following pages:
    main, login/logout, registration, news page.
    """
    url = reverse(url_name, args=url_args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (lazy_fixture('author_client'), HTTPStatus.OK),
        (lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
    )
)
@pytest.mark.parametrize(
    'url_name, url_args',
    (
        ('news:edit', lazy_fixture('comment_id')),
        ('news:delete', lazy_fixture('comment_id')),
    )
)
def test_access_to_edit_delete_comment_by_authorized_user(
    parametrized_client,
    expected_status,
    url_name,
    url_args,
):
    """
    Test result of accessing comment's edit/delete pages by author/other user.
    """
    url = reverse(url_name, args=url_args)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'url_name, url_args',
    (
        ('news:edit', lazy_fixture('comment_id')),
        ('news:delete', lazy_fixture('comment_id')),
    )
)
def test_access_to_edit_delete_comment_by_anon(
    client,
    url_name,
    url_args,
):
    """
    Test if anonymous user will be redirected from edit/delete comment pages.
    """
    url = reverse(url_name, args=url_args)
    login_url = reverse('users:login')
    response = client.get(url)
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
