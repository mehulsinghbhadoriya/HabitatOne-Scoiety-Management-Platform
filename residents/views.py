from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from accounts.decorators import admin_required
from .models import Resident
from .forms import ResidentForm, ResidentEditForm

User = get_user_model()

@login_required
@admin_required
def resident_list(request):
    # Order by flat number
    residents = Resident.objects.all().select_related('user').order_by('flat_number')
    return render(request, 'residents/list.html', {'residents': residents})

@login_required
@admin_required
def resident_create(request):
    if request.method == 'POST':
        form = ResidentForm(request.POST)
        if form.is_valid():
            # 1. Create the User
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='RESIDENT'
            )
            
            # 2. Create the Resident profile linked to that user
            resident = form.save(commit=False)
            resident.user = user
            resident.save()
            
            messages.success(request, f"Resident {user.get_full_name()} (Flat {resident.flat_number}) created successfully.")
            return redirect('residents:list')
    else:
        form = ResidentForm()
    return render(request, 'residents/form.html', {'form': form, 'title': 'Add New Resident'})

@login_required
@admin_required
def resident_edit(request, pk):
    resident = get_object_or_404(Resident, pk=pk)
    if request.method == 'POST':
        form = ResidentEditForm(request.POST, instance=resident)
        if form.is_valid():
            # 1. Update the User profile
            user = resident.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            if password:
                user.set_password(password)
            user.save()
            
            # 2. Update the Resident
            form.save()
            
            messages.success(request, f"Resident {user.get_full_name()} details updated successfully.")
            return redirect('residents:list')
    else:
        form = ResidentEditForm(instance=resident)
    return render(request, 'residents/form.html', {'form': form, 'title': 'Edit Resident'})

@login_required
@admin_required
def resident_delete(request, pk):
    resident = get_object_or_404(Resident, pk=pk)
    user = resident.user
    if request.method == 'POST':
        user.delete() # Will delete resident profile cascade
        messages.success(request, f"Resident profile for {user.username} deleted successfully.")
        return redirect('residents:list')
    return render(request, 'residents/confirm_delete.html', {'resident': resident})

@login_required
def resident_detail(request, pk):
    resident = get_object_or_404(Resident, pk=pk)
    # Check if the user is admin or is viewing their own profile
    if request.user.role != 'ADMIN' and request.user != resident.user:
        raise PermissionDenied
    return render(request, 'residents/detail.html', {'resident': resident})
