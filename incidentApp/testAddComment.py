
# from django.test import TestCase
# from django.test import Client
# from django.contrib.auth.models import User
# from incidents.models import Incident, System, Status, Priority
# from django.test import TestCase, override_settings
#
#
# @override_settings(AXES_ENABLED=False)
# class TestAddComment(TestCase):
#
#     def TestAddBlankComment(self):
#
#         client = Client()
#
#     user = User.objects.create_user(
#         username='harry',
#         password='harry',
#         first_name='harry',
#         last_name='harry',
#         email='harry@somewhere.com',
#         is_staff=False
#     )
#
#     client.login(username='harry', password='harry')
#
#     incident = Incident.objects.create(
#         title='title',
#         description='description',
#         system=System.objects.create(name='name', description='description'),
#         priority='H',
#         ownedBy=None,
#         reportedBy=User.objects.filter(username='harry').get()
#     )
#
#     response = client.post("/incidents/" + str(incident.id) + "/updateincident/",
#                            {'addcomment': 'addcomment'},
#                            follow=True)
#
#     messages = list(response.context['messages'])
#     self.assertEqual(len(messages), 1)
#     self.assertEquals(str(messages[0]), "Comment is empty and has not been saved....")
#     self.assertTrue(Incident.objects.filter(id=incident.id).exists())
