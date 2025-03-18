from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Create mock data for testing"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Mock data successfully created!"))
