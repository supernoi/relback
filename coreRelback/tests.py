from django.test import TestCase

class unitTestCase(TestCase):

    def testHomePageTemplate(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def testClientPageTemplate(self):
        response = self.client.get('/client/')
        self.assertTemplateUsed(response, 'clients.html')

    def testHostPageTemplate(self):
        response = self.client.get('/host/')
        self.assertTemplateUsed(response, 'hosts.html')

    def testDatabasePageTemplate(self):
        response = self.client.get('/database/')
        self.assertTemplateUsed(response, 'databases.html')

    def testPolicyPageTemplate(self):
        response = self.client.get('/policies/')
        self.assertTemplateUsed(response, 'policies.html')
        