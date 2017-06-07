import pytest
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

class TestUserProfile:
    def test_model(self):
        obj = mixer.blend('profiles_api.UserProfile')

        assert obj.pk == 1, 'Should create a User Profile instance'
        assert obj.name == obj.get_full_name(), 'Object name should be returned'
        assert obj.name == obj.get_short_name(), 'Object name should be returned'
        assert obj.email == str(obj), "Object's string representation is its email"

class TestProfileFeedItem:
    def test_model(self):
        obj = mixer.blend('profiles_api.ProfileFeedItem')

        assert obj.status_text == str(obj), "Object's string representation is the statu_text"
