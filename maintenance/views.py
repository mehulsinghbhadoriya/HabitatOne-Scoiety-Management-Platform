from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from accounts.decorators import admin_required
from .models import MaintenanceBill
from .forms import MaintenanceBillForm
from residents.models import Resident

@login_required
def bill_list(request):
    if request.user.role == 'ADMIN':
        bills = MaintenanceBill.objects.all().select_related('resident__user').order_by('-due_date')
        return render(request, 'maintenance/admin_list.html', {'bills': bills})
    else:
        # Resident view
        resident = getattr(request.user, 'resident_profile', None)
        if not resident:
            bills = []
            pending_dues = 0
        else:
            bills = MaintenanceBill.objects.filter(resident=resident).order_by('-due_date')
            from django.db.models import Sum
            pending_dues = bills.filter(status='PENDING').aggregate(total=Sum('amount'))['total'] or 0
        return render(request, 'maintenance/list.html', {'bills': bills, 'pending_dues': pending_dues})

@login_required
@admin_required
def bill_create(request):
    if request.method == 'POST':
        form = MaintenanceBillForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Maintenance bill created successfully.")
            return redirect('maintenance:list')
    else:
        resident_id = request.GET.get('resident')
        initial_data = {}
        if resident_id:
            initial_data['resident'] = resident_id
        form = MaintenanceBillForm(initial=initial_data)
    return render(request, 'maintenance/form.html', {'form': form, 'title': 'Create Maintenance Bill'})

@login_required
@admin_required
def bill_edit(request, pk):
    bill = get_object_or_404(MaintenanceBill, pk=pk)
    if request.method == 'POST':
        form = MaintenanceBillForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            messages.success(request, "Maintenance bill updated successfully.")
            return redirect('maintenance:list')
    else:
        form = MaintenanceBillForm(instance=bill)
    return render(request, 'maintenance/form.html', {'form': form, 'title': 'Edit Maintenance Bill'})

@login_required
@admin_required
def bill_delete(request, pk):
    bill = get_object_or_404(MaintenanceBill, pk=pk)
    if request.method == 'POST':
        bill.delete()
        messages.success(request, "Maintenance bill deleted successfully.")
        return redirect('maintenance:list')
    return render(request, 'maintenance/confirm_delete.html', {'bill': bill})

@login_required
def mark_paid(request, pk):
    bill = get_object_or_404(MaintenanceBill, pk=pk)
    # Validate access: either admin, or the resident owning this bill
    if request.user.role != 'ADMIN' and (not hasattr(request.user, 'resident_profile') or request.user.resident_profile != bill.resident):
        raise PermissionDenied
        
    bill.status = 'PAID'
    bill.save()
    messages.success(request, f"Bill of amount ${bill.amount} marked as Paid.")
    return redirect('maintenance:list')
