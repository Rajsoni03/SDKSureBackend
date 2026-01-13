from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Monitor board connectivity and status updates."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Monitoring boards (stub)."))

