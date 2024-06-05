from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView

from .forms import ProductForm
from .models import Product, Order, OrderItem, Category


class ProductListView(ListView):
    model = Product
    template_name = 'productapp/product_list.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = True
        context['popular_product'] = Product.objects.first()
        context['product_categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.kwargs.get('category_id')

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class AddItemView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        form = ProductForm()
        return render(request, 'productapp/add_item.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')
        return render(request, 'productapp/add_item.html', {'form': form})

    def test_func(self):
        return self.request.user.is_staff


class ProductDetailView(DetailView):
    model = Product
    template_name = 'productapp/product_detail.html'
    context_object_name = 'product'
    print()

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Product.objects.get(pk=pk)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sidebar'] = True
        context['popular_product'] = Product.objects.first()
        return context


class CartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            cart, created = Order.objects.get_or_create(user=request.user, status='choosing')
            cart_items = OrderItem.objects.filter(cart=cart)
            total_price = cart.total_price
            popular_product = Product.objects.first()
        except Order.DoesNotExist:
            cart_items = []
            total_price = 0
        except Exception as e:
            print(e)
            cart_items = []
            total_price = 0
        return render(
            request,
            'productapp/cart.html',
            {
                'cart_items': cart_items,
                'total_price': total_price,
                'order': cart,
                'popular_product': popular_product,
                'sidebar': True}
        )


class RemoveFromCartView(View):
    def post(self, request, item_id, *args, **kwargs):
        try:
            cart_item = OrderItem.objects.get(id=item_id)
            cart_item.delete()
        except (Order.DoesNotExist, OrderItem.DoesNotExist):
            pass
        return redirect('cart')


class AddItemToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        print(product_id)
        try:
            cart, created = Order.objects.get_or_create(user=request.user, status='choosing')
            product = Product.objects.get(id=product_id)
            cart_item, created = OrderItem.objects.get_or_create(cart=cart, product_id=product.id)
            cart_item.save()
        except Exception as e:
            print(e)
            pass
        return redirect(request.META.get('HTTP_REFERER', 'cart'))


class UpdateCartView(View):
    def post(self, request, item_id, *args, **kwargs):
        quantity = int(request.POST.get('quantity', 1))
        print(item_id, quantity)

        try:
            cart_item = OrderItem.objects.get(id=item_id)
            cart_item.quantity = quantity
            cart_item.save()
        except (Order.DoesNotExist, OrderItem.DoesNotExist):
            pass
        return redirect('cart')


class MakeOrderView(View):
    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'pending'
            order.save()
        except (Order.DoesNotExist, OrderItem.DoesNotExist):
            pass
        return redirect('cart')


class OrderListView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(status="pending")
        old_orders = Order.objects.filter(status__in=("cancelled", "completed"))
        return render(
            request,
            'productapp/order_list.html',
            {'orders': orders, 'sidebar': True, 'old_orders': old_orders})

    def test_func(self):
        return self.request.user.is_staff


class SetCompletedStatusView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'completed'
            order.save()
            messages.success(request, 'Статус заказа обновлен.')
        except Order.DoesNotExist:
            messages.error(request, 'Заказ не найден.')
        except Exception as e:
            messages.error(request, 'Некорректный статус заказа.')
            print(e)
        return redirect('order_list')

    def test_func(self):
        return self.request.user.is_staff


class DeleteOrderView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
            order.delete()
            messages.success(request, 'Заказ удален.')
        except Order.DoesNotExist:
            messages.error(request, 'Заказ не найден.')
        return redirect('order_list')

    def test_func(self):
        return self.request.user.is_staff
