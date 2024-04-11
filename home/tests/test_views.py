import pytest

from django.contrib.auth.models import User

def test_home_endpoint_returns_welcome_page(client):
    response = client.get(path='/')
    assert response.status_code == 200 ### status code 200 means URL was redirected successfully, request succeeded
    assert 'Welcome to SmartNotes!' in str(response.content) ### this is testing that the landing page should show the text asserted!
    
### test unauthenticated user access to the signup page
def test_signup_endpoint_returns_form_for_unauthenticated_user(client):
    response = client.get(path='/signup')
    assert response.status_code == 200 ### status code 200 means URL was redirected successfully, request succeeded
    assert 'home/register.html' in response.template_name ### this is testing that the unauthenticated user will be redirected to the register page
    
### test authenticatd user access to the signup page
@pytest.mark.django_db ### this adds the test user to the temporary test database environment. Pytest prevents accidental writes to the production database!
def test_signup_endpoint_redirects_authenticatd_user(client):
    '''
        When a user is authenticated and tries to access the
        signup page, they are redirected to the list of their notes.
    '''
    user = User.objects.create_user('Hearthy', 'test@test.com', 'password')
    client.login(username=user.username, password='password')
    assert user.is_authenticated
    
    response = client.get(path='/signup', follow=True) ### follow=True replaces print(type(resposne))
    print(type(response)) ### prints response details
    assert 200 == response.status_code ### this sets the expected result before the actual result; guarantees that we know what to expect vs actual result!
    assert 'notes/notes_list.html' in response.template_name ### this is testing where the authenticated user will land, not seeing the signup page but the notes list page!