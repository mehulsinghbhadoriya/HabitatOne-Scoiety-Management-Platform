from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from accounts.decorators import admin_required
from residents.models import Resident
from notices.models import Notice
from maintenance.models import MaintenanceBill
from complaints.models import Complaint
from visitors.models import Visitor
import datetime

@login_required
def home(request):
    if request.user.role == 'ADMIN':
        return redirect('dashboard:admin_home')
    return redirect('dashboard:resident_home')

@login_required
@admin_required
def admin_home(request):
    total_residents = Resident.objects.count()
    total_complaints = Complaint.objects.count()
    pending_complaints = Complaint.objects.exclude(status='RESOLVED').count()
    
    # Maintenance collection summary
    maintenance_summary = MaintenanceBill.objects.values('status').annotate(total_amount=Sum('amount'))
    paid_sum = 0
    pending_sum = 0
    for entry in maintenance_summary:
        if entry['status'] == 'PAID':
            paid_sum = entry['total_amount'] or 0
        elif entry['status'] == 'PENDING':
            pending_sum = entry['total_amount'] or 0
            
    recent_notices = Notice.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_residents': total_residents,
        'total_complaints': total_complaints,
        'pending_complaints': pending_complaints,
        'paid_sum': paid_sum,
        'pending_sum': pending_sum,
        'recent_notices': recent_notices,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def resident_home(request):
    resident = getattr(request.user, 'resident_profile', None)
    if not resident:
        messages.error(request, "Resident profile details not found. Please contact administration.")
        # If no profile, we can display a limited screen
        return render(request, 'dashboard/resident_dashboard.html', {'no_profile': True})

    # Pending dues
    pending_dues = MaintenanceBill.objects.filter(resident=resident, status='PENDING').aggregate(total=Sum('amount'))['total'] or 0
    
    # My complaints
    my_complaints_count = Complaint.objects.filter(resident=resident).count()
    
    # Recent notices
    recent_notices = Notice.objects.all().order_by('-created_at')[:5]
    
    # Upcoming visitors
    today = datetime.date.today()
    upcoming_visitors = Visitor.objects.filter(resident=resident, visit_date__gte=today).order_by('visit_date')
    
    context = {
        'resident': resident,
        'pending_dues': pending_dues,
        'my_complaints_count': my_complaints_count,
        'recent_notices': recent_notices,
        'upcoming_visitors': upcoming_visitors,
        'no_profile': False,
    }
    return render(request, 'dashboard/resident_dashboard.html', context)
