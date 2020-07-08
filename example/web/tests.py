from django.test import TestCase


# Create your tests here.

class UserTest(TestCase):
    def test_get_info(self):
        response = self.client.get('/api/v1/user/info/?hello=world')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'hello': 'world'})

    def test_post(self):
        response = self.client.post('/api/v1/user/info/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('msg'), 'ok')

    def test_group_by(self):
        response = self.client.get('/api/v1/user/group_by_11111/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('field_name'), '11111')

    def test_re_path(self):
        response = self.client.post('/api/v1/user/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('pk'), '12345')

    def test_method_not_allowed(self):
        response = self.client.delete('/api/v1/user/info/')
        self.assertEqual(response.status_code, 405)


class CourseTest(TestCase):
    def test_get(self):
        response = self.client.get('/api/v1/course/')
        self.assertEqual(response.status_code, 200)

    def test_get_by_code(self):
        response = self.client.get('/api/v1/course/1234')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('code'), 1234)


class TestApiView(TestCase):
    def test_post(self):
        response = self.client.post('/api/v1/test/', data={'user': 'test'})
        self.assertEqual(response.status_code, 200)
