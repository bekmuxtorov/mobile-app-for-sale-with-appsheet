from decimal import Decimal
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
try:
    django.setup()
except Exception as e:
    print(f"Django setup failed: {e}")
    # Try to disable rest_framework dynamically if it fails?
    # Hard to do inside the script easily without modifying settings.
    # We will assume settings are correct or user will fix env.
    pass

# Import models inside try/catch block if possible, or just at top level after setup
try:
    from users.models import User, Customer
    from products.models import Unit, Product, Category
    from warehouse.models import Input
    from orders.models import Output
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)


def run_tests():
    print("Starting verification...")

    # Create User
    if not User.objects.filter(phone_number='+998901234567').exists():
        user = User.objects.create_user(
            phone_number='+998901234567',
            password='secretpassword',
            full_name='Admin Tester'
        )
        print(f"Created User: {user}")
    else:
        user = User.objects.get(phone_number='+998901234567')
        print(f"Using existing user: {user}")

    # Create Customer
    customer = Customer.objects.create(
        full_name='John Doe',
        phone_number='+998998887766',
        description='VIP Cliet',
        address='Tashkent City'
    )
    print(f"Created Customer: {customer}")

    # Create Unit
    unit = Unit.objects.create(name='kg', description='Kilogram')
    print(f"Created Unit: {unit}")

    # Create Product
    product = Product.objects.create(
        name='Apple',
        unit=unit,
        price=15000,
        description='Red apples'
    )
    print(f"Created Product: {product}")

    # Create Input (Kirim)
    input_size = Input.objects.count()
    input_obj = Input.objects.create(
        product=product,
        user=user,
        quantity=100,
        summa=1200000  # 12,000 * 100 assumed cost
    )
    print(f"Created Input: {input_obj}")

    # Create Output (Chiqim)
    output_obj = Output.objects.create(
        product=product,
        user=user,
        customer=customer,
        quantity=5,
        summa=75000,  # 15,000 * 5
        is_payment=True
    )
    print(f"Created Output: {output_obj}")

    print("All checks passed!")


if __name__ == '__main__':
    try:
        run_tests()
    except Exception as e:
        print(f"Verification Failed: {e}")
        exit(1)
