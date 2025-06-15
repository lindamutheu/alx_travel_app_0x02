from django.core.management.base import BaseCommand
from listings.models import Property
from django.contrib.auth import get_user_model
import random

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed the database with sample listings data.'

    def handle(self, *args, **kwargs):
        if not User.objects.exists():
            self.stdout.write(self.style.ERROR('❌ No users found. Please create a user first.'))
            return

        host = User.objects.first()  # Use the first available user as host

        sample_locations = ['Nairobi', 'Mombasa', 'Kisumu', 'Naivasha', 'Malindi']
        sample_names = ['Ocean View Villa', 'Cozy Cabin', 'Modern Apartment', 'Safari Lodge', 'City Condo']

        for i in range(10):
            name = random.choice(sample_names) + f" #{random.randint(1, 100)}"
            location = random.choice(sample_locations)
            price = round(random.uniform(50, 300), 2)

            Property.objects.create(
                host=host,
                name=name,
                description=f"{name} located in {location}. A perfect stay!",
                location=location,
                price_per_night=price
            )

        self.stdout.write(self.style.SUCCESS('✅ Seeded 10 sample listings successfully.'))
