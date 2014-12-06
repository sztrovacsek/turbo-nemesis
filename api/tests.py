import logging
import unittest.mock as mock
from django.test import TestCase, Client
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class Test1(TestCase):
    def test1(self):
        x = True
        self.assertTrue(x)


class Api(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        User.objects.create_user('test', 'test@example.com', 'pass')
        self.client.login(username='test', password='pass')

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

    @mock.patch('facepy.get_extended_access_token')
    def _test_api_backend_login(self, mock1):
        # TODO: make it ajax
        # TODO: POST data
        data = {}
        data['fbUid'] = '123456789'
        data['name'] = 'Harry Hipster'
        data['accessToken'] = 'sjdihgkjgijesihiogtnvrdruh'

        resp = self.client.post('/api/backend_login/', data)
        self.assertEqual(resp.status_code, 200)



 
