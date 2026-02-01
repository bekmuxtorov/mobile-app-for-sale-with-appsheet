from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Customer
from .forms import CustomerForm
from warehouse.models import Input
from orders.models import Output


@login_required
def dashboard(request):
    """
    Main dashboard view.
    """
    today = timezone.now().date()

    # Today's stats
    today_output = Output.objects.filter(
        created_at__date=today).aggregate(Sum('summa'))['summa__sum'] or 0
    # today_input is needed if we still want to show it, but user asked for Total Input in the slot.
    # Let's keep calculating it just in case, but prioritize Total.

    # All-time stats
    total_input = Input.objects.aggregate(Sum('summa'))['summa__sum'] or 0
    total_output = Output.objects.aggregate(Sum('summa'))['summa__sum'] or 0

    # "Umumiy farq = kirim minus chiqim"
    # This represents the "Value of goods remaining" (roughly) or "Net Investment"
    general_diff = total_input - total_output

    context = {
        'customer_count': Customer.objects.count(),
        'today_output': today_output,  # Hero Number (Bugungi Savdo)
        'total_input': total_input,   # Left Small (Umumiy Kirim)
        'general_diff': general_diff,  # Right Small (Kirim - Chiqim)
    }
    return render(request, 'dashboard.html', context)


@login_required
def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Customer added successfully!')
            return redirect('dashboard')
    else:
        form = CustomerForm()
    return render(request, 'forms/customer_form.html', {'form': form, 'title': 'Add Customer'})
