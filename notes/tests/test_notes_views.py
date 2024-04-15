import pytest

from django.contrib.auth.models import User

from notes.models import Notes

@pytest.mark.django_db
def test_list_endpoint_return_user_notes(client):
    user = User.objects.create_user('Hearthy', 'test@test.com', 'password')
    client.login(username=user.username, password='password')
    
    note = Notes.objects.create(title='An interesting title', text='', user=user)
    note2 = Notes.objects.create(title='Another title', text='', user=user)
    
    response = client.get(path='/smart/notes')
    assert 200 == response.status_code
    content = str(response.content)
    assert "An interesting title" in content
    assert "Another title" in content
    assert 2 == content.count('<h3>')

@pytest.mark.django_db
def test_list_endpoint_only_list_notes_from_authenticated_user(client):
    jon = User.objects.create_user('Jon', 'test2@test.com', 'password')
    Notes.objects.create(title="Jon's notes", text="", user=jon)
    
    user = User.objects.create_user('Hearthy', 'test@test.com', 'password')
    client.login(username=user.username, password='password')
    
    note = Notes.objects.create(title='An interesting title', text='', user=user)
    note2 = Notes.objects.create(title='Another title', text='', user=user)
    
    response = client.get(path='/smart/notes')
    assert 200 == response.status_code
    content = str(response.content)
    assert "An interesting title" in content
    assert "Another title" in content
    assert "Jon's note" not in content
    assert 2 == content.count('<h3>')