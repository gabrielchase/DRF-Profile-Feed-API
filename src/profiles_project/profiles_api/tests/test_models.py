import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestUserProfile:
    def test_model(self):
        obj = mixer.blend('profiles_api.UserProfile')

        assert obj.pk == 1, 'Should create a User Profile instance'
    
    def test_model_full_name(self):
        obj = mixer.blend('profiles_api.UserProfile')

        assert obj.name == obj.get_full_name(), 'Object name should be returned'
        
    def test_model_short_name(self):
        obj = mixer.blend('profiles_api.UserProfile')
        assert obj.name == obj.get_short_name(), 'Object name should be returned'

    def test_model__str__(self):
        obj = mixer.blend('profiles_api.UserProfile')
        assert obj.email == str(obj), "Object's string representation is its email"

class TestProfileFeedItem:
    def test_model(self):
        obj = mixer.blend('profiles_api.ProfileFeedItem')

        assert obj.pk == 1, 'Should create a Profile Feed Item instance'

    def test_model__str__(self):
        obj = mixer.blend('profiles_api.ProfileFeedItem')

        assert obj.status_text == str(obj), "Object's string representation is the status_text"
