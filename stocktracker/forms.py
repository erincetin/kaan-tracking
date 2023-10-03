# stocktracker/forms.py

from django import forms
from .models import Product
from django.contrib.auth.forms import UserCreationForm
from .models import User, Personnel, Company, Node, Edge


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["product_code", "product_name", "product_type", "company"]


class SignupForm(UserCreationForm):
    # Add any additional fields you want to collect during registration
    # For example, email, full name, etc.

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class PersonnelForm(forms.ModelForm):
    class Meta:
        model = Personnel
        fields = ["personnel_name", "personnel_desc"]


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["company_name", "company_desc"]  # Add other fields as needed


class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ["node_type", "node_name", "node_desc", "product"]


class EdgeForm(forms.ModelForm):
    class Meta:
        model = Edge
        fields = [
            "edge_type",
            "prev_node",
            "next_node",
            "operation_description",
            "product",
            "coefficient",
        ]
