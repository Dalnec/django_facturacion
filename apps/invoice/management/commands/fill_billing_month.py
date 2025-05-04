from django.core.management.base import BaseCommand
from apps.invoice.models import Invoice
from dateutil.relativedelta import relativedelta

class Command(BaseCommand):
    help = 'Actualiza el campo billing_month de todas las facturas existentes basándose en read_date.'

    def handle(self, *args, **kwargs):
        updated_count = 0
        invoices = Invoice.objects.all()

        for invoice in invoices:
            if invoice.read_date:
                billing_date = (invoice.read_date - relativedelta(months=1)).replace(day=1).date()
                if invoice.billing_month != billing_date:
                    invoice.billing_month = billing_date
                    invoice.save(update_fields=["billing_month"])
                    updated_count += 1

        self.stdout.write(self.style.SUCCESS(f'Se actualizaron {updated_count} facturas exitosamente.'))
        self.stdout.write(self.style.SUCCESS(f'Facturas sin mes facturado: {Invoice.objects.filter(billing_month__isnull=True).count()}'))