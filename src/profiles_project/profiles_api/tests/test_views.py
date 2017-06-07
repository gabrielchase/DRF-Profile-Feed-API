import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from .. import views
import json


class TestUserProfileViewSet:
    def test_user_profile_viewset_get(self):
        obj = mixer.blend('profiles_api.UserProfile')
        req = RequestFactory().get('/api/profile')
        resp = views.UserProfileViewSet.as_view({
            'get': 'list'
        })(req)

        for data in resp.data:
            assert data['id'] is not None, 'Response data is not null and has id'
    
        assert resp.status_code == 200, 'Root is callable by anyone'

    def test_user_profile_viewset_retreieve(self):
        obj = mixer.blend('profiles_api.UserProfile')
        req = RequestFactory().get('/api/profile/{0}'.format(obj.pk))

        resp = views.UserProfileViewSet.as_view({
            'get': 'retrieve'
        })(req, pk=obj.pk)

        assert resp.status_code == 200, 'Response status code is callable'
        assert resp.data['id'] == obj.pk, 'Response data id is the same as the created object primary key'

    # def test_user_profile_viewset_post(self)
    #     obj = mixer.blend('profiles_api.UserProfile')
    #     req = RequestFactory().post('/api/profile')


class TestUserProfileFeedViewSet:
    def test_user_profile_feed_get_not_anonymous(self):
        req = RequestFactory().get('/api/feed')
        resp = views.UserProfileFeedViewSet.as_view({
            'get': 'list'
        })(req)

        assert resp.status_code == 401, 'User needs to be logged in to view the feed'

    def test_user_profile_feed_get_with_user(self):
        obj = mixer.blend('profiles_api.UserProfile')

        data = {
            'username': obj.email,
            'password': obj.password
        }
        print('data: {0}'.format(data))
        login_req = RequestFactory().post('/api/login', data=json.dumps(data), content_type='application/json')
        login_resp = views.LoginViewSet.as_view({'post': 'create'})(login_req)

        print('login_req: {0} | {1}'.format(login_req, type(login_req)))
        print('login_resp: {0}'.format(login_resp.data))

        # req = RequestFactory().get('/api/feed')
        # req.user = AnonymousUser()
        # print('req.user: {0}'.format(req.user))
        # resp = views.UserProfileFeedViewSet.as_view({
            # 'get': 'list'
        # })(req)

        assert login_resp.status_code == 200, 'User is logged in so they can view the feed'