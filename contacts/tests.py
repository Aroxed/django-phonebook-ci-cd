import pytest
from django.urls import reverse
from .models import Contact

@pytest.fixture(autouse=True)
def cleanup_database():
    """Clean up the database before each test."""
    yield
    Contact.objects.delete()

@pytest.fixture
def sample_contact():
    """Create a sample contact for testing."""
    contact = Contact(name='John Doe', phone='1234567890')
    contact.save()
    return contact

@pytest.fixture
def sample_contacts():
    """Create multiple sample contacts for testing."""
    contacts = [
        Contact(name='Jane Smith', phone='9876543210'),  # Jane comes before John alphabetically
        Contact(name='John Doe', phone='1234567890')
    ]
    for contact in contacts:
        contact.save()
    return contacts

@pytest.mark.django_db
class TestContactsAPI:
    def test_get_contacts_list(self, client, sample_contacts):
        # Get contacts list
        response = client.get(
            reverse('get_contacts'),
            HTTP_ACCEPT='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]['name'] == 'Jane Smith'  # Jane comes first alphabetically
        assert data[1]['name'] == 'John Doe'

    def test_add_contact_api(self, client):
        response = client.post(
            reverse('get_contacts'),
            {'name': 'John Doe', 'phone': '1234567890'},
            content_type='application/json',
            HTTP_ACCEPT='application/json'
        )
        assert response.status_code == 201
        assert response.json()['message'] == 'Contact added successfully'
        
        # Verify contact was added
        contact = Contact.objects.get(name='John Doe')
        assert contact.phone == '1234567890'

    def test_add_contact_missing_fields(self, client):
        response = client.post(
            reverse('get_contacts'),
            {'name': 'John Doe'},  # Missing phone
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'error' in response.json()

    def test_get_contact_detail(self, client, sample_contact):
        # Get contact detail
        response = client.get(
            reverse('contact_detail', args=['John Doe']),
            HTTP_ACCEPT='application/json'
        )
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == 'John Doe'
        assert data['phone'] == '1234567890'

    def test_get_nonexistent_contact(self, client):
        response = client.get(
            reverse('contact_detail', args=['Nonexistent']),
            HTTP_ACCEPT='application/json'
        )
        assert response.status_code == 404
        assert 'error' in response.json()

    def test_update_contact_api(self, client, sample_contact):
        # Update contact
        response = client.put(
            reverse('contact_detail', args=['John Doe']),
            {'phone': '9876543210'},
            content_type='application/json',
            HTTP_ACCEPT='application/json'
        )
        assert response.status_code == 200
        assert response.json()['message'] == 'Contact updated successfully'
        
        # Verify update
        contact = Contact.objects.get(name='John Doe')
        assert contact.phone == '9876543210'

    def test_delete_contact_api(self, client, sample_contact):
        # Delete contact
        response = client.delete(
            reverse('contact_detail', args=['John Doe']),
            HTTP_ACCEPT='application/json'
        )
        assert response.status_code == 200
        assert response.json()['message'] == 'Contact deleted successfully'
        
        # Verify deletion
        assert Contact.objects.filter(name='John Doe').count() == 0

@pytest.mark.django_db
class TestContactsWeb:
    def test_index_page(self, client):
        response = client.get(reverse('index'))
        assert response.status_code == 200
        assert 'Add New Contact' in response.content.decode()
        assert 'Contacts' in response.content.decode()

    def test_add_contact_form(self, client):
        response = client.post(
            reverse('get_contacts'),
            {'name': 'John Doe', 'phone': '1234567890'}
        )
        assert response.status_code == 302  # Redirect after successful add
        
        # Verify contact was added
        contact = Contact.objects.get(name='John Doe')
        assert contact.phone == '1234567890'

    def test_contact_detail_page(self, client, sample_contact):
        # Get contact detail page
        response = client.get(reverse('contact_detail', args=['John Doe']))
        assert response.status_code == 200
        content = response.content.decode()
        assert 'John Doe' in content
        assert '1234567890' in content
        assert 'Edit Contact' in content

    def test_edit_contact_form(self, client, sample_contact):
        # Edit contact using form
        response = client.post(
            reverse('contact_detail', args=['John Doe']),
            {'_method': 'PUT', 'phone': '9876543210'}
        )
        assert response.status_code == 302  # Redirect after successful edit
        
        # Verify update
        contact = Contact.objects.get(name='John Doe')
        assert contact.phone == '9876543210'

    def test_delete_contact_form(self, client, sample_contact):
        # Delete contact using form
        response = client.post(
            reverse('contact_detail', args=['John Doe']),
            {'_method': 'DELETE'}
        )
        assert response.status_code == 302  # Redirect after successful delete
        
        # Verify deletion
        assert Contact.objects.filter(name='John Doe').count() == 0

    def test_nonexistent_contact_page(self, client):
        response = client.get(reverse('contact_detail', args=['Nonexistent']))
        assert response.status_code == 404
        assert 'Error' in response.content.decode()
        assert 'Contact not found' in response.content.decode() 