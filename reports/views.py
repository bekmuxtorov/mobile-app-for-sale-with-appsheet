from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse
from django.db.models import Sum, Q, F
from orders.models import Output
from warehouse.models import Input
from users.models import Customer
from products.models import Product
from datetime import datetime
import openpyxl


def parse_datetime_input(date_str):
    """
    Helper to parse datetime string from HTML5 datetime-local input.
    Tries format with seconds first, then without.
    Returns timezone-aware datetime or None on failure.
    """
    if not date_str:
        return None

    # List of formats to try
    formats = ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M']

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
            return dt
        except ValueError:
            continue
    return None


@login_required
def customer_sales_report(request):
    """
    Report: Sales by Customer with DateTime Filter.
    """
    # Get params
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    customer_id = request.GET.get('customer')

    # Defaults
    now = timezone.now()

    # Parse Start Date
    start_date = parse_datetime_input(start_date_str)
    if not start_date:
        start_date = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

    # Parse End Date
    end_date = parse_datetime_input(end_date_str)
    if not end_date:
        end_date = now

    # Helper for template (string format for input value) - include seconds for 24h precision
    start_date_convert = start_date.strftime('%Y-%m-%dT%H:%M:%S')
    end_date_convert = end_date.strftime('%Y-%m-%dT%H:%M:%S')

    # Query
    query = Output.objects.filter(
        created_at__gte=start_date,
        created_at__lte=end_date
    ).select_related('product', 'product__unit', 'customer')

    # Filter by Customer
    if customer_id:
        query = query.filter(customer_id=customer_id)

    # Order
    items = query.order_by('-created_at')

    # Export to Excel
    if request.GET.get('export') == 'excel':
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename=Sales_Report_{start_date.strftime("%Y%m%d_%H%M%S")}_{end_date.strftime("%Y%m%d_%H%M%S")}.xlsx'

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Sales Report"

        # Headers
        headers = ['Sana', 'Mijoz', 'Mahsulot',
                   'Soni', 'Narxi', 'Jami Summa', 'Holati']
        ws.append(headers)

        total_sum_excel = 0
        for item in items:
            status = "To'langan" if item.is_payment else "Qarz"
            row = [
                item.created_at.strftime('%d/%m/%Y %H:%M:%S'),
                item.customer.full_name,
                item.product.name,
                float(item.quantity),
                float(item.price),
                float(item.summa or 0),
                status
            ]
            ws.append(row)
            total_sum_excel += (item.summa or 0)

        # Total Row
        ws.append(['', '', '', '', 'JAMI:', float(total_sum_excel), ''])

        wb.save(response)
        return response

    # Render Template
    customers = Customer.objects.all()

    # Calculate Totals
    total_sum = 0
    total_unpaid = 0

    for item in items:
        s = item.summa or 0
        total_sum += s
        if not item.is_payment:
            total_unpaid += s

    total_paid = total_sum - total_unpaid

    context = {
        'items': items,
        'customers': customers,
        'start_date': start_date_convert,
        'end_date': end_date_convert,
        'selected_customer': int(customer_id) if customer_id else None,
        'total_sum': total_sum,
        'total_unpaid': total_unpaid,
        'total_paid': total_paid,
        'title': 'Mijozlar hisoboti'
    }
    return render(request, 'reports/customer_sales_report.html', context)


