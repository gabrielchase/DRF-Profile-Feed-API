import pytest
from django.test import RequestFactory, TestCase
from mixer.backend.django import mixer
pytestmark = pytest.mark.django_db

from .. import views
from .. import models
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

    def test_user_profile_viewset_account_creation(self):
        validated_data = {
            'email': 'test@test.com',
            'name': 'test',
            'password': 'password'
        }

        req = RequestFactory().post('/api/profile', data=json.dumps(validated_data), content_type='application/json')
        resp = views.UserProfileViewSet.as_view({'post': 'create'})(req)

        assert resp.status_code == 201, 'User was successfully created'
        assert resp.data['id'] == 1, 'New user created'
        assert resp.data['email'] == validated_data['email'], 'Given email is registered'
        assert resp.data['name'] == validated_data['name'], 'Given name is registered'


class TestUserProfileFeedViewSet(TestCase):
    def setUp(self):

        models.UserProfile.objects.create_user(email='test@test.com', name='test', password='password')

    def test_user_profile_feed_get_without_user(self):

        req = RequestFactory().get('/api/feed')
        resp = views.UserProfileFeedViewSet.as_view({
            'get': 'list'  
        })(req)

        assert resp.status_code == 401, 'User needs to be logged in to view the feed'

    def test_user_profile_feed_get_with_user(self):

        data = {
            'username': 'test@test.com',
            'password': 'password'
        }

        login_req = RequestFactory().post('/api/login', data=json.dumps(data), content_type='application/json')
        login_resp = views.LoginViewSet.as_view({'post': 'create'})(login_req)

        auth_token = 'Token ' + login_resp.data['token']
        # print('Auth Token: {0}'.format(auth_token))

        feed_req = RequestFactory().get('/api/feed', HTTP_AUTHORIZATION=auth_token)
        feed_resp = views.UserProfileFeedViewSet.as_view({'get': 'list'})(feed_req)

        print('login token: {0}'.format(login_resp.data['token']))
        # print('feed_resp: {0}'.format(feed_resp.__dict__))
        # print('feed_resp status code: {0}'.format(feed_resp.status_code))

        assert login_resp.status_code == 200, 'User is logged in so they can view the feed'
        assert feed_resp.status_code == 200, 'User can see the feed because they are logged in'
        assert auth_token is not None, 'Auth token is returned upon login'


class TestLoginViewSet(TestCase):

    def setUp(self):

        models.UserProfile.objects.create_user(email='tester@test.com', name='test', password='password')

    def test_login(self):

        data = {
            'username': 'tester@test.com',
            'password': 'password'
        }

        login_req = RequestFactory().post('/api/login', data=json.dumps(data), content_type='application/json')
        login_resp = views.LoginViewSet.as_view({'post': 'create'})(login_req)
        auth_token = 'Token ' + login_resp.data['token']

        assert login_resp.status_code == 200, 'User is logged in so they can view the feed'
        assert auth_token is not None, 'Auth token is given upon login'