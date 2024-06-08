from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from authapp.forms import LoginForm, RegisterForm, EditProfileForm, CustomPasswordChangeForm
from productapp.models import Order


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'authapp/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            print(username)
            password = form.cleaned_data.get('password')
            print(password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect(reverse('home'))  # Перенаправление на главную страницу после успешного входа
            else:
                error_message = "Неверные учетные данные"
                return render(request, 'authapp/login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Недействительная форма"
            return render(request, 'authapp/login.html', {'form': form, 'error_message': error_message})


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'authapp/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, './authapp/register.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')  # Перенаправление на главную страницу после выхода


@method_decorator(login_required, name='dispatch')
class UserView(DetailView):
    model = User
    template_name = 'authapp/user_profile.html'
    context_object_name = 'user'
    user_form_class = EditProfileForm
    password_form_class = CustomPasswordChangeForm

    def get_object(self, queryset=None):
        return User.objects.get(id=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user_form'] = self.user_form_class(instance=user)
        context['password_form'] = self.password_form_class(user=user)
        context['orders'] = Order.objects.filter(user_id=user.id).exclude(status='choosing').order_by('-created_at')[:5]
        return context


class EditProfileView(View):
    template_name = 'authapp/user_profile.html'
    user_form_class = EditProfileForm
    password_form_class = CustomPasswordChangeForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = self.request.user.id
        user_form = self.user_form_class(request.POST, instance=request.user)
        password_form = self.password_form_class(user=request.user, data=request.POST)

        if 'save_user' in request.POST and user_form.is_valid():
            user_form.save()
            return redirect('user', user_id=user_id)

        if 'save_password' in request.POST and password_form.is_valid():
            password_form.save()
            return redirect('home')

        context = self.get_context_data(
            user_form=user_form,
            password_form=password_form)

        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = kwargs
        if 'user_form' not in context:
            context['user_form'] = self.user_form_class(instance=self.request.user)
        if 'password_form' not in context:
            context['password_form'] = self.password_form_class(user=self.request.user)

        return context

#
