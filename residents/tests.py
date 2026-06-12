from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from residents.models import Resident
from notices.models import Notice
from maintenance.models import MaintenanceBill
from complaints.models import Complaint
from visitors.models import Visitor
import datetime

User = get_user_model()

class SocietyManagementTests(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = User.objects.create_user(
            username='admin_test',
            password='admin123_password',
            email='admin_test@test.com',
            role='ADMIN'
        )

        # Create a resident user
        self.resident_user = User.objects.create_user(
            username='resident_test',
            password='resident123_password',
            email='resident_test@test.com',
            role='RESIDENT'
        )
        self.resident_profile = Resident.objects.create(
            user=self.resident_user,
            flat_number='101-A',
            phone='1234567890',
            family_members=3,
            move_in_date=datetime.date.today()
        )

    def test_user_roles(self):
        self.assertTrue(self.admin_user.is_admin_role())
        self.assertFalse(self.admin_user.is_resident_role())
        self.assertTrue(self.resident_user.is_resident_role())
        self.assertFalse(self.resident_user.is_admin_role())

    def test_dashboard_redirection(self):
        # Test admin dashboard redirection
        self.client.login(username='admin_test', password='admin123_password')
        response = self.client.get(reverse('dashboard:home'))
        self.assertRedirects(response, reverse('dashboard:admin_home'))

        # Test resident dashboard redirection
        self.client.login(username='resident_test', password='resident123_password')
        response = self.client.get(reverse('dashboard:home'))
        self.assertRedirects(response, reverse('dashboard:resident_home'))

    def test_resident_management_permissions(self):
        # Resident trying to view resident list should receive a 403 (PermissionDenied)
        self.client.login(username='resident_test', password='resident123_password')
        response = self.client.get(reverse('residents:list'))
        self.assertEqual(response.status_code, 403)

        # Admin can view resident list
        self.client.login(username='admin_test', password='admin123_password')
        response = self.client.get(reverse('residents:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '101-A')

    def test_resident_create(self):
        self.client.login(username='admin_test', password='admin123_password')
        post_data = {
            'username': 'new_resident',
            'email': 'new@test.com',
            'password': 'password123',
            'first_name': 'New',
            'last_name': 'User',
            'flat_number': '102-B',
            'phone': '0987654321',
            'family_members': 2,
            'move_in_date': '2026-05-30'
        }
        response = self.client.post(reverse('residents:create'), post_data)
        self.assertRedirects(response, reverse('residents:list'))
        self.assertTrue(User.objects.filter(username='new_resident').exists())
        self.assertTrue(Resident.objects.filter(flat_number='102-B').exists())

    def test_notice_board(self):
        self.client.login(username='admin_test', password='admin123_password')
        notice = Notice.objects.create(
            title="Scheduled Power Cut",
            description="Power cut for 2 hours on Sunday."
        )
        
        # Test viewing notices
        response = self.client.get(reverse('notices:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Scheduled Power Cut")

        # Test creating notice (admin only)
        post_data = {
            'title': 'New Notice Title',
            'description': 'Description content'
        }
        response = self.client.post(reverse('notices:create'), post_data)
        self.assertRedirects(response, reverse('notices:list'))
        self.assertTrue(Notice.objects.filter(title='New Notice Title').exists())

    def test_complaints(self):
        # Resident raises complaint
        self.client.login(username='resident_test', password='resident123_password')
        post_data = {
            'subject': 'Tap Leakage',
            'description': 'Water tap is dripping in bathroom.'
        }
        response = self.client.post(reverse('complaints:create'), post_data)
        self.assertRedirects(response, reverse('complaints:list'))
        self.assertTrue(Complaint.objects.filter(subject='Tap Leakage').exists())

        # Admin updates complaint status
        complaint = Complaint.objects.create(
            resident=self.resident_profile,
            subject='Geyser broken',
            description='Geyser does not heat.'
        )
        self.client.login(username='admin_test', password='admin123_password')
        response = self.client.post(reverse('complaints:update_status', args=[complaint.pk]), {'status': 'RESOLVED'})
        self.assertRedirects(response, reverse('complaints:list'))
        complaint.refresh_from_db()
        self.assertEqual(complaint.status, 'RESOLVED')

    def test_maintenance_dues(self):
        # Admin creates a maintenance bill
        self.client.login(username='admin_test', password='admin123_password')
        bill = MaintenanceBill.objects.create(
            resident=self.resident_profile,
            amount=250.00,
            due_date=datetime.date.today(),
            status='PENDING'
        )

        # Resident views list and sees dues
        self.client.login(username='resident_test', password='resident123_password')
        response = self.client.get(reverse('maintenance:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '250.00')

        # Resident marks as paid
        response = self.client.get(reverse('maintenance:mark_paid', args=[bill.pk]))
        self.assertRedirects(response, reverse('maintenance:list'))
        bill.refresh_from_db()
        self.assertEqual(bill.status, 'PAID')

    def test_visitor_management(self):
        # Resident registers a visitor
        self.client.login(username='resident_test', password='resident123_password')
        post_data = {
            'visitor_name': 'John Delivery',
            'visit_date': '2026-06-01',
            'purpose': 'Courier'
        }
        response = self.client.post(reverse('visitors:create'), post_data)
        self.assertRedirects(response, reverse('visitors:list'))
        self.assertTrue(Visitor.objects.filter(visitor_name='John Delivery').exists())
