from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProductForm, UnitForm


@login_required
def add_product(request):
    if request.method == 'POST':
        # Files for image if add later
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product added successfully!')
            return redirect('dashboard')
    else:
        form = ProductForm()
    return render(request, 'forms/product_form.html', {'form': form, 'title': 'Add Product'})


@login_required
def add_unit(request):
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Unit added successfully!')
            return redirect('dashboard')
    else:
        form = UnitForm()
    return render(request, 'forms/unit_form.html', {'form': form, 'title': 'Add Unit'})
