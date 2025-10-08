from decimal import Decimal
from datetime import date, datetime
from uuid import UUID
from django.db import models
from model_utils.models import TimeStampedModel

def _jsonable(v):
    from collections.abc import Mapping, Sequence
    if isinstance(v, Decimal):
        return str(v)
    if isinstance(v, (date, datetime)):
        return v.isoformat()
    if isinstance(v, UUID):
        return str(v)
    if isinstance(v, Mapping):
        return {k: _jsonable(val) for k, val in v.items()}
    if isinstance(v, Sequence) and not isinstance(v, (str, bytes, bytearray)):
        return [_jsonable(item) for item in v]
    return v

class InvoiceHistory(TimeStampedModel):
    ACTION_CHOICES = [('create','create'),('update','update'),('delete','delete')]
    
    invoice = models.ForeignKey("invoice.Invoice", related_name='history_changes', on_delete=models.CASCADE)
    employee = models.ForeignKey('user.Employee', related_name='history_changes', on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField()  # diff campo-> {old, new}
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    
    def __str__(self):
        return f"{self.invoice} - {self.action} - {self.changed_at}"
    
    class Meta:
        db_table = 'InvoiceHistory'
        verbose_name = 'Historial deFactura'
        verbose_name_plural = 'Historial de Facturas'
    
    @staticmethod
    def get_diff(old, new) -> dict:
        AUDITED_FIELDS = ['read_date','measured','price','total','subtotal','status','observations','billing_month']
        diff = {}
        for f in AUDITED_FIELDS:
            old_val = getattr(old, f, None) if old else None
            new_val = getattr(new, f, None) if new else None
            if old_val != new_val:
                diff[f] = {
                    'old': _jsonable(old_val),
                    'new': _jsonable(new_val),
                }
        return diff