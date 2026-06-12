import os
import django
from django.test import Client
from django.urls import reverse
from bs4 import BeautifulSoup

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'society_management.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

def inspect_page(client, url, role, description):
    print(f"\n--- Fetching {description} ({url}) as {role} ---")
    response = client.get(url, follow=True)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Get title
        title = soup.title.string.strip() if soup.title else "No Title"
        print(f"Page Title: {title}")
        
        # Find all card headings or main headers
        headers = [h.get_text().strip() for h in soup.find_all(['h3', 'h4', 'h5', 'h6'])]
        print(f"Key Headings: {headers[:8]}")
        
        # Check for alert boxes
        alerts = [div.get_text().strip() for div in soup.find_all(class_='alert')]
        if alerts:
            print(f"Alerts present: {alerts}")
            
        # Check for tables or logs
        tables = soup.find_all('table')
        if tables:
            print(f"Tables found: {len(tables)} table(s)")
            for i, table in enumerate(tables):
                headers = [th.get_text().strip() for th in table.find_all('th')]
                print(f"  Table {i+1} Columns: {headers}")
    else:
        print("Failed to load page content.")

def main():
    client = Client()
    
    # Check if admin user exists, if not seed
    if not User.objects.filter(username='admin').exists():
        import seed_data
        seed_data.seed()
        
    # Test 1: Admin workflow
    print("LOGGING IN AS ADMIN...")
    login_success = client.login(username='admin', password='admin123')
    print(f"Login successful: {login_success}")
    
    inspect_page(client, '/admin-dashboard/', 'ADMIN', 'Admin Dashboard')
    inspect_page(client, '/residents/', 'ADMIN', 'Resident List')
    inspect_page(client, '/notices/', 'ADMIN', 'Notice Board')
    inspect_page(client, '/maintenance/', 'ADMIN', 'Maintenance Bills')
    inspect_page(client, '/complaints/', 'ADMIN', 'Complaints Log')
    inspect_page(client, '/visitors/', 'ADMIN', 'Visitor Log')
    
    client.logout()
    
    # Test 2: Resident workflow
    print("\nLOGGING IN AS RESIDENT...")
    login_success = client.login(username='resident1', password='resident123')
    print(f"Login successful: {login_success}")
    
    inspect_page(client, '/resident/', 'RESIDENT', 'Resident Dashboard')
    inspect_page(client, '/notices/', 'RESIDENT', 'Notice Board')
    inspect_page(client, '/maintenance/', 'RESIDENT', 'My Maintenance Bills')
    inspect_page(client, '/complaints/', 'RESIDENT', 'My Complaints')
    inspect_page(client, '/visitors/', 'RESIDENT', 'My Visitors')
    
if __name__ == '__main__':
    main()
