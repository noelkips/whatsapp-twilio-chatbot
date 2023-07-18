from django.urls import path
from whatsapp import views

urlpatterns = [
    path('', views.message, name='message'),
    # path('response/', views.handle_user_response, name='response'),
    # path('categories/', views.display_categories, name='categories'),
    # path('category_selection/', views.category_selection, name='category_selection'),
    # path('category/<int:category_id>/', views.display_products, name='products'),
    # path('handle_product_selection', views.handle_product_selection, name='handle_product_selection'),
    # path('product/<int:product_id>/', views.view_product, name='product'),
    # path('order/<int:product_id>/', views.place_order, name='order'),
]
