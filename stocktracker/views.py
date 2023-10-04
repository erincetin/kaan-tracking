from django.shortcuts import render, redirect, get_object_or_404
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

import networkx as nx
import matplotlib.pyplot as plt
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import SignupForm, PersonnelForm, CompanyForm, NodeForm, EdgeForm
from django.urls import reverse
from django.db import transaction
from django.forms import formset_factory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def main_page(request):
    return render(request, "stocktracker/main_page.html")

def select_product(request):
    products = Product.objects.all()
    return render(request, 'stocktracker/select_product.html', {'products': products})

def production_steps_graph(request, product_id):
    product = Product.objects.get(pk=product_id)
    intermediates = product.intermediates.all()
    final_intermediates = intermediates.filter(is_final_step=True)

    G = nx.DiGraph()

    for intermediate in intermediates:
        outgoing_steps = intermediate.outgoing_steps.all()
        for step in outgoing_steps:
            G.add_edge(intermediate.name, step.to_intermediate.name)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight="bold")
    plt.show()

    return render(
        request, "stocktracker/production_steps_graph.html", {"product": product}
    )

@csrf_exempt
def create_new_product(request):

    ajax_urls = {
        'fetch_products': reverse('stocktracker:fetch_products'),
        'create_new_product': reverse('stocktracker:create_new_product'),
    }

    print(ajax_urls["fetch_products"])

    if request.method == "POST":
        if 'product_code' in request.POST:  # Assuming 'product_code' is one of the fields in ProductForm
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                new_product = product_form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Product added successfully!',
                    'product_name': new_product.product_name,
                    'product_code': new_product.product_code
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to save product. Please try again.'})
            
        if 'node_name' in request.POST:  # Assuming 'node_name' is one of the fields in NodeForm
            node_form = NodeForm(request.POST)
            if node_form.is_valid():
                new_node = node_form.save()
                return JsonResponse({
                    'status': 'success',
                    'message': 'Node added successfully!',
                    'node_id': str(new_node.node_id),  # Sending the newly created node's ID
                    'node_name': new_node.node_name
    })

        elif 'edge_type' in request.POST:
            edge_form = EdgeForm(request.POST)
            if edge_form.is_valid():
                edge_form.save()
                return JsonResponse({'status': 'success', 'message': 'Edge added successfully!'})

    product_form = ProductForm()
    node_form = NodeForm()
    edge_form = EdgeForm()

    context = {
        'product_form': product_form,
        'node_form': node_form,
        'edge_form': edge_form,
        'ajax_urls': ajax_urls,
    }

    return render(request, 'stocktracker/create_new_product.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    nodes = Node.objects.filter(product=product)
    edges = Edge.objects.filter(product=product)

    if request.method == "POST":
        # Handle the form submission here if needed
        pass

    context = {
        'product': product,
        'nodes': nodes,
        'edges': edges,
        'node_form': NodeForm(),
        'edge_form': EdgeForm(),
    }

    return render(request, 'stocktracker/edit_product.html', context)

def fetch_products(request):
    products = Product.objects.all()
    product_list = [{'id': str(p.product_id), 'name': p.product_name, 'code': p.product_code} for p in products]
    return JsonResponse({'status': 'success', 'products': product_list})

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(
                "stocktracker:main_page"
            )  # Redirect to the main page after successful signup
    else:
        form = SignupForm()
    return render(request, "stocktracker/signup.html", {"form": form})


def fetch_graph_data(request):
    product_id = request.GET.get('product_id')
    
    if not product_id:
        return JsonResponse({'status': 'error', 'message': 'Product ID is required'})

    try:
        nodes = Node.objects.filter(product__product_id=product_id).values()
        edges = Edge.objects.filter(product__product_id=product_id).values()
        
        data = {
            'nodes': list(nodes),
            'edges': list(edges)
        }
        
        return JsonResponse({'status': 'success', 'data': data})
    
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product does not exist'})

    except Exception as e:
        # This is a broad exception for unexpected errors.
        # You might want to log this error in production.
        return JsonResponse({'status': 'error', 'message': 'An unexpected error occurred.'})


def all_forms(request):
    pass


def all_models(request):
    users = User.objects.all()
    companys = Company.objects.all()
    receipts = Receipt.objects.all()
    products = Product.objects.all()
    receiptProducts = ReceiptProduct.objects.all()
    invoices = Invoice.objects.all()
    invoiceReceipts = InvoiceReceipt.objects.all()
    fiscalDocuments = FiscalDocument.objects.all()
    personnels = Personnel.objects.all()
    nodes = Node.objects.all()
    edges = Edge.objects.all()
    manufacturings = Manufacturing.objects.all()

    return render(
        request,
        "stocktracker/all_models.html",
        {
            "users": users,
            "products": products,
            "companys": companys,
            "receipts": receipts,
            "receiptProducts": receiptProducts,
            "invoices": invoices,
            "invoiceReceipts": invoiceReceipts,
            "fiscalDocuments": fiscalDocuments,
            "personnels": personnels,
            "nodes": nodes,
            "edges": edges,
            "manufacturings": manufacturings,
        },
    )


def add_personnel(request):
    if request.method == "POST":
        form = PersonnelForm(request.POST)
        if form.is_valid():
            form.save()
            # Create a new instance of the form after successfully saving
            form = PersonnelForm()  # This will create a blank form

            return redirect(reverse("stocktracker:success"))
    else:
        form = PersonnelForm()

    return render(request, "stocktracker/add_personnel.html", {"form": form})


def add_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to a success page or another view
            form = CompanyForm()
            return redirect(reverse("stocktracker:success"))
    else:
        form = CompanyForm()

    return render(request, "stocktracker/add_company.html", {"form": form})


def success_view(request):
    messages.success(request, "Your success message here.")
    return render(request, "stocktracker/success.html")
