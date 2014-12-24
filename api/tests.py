import logging
import time
import unittest.mock
from django.test import TestCase, Client
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from api.models import *

logger = logging.getLogger(__name__)


class Test1(TestCase):
    def test1(self):
        x = True
        self.assertTrue(x)


def mock_fb_get1(token, appid, appsecret):
    return ('longtoken', time.time())

class Api(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        User.objects.create_user('test', 'test@example.com', 'pass')
        self.client.login(username='test', password='pass')
        fp = FoodPhoto(
            photo_url='https://prandius.s3.amazonaws.com/t_feed_762954137074363-1418328283.jpg',
            user=User.objects.first(),
        )
        fp.save()
        p = Post(
            user=User.objects.first(),
            foodphoto=fp,
            description='bla',
            address_raw='Utrecht',
            coords_x=52,
            coords_y=5,
        )
        p.save()

    def test_api_test(self):
        resp = self.client.get('/api/test/')
        self.assertEqual(resp.status_code, 200)

    def _test_api_sign_s3(self):
        resp = self.client.get('/sign_s3/')
        # MultiValueDictKeyError
        self.assertEqual(resp.status_code, 200)

    def test_api_latest_posts(self):
        resp = self.client.get('/api/latest_posts/')
        self.assertEqual(resp.status_code, 200)

    def test_api_user_login_status(self):
        resp = self.client.get('/api/user_login_status/')
        self.assertEqual(resp.status_code, 200)

    @unittest.mock.patch(
        'facepy.get_extended_access_token',
        new=mock_fb_get1)
    def test_api_backend_login(self):
        data = {}
        data['fbUid'] = '123456789'
        data['name'] = 'Harry Hipster'
        data['accessToken'] = 'sjdihgkjgijesihiogtnvrdruh'

        resp = self.client.post(
            '/api/backend_login/',
            data=data,
            #content_type='application/json',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(resp.status_code, 200)

    def test_api_currentuser_latest_posts(self):
        resp = self.client.get('/api/currentuser/latest_posts/')
        self.assertEqual(resp.status_code, 200)

    def test_api_post_detail(self):
        resp = self.client.get('/api/post_detail/1/')
        self.assertEqual(resp.status_code, 200)

    def test_api_csrf_token(self):
        resp = self.client.get('/api/csrf_token/')
        self.assertEqual(resp.status_code, 200)

    def test_api_post_detail_fb(self):
        resp = self.client.get('/api/post_detail_fb/1/')
        self.assertEqual(resp.status_code, 302)


class Tools(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        User.objects.create_user('test', 'test@example.com', 'pass')
        self.client.login(username='test', password='pass')
        fp = FoodPhoto(
            photo_url='https://prandius.s3.amazonaws.com/t_feed_762954137074363-1418328283.jpg',
            user=User.objects.first(),
        )
        fp.save()
        p = Post(
            user=User.objects.first(),
            foodphoto=fp,
            description='bla',
        )
        p.save()

    def test_create_missing_thumbnails(self):
        resp = self.client.get('/api/test/')
        self.assertEqual(resp.status_code, 200)
        # TODO: test


