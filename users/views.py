from django.shortcuts import render, redirect, get_object_or_404
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

    context = {
        'customer_count': Customer.objects.count(),
        'today_output': today_output,
        'total_input': total_input,
    }
    return render(request, 'dashboard.html', context)


@login_required
def add_customer(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        description = request.POST.get('description')

        Customer.objects.create(
            full_name=full_name,
            phone_number=phone_number,
            address=address,
            description=description
        )
        messages.success(request, 'Customer added successfully!')
        return redirect('dashboard')
    return render(request, 'users/add_customer.html')


@login_required
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'users/customer_list.html', {'customers': customers})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.full_name = request.POST.get('full_name')
        customer.phone_number = request.POST.get('phone_number')
        customer.address = request.POST.get('address')
        customer.description = request.POST.get('description')
        customer.save()
        messages.success(request, 'Customer updated successfully!')
        return redirect('customer_list')
    return render(request, 'users/customer_detail.html', {'customer': customer})
