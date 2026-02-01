from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from products.models import Product, Unit, Category
from warehouse.models import Input
from orders.models import Output
from users.models import Customer, User


class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write("Ma'lumotlar yaratilmoqda...")

        # 1. Ensure User/Admin exists
        admin_user = User.objects.first()
        if not admin_user:
            self.stdout.write(
                "Admin user topilmadi. Yangi superuser yaratilmoqda...")
            try:
                admin_user = User.objects.create_superuser(
                    phone_number='+998900000000',
                    full_name='Admin',
                    password='1'
                )
                self.stdout.write("Superuser yaratildi: +998900000000 / 1")
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Xatolik user yaratishda: {e}"))
                return

        # 2. Ensure Unit exists
        unit, _ = Unit.objects.get_or_create(name="dona")

        # 3. Ensure Category exists
        category, _ = Category.objects.get_or_create(name="Umumiy")

        # 4. Ensure Customer exists
        customer, _ = Customer.objects.get_or_create(
            phone_number="+998901234567",
            defaults={'full_name': "Test Mijoz", 'address': "Toshkent"}
        )

        # 5. Create 20 Products
        for i in range(1, 21):
            product_name = f"Test Tovar {i}"
            product, created = Product.objects.get_or_create(
                name=product_name,
                defaults={
                    'category': category,
                    'unit': unit,
                    'price': random.randint(60000, 100000),
                    'description': f"Avtomatik yaratilgan test tovar {i}"
                }
            )

            # 6. Create Input (Kirim)
            for days_ago in [1, 0]:
                qty = random.randint(10, 100)
                price = random.randint(1000, 50000)

                inp = Input.objects.create(
                    product=product,
                    user=admin_user,
                    quantity=qty,
                    price=price
                )
                inp.created_at = timezone.now() - timedelta(days=days_ago)
                inp.save()

            # 7. Create Output (Chiqim)
            for days_ago in [1, 0]:
                qty = random.randint(1, 10)
                price = product.price or random.randint(60000, 100000)

                out = Output.objects.create(
                    product=product,
                    customer=customer,
                    user=admin_user,
                    quantity=qty,
                    price=price
                )
                out.created_at = timezone.now() - timedelta(days=days_ago)
                out.save()

            self.stdout.write(f"{product.name} yaratildi.")

        self.stdout.write(self.style.SUCCESS(
            "MUVADFAQIYATLI YAKUNLANDI! 20 ta tovar qo'shildi."))
