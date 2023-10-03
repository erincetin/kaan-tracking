# stock_racker/urls.py

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "stocktracker"
urlpatterns = [
    path("create-new-product/", views.create_new_product, name="create_new_product"),
    path("", views.main_page, name="main_page"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="stocktracker/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("success/", views.success_view, name="success"),
    path("all-forms/", views.all_forms, name="all_forms"),
    path("all-models/", views.all_models, name="all_models"),
    path("add-personnel/", views.add_personnel, name="add-personnel"),
    path("add-company/", views.add_company, name="add-company"),
    path('fetch-products/', views.fetch_products, name='fetch_products'),
    path('fetch_graph_data/', views.fetch_graph_data, name='fetch_graph_data'),
    path('edit_product/<uuid:product_id>/', views.edit_product, name='edit_product'),
    path('select_product/', views.select_product, name='select_product'),
]
