from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Output
from .forms import OutputForm
from datetime import datetime


@login_required
def output_list(request):
    """
    List view for Sales Outputs (Chiqim) with date filtering.
    """
    date_str = request.GET.get('date')
    if date_str:
        try:
            date_filter = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            date_filter = timezone.now().date()
    else:
        date_filter = timezone.now().date()

    items = Output.objects.filter(
        created_at__date=date_filter).order_by('-created_at')
    total_sum = items.aggregate(Sum('summa'))['summa__sum'] or 0

    context = {
        'items': items,
        'title': 'Chiqim (Out) List',
        'date_filter': date_filter.strftime('%Y-%m-%d'),
        'total_sum': total_sum,
        'add_url': '/orders/add/',
        'detail_url_name': 'output_detail',  # To link in template
        'delete_url_name': 'delete_output',
    }
    return render(request, 'lists/generic_list.html', context)


@login_required
def add_output(request):
    if request.method == 'POST':
        form = OutputForm(request.POST)
        if form.is_valid():
            output_obj = form.save(commit=False)
            output_obj.user = request.user
            output_obj.save()
            messages.success(request, 'Sale Output added successfully!')
            return redirect('output_list')
    else:
        form = OutputForm()
    return render(request, 'forms/output_form.html', {'form': form, 'title': 'Add Sale (Chiqim)'})


@login_required
def output_detail(request, pk):
    """
    View to show details and update Output.
    """
    output_obj = get_object_or_404(Output, pk=pk)

    if request.method == 'POST':
        form = OutputForm(request.POST, instance=output_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sale updated successfully!')
            return redirect('output_list')
    else:
        form = OutputForm(instance=output_obj)

    return render(request, 'forms/output_form.html', {
        'form': form,
        'title': 'Edit Sale (Chiqim)',
        'object': output_obj
    })


@login_required
def delete_output(request, pk):
    output_obj = get_object_or_404(Output, pk=pk)
    if request.method == 'POST':
        output_obj.delete()
        messages.success(request, 'Sale Output deleted successfully!')
        return redirect('output_list')
    return redirect('output_list')