@login_required
def product_sales_report(request):
    """
    Report: Product Turnover (Input vs Output) with DateTime Filter.
    Aggregates data per Product.
    """
    # Get params
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    product_id = request.GET.get('product')

    # Defaults
    now = timezone.now()

    # Parse Start Date
    start_date = parse_datetime_input(start_date_str)
    if not start_date:
        # Default: 1st of current month at 00:00:00
        start_date = now.replace(
            day=1, hour=0, minute=0, second=0, microsecond=0)

    # Parse End Date
    end_date = parse_datetime_input(end_date_str)
    if not end_date:
        # Default: Now (end of period)
        end_date = now

    # Helper for template
    start_date_convert = start_date.strftime('%Y-%m-%dT%H:%M:%S')
    end_date_convert = end_date.strftime('%Y-%m-%dT%H:%M:%S')

    # Get Products (filtered if selected)
    products = Product.objects.all().select_related('unit')
    if product_id:
        products = products.filter(id=product_id)

    report_data = []

    grand_total_in_sum = 0
    grand_total_out_sum = 0

    for product in products:
        # Inputs (Kirim) in period
        inputs = Input.objects.filter(
            product=product,
            created_at__gte=start_date,
            created_at__lte=end_date
        ).aggregate(
            qty=Sum('quantity'),
            total=Sum('summa')
        )
        in_qty = inputs['qty'] or 0
        in_sum = inputs['total'] or 0
        in_price = (in_sum / in_qty) if in_qty > 0 else 0

        # Outputs (Chiqim) in period
        outputs = Output.objects.filter(
            product=product,
            created_at__gte=start_date,
            created_at__lte=end_date
        ).aggregate(
            qty=Sum('quantity'),
            total=Sum('summa')
        )
        out_qty = outputs['qty'] or 0
        out_sum = outputs['total'] or 0
        out_price = (out_sum / out_qty) if out_qty > 0 else 0

        # Remaining (Stock) - Current Actual Stock
        all_time_in = Input.objects.filter(product=product).aggregate(
            Sum('quantity'))['quantity__sum'] or 0
        all_time_out = Output.objects.filter(product=product).aggregate(
            Sum('quantity'))['quantity__sum'] or 0
        current_stock = all_time_in - all_time_out

        # Determine if we should show this row
        # Show if there is activity in period OR if there is stock remaining
        has_activity = (in_qty > 0 or out_qty > 0)
        has_stock = (current_stock != 0)

        # If user picked a specific product, show it even if empty
        is_selected = (str(product.id) == str(product_id))

        if has_activity or has_stock or is_selected:
            report_data.append({
                'product': product,
                'in_qty': in_qty,
                'in_sum': in_sum,
                'in_price': in_price,
                'out_qty': out_qty,
                'out_sum': out_sum,
                'out_price': out_price,
                'remaining': current_stock
            })
            grand_total_in_sum += in_sum
            grand_total_out_sum += out_sum

    # Export to Excel
    if request.GET.get('export') == 'excel':
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response[
            'Content-Disposition'] = f'attachment; filename=Turnover_Report_{start_date.strftime("%Y%m%d_%H%M%S")}_{end_date.strftime("%Y%m%d_%H%M%S")}.xlsx'

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Turnover Report"

        # Headers
        headers = [
            'Tovar',
            'Kirim Soni', 'Kirim Narxi (O\'rt)', 'Kirim Jami',
            'Chiqim Soni', 'Chiqim Narxi (O\'rt)', 'Chiqim Jami',
            'Qolgan Soni'
        ]
        ws.append(headers)

        for row_data in report_data:
            row = [
                row_data['product'].name,
                float(row_data['in_qty']),
                float(row_data['in_price']),
                float(row_data['in_sum']),
                float(row_data['out_qty']),
                float(row_data['out_price']),
                float(row_data['out_sum']),
                float(row_data['remaining'])
            ]
            ws.append(row)

        # Total Row
        ws.append(['JAMI:', '', '', float(grand_total_in_sum),
                  '', '', float(grand_total_out_sum), ''])

        wb.save(response)
        return response

    print(f"DEBUG: Product Report - Found {len(report_data)} items")
    context = {
        'report_data': report_data,
        'products': Product.objects.all(),  # For filter dropdown
        'start_date': start_date_convert,
        'end_date': end_date_convert,
        'selected_product': int(product_id) if product_id else None,
        'grand_total_in_sum': grand_total_in_sum,
        'grand_total_out_sum': grand_total_out_sum,
        'title': 'Tovar aylanma hisoboti'
    }
    return render(request, 'reports/product_sales_report.html', context)
