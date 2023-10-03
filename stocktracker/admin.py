from django.contrib import admin
from .models import (
    User,
    Company,
    Receipt,
    Product,
    ReceiptProduct,
    Invoice,
    InvoiceReceipt,
    FiscalDocument,
    Personnel,
    Node,
    Edge,
    Manufacturing,
)

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Receipt)
admin.site.register(Product)
admin.site.register(ReceiptProduct)
admin.site.register(Invoice)
admin.site.register(InvoiceReceipt)
admin.site.register(FiscalDocument)
admin.site.register(Personnel)
admin.site.register(Node)
admin.site.register(Edge)
admin.site.register(Manufacturing)
