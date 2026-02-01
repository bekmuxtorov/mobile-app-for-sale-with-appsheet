
import random
from decimal import Decimal
from users.models import User, Customer
from products.models import Product, Unit, Category
from warehouse.models import Input
from orders.models import Output


def create_data():
    print("Starting data generation...")

    # 1. Get or Create User
    # Using the existing superuser created by user
    user = User.objects.filter(is_superuser=True).first()
    if not user:
        print("No superuser found! Creating one...")
        user = User.objects.create_superuser(
            phone_number='+998900000000', password='admin', full_name='Auto Admin')
    else:
        print(f"Using existing user: {user.phone_number}")

    # 2. Create Units
    unit_names = ['kg', 'dona', 'litr', 'metr', 'quti']
    units = []
    for name in unit_names:
        unit, _ = Unit.objects.get_or_create(name=name)
        units.append(unit)
    print(f"Created {len(units)} units.")

    # 3. Create Categories
    category_names = ['Oziq-ovqat', 'Texnika',
                      'Kiyim-kechak', 'Xo\'jalik mollari', 'Kanselyariya']
    categories = []
    for name in category_names:
        cat, _ = Category.objects.get_or_create(name=name)
        categories.append(cat)
    print(f"Created {len(categories)} categories.")

    # 4. Create Customers
    customer_names = ['Ali Valiyev', 'Ivan Ivanov', 'John Doe', 'Vali Aliyev']
    customers = []
    for name in customer_names:
        cust, _ = Customer.objects.get_or_create(
            phone_number=f"+99890{random.randint(1000000, 9999999)}",
            defaults={'full_name': name, 'address': 'Tashkent'}
        )
        customers.append(cust)
    print(f"Created {len(customers)} customers.")

    # 5. Create 20 Products
    products = []
    product_base_names = [
        "Olma", "Non", "Sut", "Shakar", "Un",
        "Televizor", "Telefon", "Noutbuk", "Muzlatgich", "Dazmol",
        "Futbolka", "Shim", "Kurtka", "Paypoq", "Kepka",
        "Sovun", "Shampun", "Tish pastasi", "Kir kukun", "Salfetka"
    ]

    for i, name in enumerate(product_base_names):
        unit = random.choice(units)
        category = random.choice(categories)
        price = Decimal(random.randint(10, 1000)) * 1000  # 10,000 to 1,000,000

        product, _ = Product.objects.get_or_create(
            name=name,
            defaults={
                'unit': unit,
                'category': category,
                'price': price,
                'description': f"Test product {name}"
            }
        )
        products.append(product)
    print(f"Created/Found {len(products)} products.")

    # 6. Create Inputs (Kirim) and Outputs (Chiqim)
    for product in products:
        # Input
        qty_in = Decimal(random.randint(50, 200))
        price_in = product.price * Decimal('0.8')  # Buy at 80% of sell price

        Input.objects.create(
            product=product,
            user=user,
            quantity=qty_in,
            price=price_in
        )

        # Output
        qty_out = Decimal(random.randint(1, 40))
        customer = random.choice(customers)

        Output.objects.create(
            product=product,
            user=user,
            customer=customer,
            quantity=qty_out,
            price=product.price,
            is_payment=True
        )

        # Update stock manually since signals might not be set up or simple update needed
        product.stock_quantity = product.stock_quantity + \
            int(qty_in) - int(qty_out)
        product.save()

    print("Created Inputs and Outputs for all products.")
    print("Data generation complete!")
