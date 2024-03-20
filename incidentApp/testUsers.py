from django.test import TestCase
from django.test import Client


class TestUsers(TestCase):

    def test_invalid_password(self):
        client = Client()
        response = client.post("/accounts/register/",
                               {
                                   "first_name": "harry",
                                   "last_name": "harry",
                                   "email": "harry@gmail.com",
                                   "username": "harry",
                                   "password": "password",
                                   "password2": "password"
                               },
                               follow=True)

        self.assertRedirects(response, "/accounts/regsiter/", 302, 200)
        self.assertContains(response, "Password is rubbish!")
