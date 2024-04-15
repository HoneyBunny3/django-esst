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
    jon = User.objects.create_user('Jon', 'test2@test.com', 'password')
    Notes.objects.create(title="Jon's notes", text="", user=jon)
    
    note = Notes.objects.create(title='An interesting title', text='', user=logged_user)
    note2 = Notes.objects.create(title='Another title', text='', user=logged_user)
    
    response = client.get(path='/smart/notes')
    assert 200 == response.status_code
    content = str(response.content)
    assert "An interesting title" in content
    assert "Another title" in content
    assert "Jon's note" not in content
    assert 2 == content.count('<h3>')