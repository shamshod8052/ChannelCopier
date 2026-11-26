from unittest import mock

from django.db import OperationalError
from django.test import SimpleTestCase


class HealthzTests(SimpleTestCase):
    @mock.patch('Admin.views.connection')
    def test_ok(self, connection):
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})
        connection.cursor.return_value.__enter__.return_value.execute.assert_called_once_with('SELECT 1')

    @mock.patch('Admin.views.connection')
    def test_db_down(self, connection):
        connection.cursor.side_effect = OperationalError('connection refused')
        response = self.client.get('/healthz')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'error', 'db': 'connection refused'})
