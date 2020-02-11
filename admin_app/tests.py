from django.test import TestCase
from admin_app.models import Activity

# Create your tests here.

class ActivityTestCase(TestCase):
    def setUp(self):
        Activity.objects.create(
            title = "Test activity",
            overview_paragraph = "This is only a test",
        )

    def test_activity_exists(self):
        """Just checks that my test activity exists"""
        test = Activity.objects.get(title="Test activity")
        self.assertEqual(test.overview, 'This is only a test')
