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


class CourseTest(TestCase):
    def test_get(self):
        response = self.client.get('/api/v1/course/')
        self.assertEqual(response.status_code, 200)

    def test_get_by_code(self):
        response = self.client.get('/api/v1/course/1234')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('code'), 1234)
