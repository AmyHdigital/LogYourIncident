from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from incidents.models import Incident, System, Status, Priority
from django.test import TestCase, override_settings


@override_settings(AXES_ENABLED=False)
class TestDeleteIncidents(TestCase):

    def testDeleteIncidentWithNonAdminUser(self):
        client = Client()

        user = User.objects.create_user(
            username='harry',
            password='harry',
            first_name='harry',
            last_name='harry',
            email='harry@somewhere.com',
            is_staff=False
        )

        client.login(username='harry', password='harry')

        # Capture number of incidents at the start of the test
        numberOfIncidents = Incident.objects.count();

        incident = Incident.objects.create(
            title='title',
            description='description',
            system=System.objects.create(name='name', description='description'),
            priority='H',
            reportedBy=User.objects.filter(username='harry').get()
        )

        # Verify that the incident has been created and there is
        # now one more in the list of incidents.
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)

        response = client.post("/incidents/" + str(incident.id) + "/updateincident/",
                               {'delete': 'delete'},
                               follow=True)

        # Verify that the delete operations has been called and that
        # the incident has NOT been deleted
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)
        self.assertEquals(str(messages[0]), "Only admin users can delete incidents.")
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())

    def testDeleteIncidentWithAdminUser(self):
        client = Client()

        user = User.objects.create_user(
            username='admin',
            password='admin',
            first_name='admin',
            last_name='admin',
            email='admin@somewhere.com',
            is_staff=True
        )

        client.login(username='admin', password='')

        # Capture number of incidents at the start of the test
        numberOfIncidents = Incident.objects.count();

        incident = Incident.objects.create(
            title='title',
            description='description',
            system=System.objects.create(name='name', description='description'),
            priority='H',
            reportedBy=User.objects.filter(username='admin').get()
        )

        # Verify that the incident has been created and there is
        # now one more in the list of incidents.
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)

        response = client.post("/incidents/" + str(incident.id) + "/updateincident/",
                               {'delete': 'delete'},
                               follow=True)

        # Verify that the delete operations has been called and that
        # the incident has NOT been deleted
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)
        self.assertEquals(str(messages[0]), "Only admin users can delete incidents.")
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())

    def testAssignIncidentWithNotRaisedByCurrentUser(self):
        client = Client()

        user = User.objects.create_user(
            username='harry',
            password='harry',
            first_name='harry',
            last_name='harry',
            email='harry@somewhere.com',
            is_staff=False
        )

        user = User.objects.create_user(
            username='sally',
            password='sally',
            first_name='sally',
            last_name='sally',
            email='sally@somewhere.com',
            is_staff=False
        )

        client.login(username='harry', password='harry')

        # Capture number of incidents at the start of the test
        numberOfIncidents = Incident.objects.count();

        incident = Incident.objects.create(
            title='title',
            description='description',
            system=System.objects.create(name='name', description='description'),
            priority='H',
            ownedBy=None,
            reportedBy=User.objects.filter(username='sally').get()
        )

        # Verify that the incident has been created and there is
        # now one more in the list of incidents.
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)

        response = client.post("/incidents/" + str(incident.id) + "/updateincident/",
                               {'assign': 'assign'},
                               follow=True)

        # Verify that the delete operations has been called and that
        # the incident has NOT been deleted
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)
        self.assertEquals(str(messages[0]), "Incident assigned successfully")
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())
