from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
import uuid
from django.utils.translation import gettext_lazy as _

# New models from here


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ("admin", "Admin"),
        ("employee", "Employee"),
    ]

    user_type = models.CharField(max_length=9, choices=USER_TYPE_CHOICES)
    # Add other fields specific to each user type
    groups = models.ManyToManyField(
        Group, blank=True, related_name="stocktracker_users"
    )
    user_permissions = models.ManyToManyField(
        Permission, blank=True, related_name="stocktracker_users"
    )

    def is_admin(self):
        return self.user_type == "admin"

    def is_employee(self):
        return self.user_type == "employee"


class Company(models.Model):
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company_name = models.CharField(max_length=255)
    company_desc = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


class Receipt(models.Model):
    receipt_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receipt_date = models.DateTimeField()

    def __str__(self):
        return f"{self.receipt_id} - {self.receipt_date}"


class Product(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_code = models.CharField(max_length=255, unique=True)
    product_name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=20)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.product_name} - {self.product_code} - {self.company}"

class ReceiptProduct(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    product_quantity = models.IntegerField()
    transfer_direction = models.CharField(max_length=10)



class Invoice(models.Model):
    invoice_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    transfer_direction = models.CharField(max_length=10)
    invoice_date = models.DateTimeField()


class InvoiceReceipt(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    invoice_receipt_desc = models.CharField(max_length=255)


class FiscalDocument(models.Model):
    fiscal_document_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    fiscal_document_name = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    transfer_direction = models.CharField(max_length=10)
    fiscal_document_date = models.DateTimeField()


class Personnel(models.Model):
    personnel_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    personnel_name = models.CharField(max_length=255)
    personnel_desc = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.personnel_name}"


class Node(models.Model):
    node_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class NodeType(models.TextChoices):
        START = "S", _("baslangic")
        END = "E", _("bitis")
        ARA = "A", _("ara islem")
        DISARI = "D", _("bu mal disarida")

    node_type = models.CharField(
        max_length=1, choices=NodeType.choices, default=NodeType.ARA
    )

    node_name = models.CharField(max_length=255)
    node_desc = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.node_name} - {self.product} - {self.node_desc}"


class Edge(models.Model):
    edge_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class EdgeType(models.TextChoices):
        NORMAL = "N", _("sirket ici islem")
        DISARIYA = "D", _("mal disariya cikti")
        ICERIYE = "I", _("mal disaridan geldi")

    edge_type = models.CharField(
        max_length=1, choices=EdgeType.choices, default=EdgeType.NORMAL
    )

    prev_node = models.ForeignKey(
        Node, null=True, on_delete=models.DO_NOTHING, related_name="prev_node"
    )
    next_node = models.ForeignKey(
        Node, null=True, on_delete=models.DO_NOTHING, related_name="next_node"
    )
    operation_description = models.TextField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    coefficient = models.FloatField(default=1)

    def __str__(self) -> str:
        return f"{self.prev_node} - {self.next_node} - {self.edge_type}"


class Manufacturing(models.Model):
    manufacturing_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    personnel = models.ForeignKey(
        Personnel, null=True, blank=True, on_delete=models.SET_NULL
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    quantity = models.IntegerField()
    node_id = models.ForeignKey(Node, on_delete=models.DO_NOTHING)
