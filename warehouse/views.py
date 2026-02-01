from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Input
from .forms import InputForm
from datetime import datetime


@login_required
def input_list(request):
    """
    List view for Stock Inputs (Kirim) with date filtering.
    """
    date_str = request.GET.get('date')
    if date_str:
        try:
            date_filter = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date_filter = timezone.now().date()
    else:
        date_filter = timezone.now().date()

    items = Input.objects.filter(
        created_at__date=date_filter).order_by('-created_at')
    total_sum = items.aggregate(Sum('summa'))['summa__sum'] or 0

    context = {
        'items': items,
        'title': 'Kirim (In) List',
        'date_filter': date_filter.strftime('%Y-%m-%d'),
        'total_sum': total_sum,
        'add_url': '/warehouse/add/',
        'detail_url_name': 'input_detail',  # To link in template
        'delete_url_name': 'delete_input',
    }
    return render(request, 'lists/generic_list.html', context)


@login_required
def add_input(request):
    if request.method == 'POST':
        form = InputForm(request.POST)
        if form.is_valid():
            input_obj = form.save(commit=False)
            input_obj.user = request.user
            input_obj.save()
            messages.success(request, 'Stock Input added successfully!')
            return redirect('input_list')
    else:
        form = InputForm()
    return render(request, 'forms/input_form.html', {'form': form, 'title': 'Add Stock (Kirim)'})


@login_required
def input_detail(request, pk):
    """
    View to show details and update Input.
    """
    input_obj = get_object_or_404(Input, pk=pk)

    if request.method == 'POST':
        form = InputForm(request.POST, instance=input_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Stock Input updated successfully!')
            return redirect('input_list')
    else:
        form = InputForm(instance=input_obj)

    return render(request, 'forms/input_form.html', {
        'form': form,
        'title': 'Edit Stock (Kirim)',
        'object': input_obj  # Pass object if needed for extra info
    })


@login_required
def delete_input(request, pk):
    input_obj = get_object_or_404(Input, pk=pk)
    if request.method == 'POST':
        input_obj.delete()
        messages.success(request, 'Stock Input deleted successfully!')
        return redirect('input_list')
    return redirect('input_list')
