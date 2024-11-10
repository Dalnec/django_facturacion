import uuid
from django.core.management.base import BaseCommand
from apps.invoice.models import Invoice

class Command(BaseCommand):
    help = 'Assign UUID to invoices that do not have it'

    def handle(self, *args, **kwargs):
        invoices_without_uuid = Invoice.objects.filter(uuid__isnull=True)
        for invoice in invoices_without_uuid:
            invoice.uuid = uuid.uuid4()
            invoice.save()
        self.stdout.write(self.style.SUCCESS(f'Assigned UUIDs to {invoices_without_uuid.count()} invoices'))
