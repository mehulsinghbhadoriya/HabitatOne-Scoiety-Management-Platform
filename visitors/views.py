from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Visitor
from .forms import VisitorForm

@login_required
def visitor_list(request):
    if request.user.role == 'ADMIN':
        # Admin / Security see all visitors, ordered by date
        visitors = Visitor.objects.all().select_related('resident__user').order_by('-visit_date')
        return render(request, 'visitors/admin_list.html', {'visitors': visitors})
    else:
        # Residents only see their own logged visitors
        resident = getattr(request.user, 'resident_profile', None)
        if not resident:
            visitors = []
        else:
            visitors = Visitor.objects.filter(resident=resident).order_by('-visit_date')
        return render(request, 'visitors/list.html', {'visitors': visitors})

@login_required
def visitor_create(request):
    if request.user.role != 'RESIDENT':
        messages.error(request, "Only residents can pre-register visitors.")
        return redirect('visitors:list')

    resident = getattr(request.user, 'resident_profile', None)
    if not resident:
        messages.error(request, "Resident profile not found.")
        return redirect('dashboard:home')

    if request.method == 'POST':
        form = VisitorForm(request.POST)
        if form.is_valid():
            visitor = form.save(commit=False)
            visitor.resident = resident
            visitor.save()
            messages.success(request, "Visitor pre-registered successfully.")
            return redirect('visitors:list')
    else:
        form = VisitorForm()
    return render(request, 'visitors/form.html', {'form': form})
