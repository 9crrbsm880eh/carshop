from django.urls import path
from .views import ProductListView, ProductDetailView, CartView, RemoveFromCartView, UpdateCartView, AddItemToCartView, MakeOrderView, OrderListView, DeleteOrderView, SetCompletedStatusView, AddItemView

#
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('category_filter/<int:category_id>', ProductListView.as_view(), name='category_product_filter'),
    path('cart/', CartView.as_view(), name='cart'),
    path('remove-from-cart/<int:item_id>/', RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('update-cart/<int:item_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('add_item_to_cart/', AddItemToCartView.as_view(), name='add_item_to_cart'),
    path('add_item/', AddItemView.as_view(), name='add_item'),
    path('make_order/<int:order_id>', MakeOrderView.as_view(), name='make_order'),
    path('order_list/', OrderListView.as_view(), name='order_list'),
    path('update_order_status/<int:order_id>/', SetCompletedStatusView.as_view(), name='update_order_status'),
    path('delete_order/<int:order_id>/', DeleteOrderView.as_view(), name='delete_order'),
]
