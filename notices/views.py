from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import admin_required
from .models import Notice
from .forms import NoticeForm

@login_required
def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notices/list.html', {'notices': notices})

@login_required
@admin_required
def notice_create(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice posted successfully on the notice board.")
            return redirect('notices:list')
    else:
        form = NoticeForm()
    return render(request, 'notices/form.html', {'form': form, 'title': 'Create Notice'})

@login_required
@admin_required
def notice_edit(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            messages.success(request, "Notice updated successfully.")
            return redirect('notices:list')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'notices/form.html', {'form': form, 'title': 'Edit Notice'})

@login_required
@admin_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.delete()
        messages.success(request, "Notice deleted successfully.")
        return redirect('notices:list')
    return render(request, 'notices/confirm_delete.html', {'notice': notice})
