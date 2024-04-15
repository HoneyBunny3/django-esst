import pytest

from django.contrib.auth.models import User

from notes.models import Notes
from .factories import UserFactory, NoteFactory

@pytest.fixture
def logged_user(client):
    user = UserFactory()
    client.login(username=user.username, password='password')
    return user

@pytest.mark.django_db
def test_list_endpoint_return_user_notes(client, logged_user):
        
    note = NoteFactory(user=logged_user)
    second_note = NoteFactory(user=logged_user)
    
    response = client.get(path='/smart/notes')
    content = str(response.content)
    
    assert 200 == response.status_code
    assert note.title in content
    assert second_note.title in content
    assert 2 == content.count('<h3>')

@pytest.mark.django_db
def test_list_endpoint_only_list_notes_from_authenticated_user(client, logged_user):
    another_user_note = NoteFactory()
    
    note = NoteFactory(user=logged_user)
    second_note = NoteFactory(user=logged_user)
    
    response = client.get(path='/smart/notes')
    content = str(response.content)
    
    assert 200 == response.status_code
    assert note.title in content
    assert second_note.title in content
    assert another_user_note.title not in content
    assert 2 == content.count('<h3>')
    
@pytest.mark.django_db
def test_create_endpoint_receives_form_data(client, logged_user):
    form_data = {'title': 'An impressive title', 'text': 'A really interesting text'}
    
    response = client.post(path='/smart/notes/new', data=form_data, follow=True)
    
    assert 200 == response.status_code
    assert 'notes/notes_list.html' in response.template_name
    assert 1 == logged_user.notes.count()
    assert "An impressive title" == logged_user.notes.first().title