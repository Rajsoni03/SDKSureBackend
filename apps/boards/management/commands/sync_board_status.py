from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sync board status (stub)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Synced board status (stub)."))

