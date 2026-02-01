from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from products.models import Product
from warehouse.models import Input
from orders.models import Output


class Command(BaseCommand):
    help = 'Verify database content and query logic'

    def handle(self, *args, **kwargs):
        self.stdout.write("--- BAZANI TEKSHIRISH START ---")

        # 1. Total Counts
        self.stdout.write(f"Product count: {Product.objects.count()}")
        self.stdout.write(f"Input count: {Input.objects.count()}")
        self.stdout.write(f"Output count: {Output.objects.count()}")

        # 2. Check Timestamps of a sample Input
        last_input = Input.objects.last()
        if last_input:
            self.stdout.write(
                f"Last Input created_at: {last_input.created_at} (Timezone: {last_input.created_at.tzinfo})")

        # 3. Simulate Query Range (Full Year 2026)
        # Using the EXACT logic from views.py
        start_date = timezone.datetime(2026, 1, 1, 0, 0, 0)
        end_date = timezone.datetime(2026, 12, 31, 23, 59, 59)

        # Make aware if naive
        if timezone.is_naive(start_date):
            start_date = timezone.make_aware(start_date)
        if timezone.is_naive(end_date):
            end_date = timezone.make_aware(end_date)

        self.stdout.write(f"Query Range: {start_date} to {end_date}")

        # Run Query
        inputs_in_range = Input.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).count()

        outputs_in_range = Output.objects.filter(
            created_at__gte=start_date,
            created_at__lte=end_date
        ).count()

        self.stdout.write(f"Inputs found in range: {inputs_in_range}")
        self.stdout.write(f"Outputs found in range: {outputs_in_range}")

        if inputs_in_range > 0:
            self.stdout.write(self.style.SUCCESS("FILTER ISHLAYAPTI!"))
        else:
            self.stdout.write(self.style.ERROR("FILTER ISHLAMAYAPTI!"))
