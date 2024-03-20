from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User
from incidents.models import Incident, System, Status, Priority


class TestUnassignIncidents(TestCase):

    def testUnassignIncidentWithUserLoggedInAsAdmin(self):
        client = Client()

        user = User.objects.create_user(
            username='admin',
            password='admin',
            first_name='admin',
            last_name='admin',
            email='admin@somewhere.com',
            is_staff=True
        )

        user = User.objects.create_user(
            username='sally',
            password='sally',
            first_name='sally',
            last_name='sally',
            email='sally@somewhere.com',
            is_staff=False
        )

        client.login(username='admin', password='admin')

        # Capture number of incidents at the start of the test
        numberOfIncidents = Incident.objects.count();

        incident = Incident.objects.create(
            title='title',
            description='description',
            system=System.objects.create(name='name', description='description'),
            priority='H',
            ownedBy=User.objects.filter(username='sally').get(),
            reportedBy=User.objects.filter(username='sally').get(),
            status="IP"
        )

        # Verify that the incident has been created and there is
        # now one more in the list of incidents.
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)

        response = client.post("/incidents/" + str(incident.id) + "/updateincident/",
                               {'unassign': 'unassign'},
                               follow=True)

        # Verify that the delete operations has been called and that
        # the incident has NOT been deleted
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)
        self.assertEquals(str(messages[0]), "Incident unassigned successfully")
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())

    def testUnassignIncidentWithUserAsAdminButStatusNotInProgress(self):
        client = Client()

        user = User.objects.create_user(
            username='admin',
            password='admin',
            first_name='admin',
            last_name='admin',
            email='admin@somewhere.com',
            is_staff=True
        )

        user = User.objects.create_user(
            username='sally',
            password='sally',
            first_name='sally',
            last_name='sally',
            email='sally@somewhere.com',
            is_staff=False
        )

        client.login(username='admin', password='admin')

        # Capture number of incidents at the start of the test
        numberOfIncidents = Incident.objects.count();

        incident = Incident.objects.create(
            title='title',
            description='description',
            system=System.objects.create(name='name', description='description'),
            priority='H',
            ownedBy=User.objects.filter(username='sally').get(),
            reportedBy=User.objects.filter(username='sally').get(),
            status="UA"
        )

        # Verify that the incident has been created and there is
        # now one more in the list of incidents.
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)

        response = client.post("/incidents/" + str(incident.id) + "/updateincident/",
                               {'unassign': 'unassign'},
                               follow=True)

        # Verify that the delete operations has been called and that
        # the incident has NOT been deleted
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)
        self.assertEquals(str(messages[0]), "This incident is not in-progress")
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())

    def testUnassignIncidentWithUserNotAdmin(self):
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
            ownedBy=User.objects.filter(username='harry').get(),
            reportedBy=User.objects.filter(username='sally').get(),
            status="IP"
        )

        # Verify that the incident has been created and there is
        # now one more in the list of incidents.
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)

        response = client.post("/incidents/" + str(incident.id) + "/updateincident/",
                               {'unassign': 'unassign'},
                               follow=True)

        # Verify that the delete operations has been called and that
        # the incident has NOT been deleted
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEquals(Incident.objects.count(), numberOfIncidents + 1)
        self.assertEquals(str(messages[0]), "Incident can only be unassigned by Admin")
        self.assertTrue(Incident.objects.filter(id=incident.id).exists())

