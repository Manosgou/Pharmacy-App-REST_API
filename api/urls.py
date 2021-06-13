from django.urls import path
from api.views import general
from api.views import supplier
from api.views import pharmacist
from api.views import customer


urlpatterns = [
    path('login', general.login),
    path('logout', general.logout),
    path('dashboard', general.dashboard),
    path('user/update/<int:id>', general.user_update),
    path('location/update/<int:id>', general.location_update),
    path('supplier/create/medicine', supplier.create_medicine),
    path('supplier/update/medicine/<int:id>', supplier.update_medicine),
    path('supplier/delete/medicine/<int:id>', supplier.delete_medicine),
    path('supplier/get/medicines', supplier.get_medicines),
    path('supplier/get/categories', supplier.get_medicine_categories),
    path('supplier/create/category', supplier.create_medicine_category),
    path('supplier/update/category/<int:id>', supplier.update_medicine_category),
    path('supplier/delete/category/<int:id>', supplier.delete_medicine_category),
    path('supplier/get/orders',supplier.get_orders),
    path('supplier/update/order-status/<int:id>',supplier.update_order_status),
    path('supplier/delete/order/<int:id>',supplier.delete_order),
    path('pharmacist/make/order',pharmacist.make_order),
    path('pharmacist/get/orders',pharmacist.get_orders),
    path('pharmacist/get/customers/orders',pharmacist.get_customers_orders),
    path('pharmacist/update/customer/order-status/<int:id>',pharmacist.update_customer_order_status),
    path('pharmacist/delete/customer/order/<int:id>',pharmacist.delete_customer_order),
    path('pharmacist/get/medicines',pharmacist.get_medicines),
    path('pharmacist/medicines',pharmacist.pharmacist_medicines),
    path('pharmacist/make/medicine-available/<int:id>',pharmacist.make_medicine_available),
    path('pharmacist/update/medicine/<int:id>/price',pharmacist.update_medicine_price),
    path('customer/get/medicines',customer.get_medicines),
    path('customer/make/order',customer.make_order),
    path('customer/get/orders',customer.get_orders),
]