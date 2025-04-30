from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import MenuTable, BookingTable
from restaurant.serializer import MenuTableSerializer, BookingTableSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User  # <-- Add this import


class MenuViewTest(TestCase):

    def setUp(self):
        """Set up some sample MenuTable instances for testing."""
        self.client = APIClient()

        # Create some menu items for testing
        self.menu1 = MenuTable.objects.create(
            ID=1, Title="Pizza", Price=12.99, Inventory=100
        )
        self.menu2 = MenuTable.objects.create(
            ID=2, Title="Burger", Price=8.99, Inventory=50
        )
        self.menu3 = MenuTable.objects.create(
            ID=3, Title="Pasta", Price=10.99, Inventory=80
        )

    def test_get_all_menus(self):
        """Test retrieving all menu items."""
        response = self.client.get('/menu/items/')
        expected_data = MenuTableSerializer([self.menu1, self.menu2, self.menu3], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_menu_item(self):
        """Test creating a new menu item."""
        new_menu_item = {
            'ID': 4,
            'Title': 'Salad',
            'Price': 6.99,
            'Inventory': 120
        }
        response = self.client.post('/menu/items/', new_menu_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Title'], new_menu_item['Title'])
        self.assertEqual(response.data['Price'], str(new_menu_item['Price']))
        self.assertEqual(response.data['Inventory'], new_menu_item['Inventory'])

    def test_get_single_menu_item(self):
        """Test retrieving a single menu item by ID."""
        response = self.client.get(f'/menu/items/{self.menu1.ID}/')
        expected_data = MenuTableSerializer(self.menu1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_update_menu_item(self):
        """Test updating an existing menu item."""
        updated_menu_item = {
            'ID': self.menu1.ID,
            'Title': 'Updated Pizza',
            'Price': 14.99,
            'Inventory': 90
        }
        response = self.client.put(f'/menu/items/{self.menu1.ID}/', updated_menu_item, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Title'], updated_menu_item['Title'])
        self.assertEqual(response.data['Price'], str(updated_menu_item['Price']))
        self.assertEqual(response.data['Inventory'], updated_menu_item['Inventory'])

    def test_delete_menu_item(self):
        """Test deleting a menu item."""
        response = self.client.delete(f'/menu/items/{self.menu1.ID}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class BookingTableViewTest(TestCase):

    def setUp(self):
        """Set up some sample BookingTable instances for testing."""
        self.client = APIClient()

        # Create some booking tables for testing
        self.booking1 = BookingTable.objects.create(
            Name="John Doe", No_of_guests=4, Booking_date="2025-04-01 18:30:00"
        )
        self.booking2 = BookingTable.objects.create(
            Name="Jane Smith", No_of_guests=2, Booking_date="2025-04-01 19:00:00"
        )
        self.booking3 = BookingTable.objects.create(
            Name="Alice Johnson", No_of_guests=6, Booking_date="2025-04-01 20:00:00"
        )

    def test_get_all_bookings(self):
        """Test retrieving all booking tables."""
        response = self.client.get('/booking/tables/')
        expected_data = BookingTableSerializer([self.booking1, self.booking2, self.booking3], many=True).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_create_booking_table(self):
        """Test creating a new booking table."""
        new_booking = {
            'Name': 'Bob Marley',
            'No_of_guests': 5,
            'Booking_date': '2025-04-01 21:00:00'
        }
        response = self.client.post('/booking/tables/', new_booking, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['Name'], new_booking['Name'])
        self.assertEqual(response.data['No_of_guests'], new_booking['No_of_guests'])
        self.assertEqual(response.data['Booking_date'], new_booking['Booking_date'])

    def test_get_single_booking(self):
        """Test retrieving a single booking table by ID."""
        response = self.client.get(f'/booking/{self.booking1.ID}/')
        expected_data = BookingTableSerializer(self.booking1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_update_booking(self):
        """Test updating an existing booking table."""
        updated_booking = {
            'Name': 'Updated Bob Marley',
            'No_of_guests': 7,
            'Booking_date': '2025-04-01 22:00:00'
        }
        response = self.client.put(f'/booking/{self.booking1.ID}/', updated_booking, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Name'], updated_booking['Name'])
        self.assertEqual(response.data['No_of_guests'], updated_booking['No_of_guests'])
        self.assertEqual(response.data['Booking_date'], updated_booking['Booking_date'])

    def test_delete_booking(self):
        """Test deleting a booking table."""
        response = self.client.delete(f'/booking/{self.booking1.ID}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class AuthTokenTest(TestCase):

    def setUp(self):
        """Set up user and token for authentication testing."""
        self.client = APIClient()
        # Create a user and get an authentication token
        self.user = User.objects.create_user(username='testuser', password='password')
        self.token = Token.objects.create(user=self.user)

    def test_auth_token(self):
        """Test obtaining an authentication token."""
        response = self.client.post('/api-token-auth/', {
            'username': 'testuser',
            'password': 'password'
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)  # Check that the token is in the response

    def test_authenticated_request(self):
        """Test making an authenticated request."""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get('/menu/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
