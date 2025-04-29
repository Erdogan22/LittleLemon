from django.test import TestCase
from restaurant.models import Menu

class TestMenuItem(TestCase):
    def test_get_item(self):
        # Create a Menu object
        item = Menu.objects.create(title="IceCream", price=80, inventory=100)
        
        # Assert that the string representation matches the expected value
        self.assertEqual(str(item), "IceCream : 80")