from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from accounts.decorators import admin_required
from .models import Complaint
from .forms import ComplaintForm, ComplaintStatusForm

@login_required
def complaint_list(request):
    if request.user.role == 'ADMIN':
        complaints = Complaint.objects.all().select_related('resident__user').order_by('-created_at')
        # We will also pass the status form so they can update status inline or on a detail/update page
        return render(request, 'complaints/admin_list.html', {'complaints': complaints})
    else:
        resident = getattr(request.user, 'resident_profile', None)
        if not resident:
            complaints = []
        else:
            complaints = Complaint.objects.filter(resident=resident).order_by('-created_at')
        return render(request, 'complaints/list.html', {'complaints': complaints})

@login_required
def complaint_create(request):
    # Only residents should create complaints
    if request.user.role != 'RESIDENT':
        messages.error(request, "Only residents can file complaints.")
        return redirect('complaints:list')
        
    resident = getattr(request.user, 'resident_profile', None)
    if not resident:
        messages.error(request, "Resident profile not found.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.resident = resident
            complaint.save()
            messages.success(request, "Complaint raised successfully.")
            return redirect('complaints:list')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/form.html', {'form': form})

@login_required
@admin_required
def complaint_update_status(request, pk):
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = ComplaintStatusForm(request.POST, instance=complaint)
        if form.is_valid():
            form.save()
            messages.success(request, f"Complaint status updated to {complaint.get_status_display()}.")
            return redirect('complaints:list')
    else:
        form = ComplaintStatusForm(instance=complaint)
    return render(request, 'complaints/update_status.html', {'form': form, 'complaint': complaint})
