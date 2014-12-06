import logging
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



 
