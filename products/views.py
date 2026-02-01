from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Unit


@login_required
def add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        unit_id = request.POST.get('unit')
        price = request.POST.get('price')
        description = request.POST.get('description')

        unit = Unit.objects.filter(id=unit_id).first() if unit_id else None

        Product.objects.create(
            name=name,
            unit=unit,
            price=price or 0,
            description=description
        )
        messages.success(request, 'Product added successfully!')
        # Redirect to list instead of dashboard for better flow
        return redirect('product_list')

    units = Unit.objects.all()
    return render(request, 'products/add_product.html', {'units': units})


@login_required
def product_list(request):
    products = Product.objects.select_related(
        'unit').all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        unit_id = request.POST.get('unit')
        product.price = request.POST.get('price') or 0
        product.description = request.POST.get('description')

        if unit_id:
            product.unit = Unit.objects.filter(id=unit_id).first()
        else:
            product.unit = None

        product.save()
        messages.success(request, 'Product updated successfully!')
        return redirect('product_list')

    units = Unit.objects.all()
    return render(request, 'products/product_detail.html', {'product': product, 'units': units})


@login_required
def add_unit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')

        Unit.objects.create(
            name=name,
            description=description
        )
        messages.success(request, 'Unit added successfully!')
        return redirect('unit_list')  # Redirect to list
    return render(request, 'products/add_unit.html')


@login_required
def unit_list(request):
    units = Unit.objects.all().order_by('-created_at')
    return render(request, 'products/unit_list.html', {'units': units})


@login_required
def unit_detail(request, pk):
    unit = get_object_or_404(Unit, pk=pk)
    if request.method == 'POST':
        unit.name = request.POST.get('name')
        unit.description = request.POST.get('description')
        unit.save()
        messages.success(request, 'Unit updated successfully!')
        return redirect('unit_list')
    return render(request, 'products/unit_detail.html', {'unit': unit})
