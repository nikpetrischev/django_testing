from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest import lazy_fixture
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


@pytest.mark.parametrize(
    'parametrized_client, expected_count_of_comments',
    (
        (lazy_fixture('author_client'), 1),
        (lazy_fixture('client'), 0),
    )
)
@pytest.mark.django_db
def test_add_comment(
    parametrized_client,
    expected_count_of_comments,
    news_id,
    form_data,
):
    """
    Test if authorized user can add comments but unauthorized cannot.
    """
    url = reverse('news:detail', args=news_id)
    parametrized_client.post(url, data=form_data)
    comments_count = Comment.objects.count()
    assert comments_count == expected_count_of_comments


@pytest.mark.parametrize(
    'parametrized_client, expected_comments_count',
    (
        (lazy_fixture('author_client'), 0),
        (lazy_fixture('admin_client'), 1),
    )
)
def test_delete_comment(
    parametrized_client,
    expected_comments_count,
    comment_id,
):
    """Test if only author can delete theirs comments."""
    url = reverse('news:delete', args=comment_id)
    parametrized_client.post(url)
    comments_count = Comment.objects.count()
    assert comments_count == expected_comments_count


@pytest.mark.parametrize(
    'parametrized_client, expected_text_number, expected_status',
    (
        (
            lazy_fixture('author_client'),
            1,
            HTTPStatus.FOUND,
        ),
        (
            lazy_fixture('admin_client'),
            0,
            HTTPStatus.NOT_FOUND,
        ),
    )
)
def test_editing_comment(
    parametrized_client,
    expected_text_number,
    expected_status,
    comment_id,
    form_data,
    comment_text,
):
    """Test if only author can edit theirs comment."""
    url = reverse('news:edit', args=comment_id)
    response = parametrized_client.post(url, data=form_data)
    assert response.status_code == expected_status
    edited_comment = Comment.objects.get()
    assert edited_comment.text == comment_text[expected_text_number]


def test_cannot_use_bad_words(author_client, news_id):
    """Test filter for profane laanguage."""
    url = reverse('news:detail', args=news_id)
    response = author_client.post(url, data={'text': BAD_WORDS[0]})
    assertFormError(
        response,
        'form',
        'text',
        WARNING,
    )
    comments_count = Comment.objects.count()
    assert comments_count == 0
