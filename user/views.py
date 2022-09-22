from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import RedirectView
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import BaseSignupForm, BaseProfileForm


class UserLoginView(LoginView):
    template_name = 'user/login.html'


class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "You are successfully logged out.")

        return super().dispatch(request, *args, **kwargs)


class UserRegistrationView(CreateView):
    model = User
    form_class = BaseSignupForm
    template_name = 'user/signup.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        messages.success(self.request, "Your account was successfully created.")

        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = BaseProfileForm
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def form_valid(self, form):
        messages.success(self.request, "Your profile was successfully updated.")

        return super().form_valid(form)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'user/change_password.html'

    def form_valid(self, form):
        messages.success(self.request, "Password was successfully changed.")

        return super().form_valid(form)

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('profile')


class UserUpgradeView(LoginRequiredMixin, RedirectView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        authors_group = Group.objects.get(name='authors')
        if not request.user.groups.filter(name='authors').exists():
            authors_group.user_set.add(user)

        messages.success(request, "Congratulations, you are now an author.")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse_lazy('profile')


class UserDowngradeView(LoginRequiredMixin, RedirectView):
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        authors_group = Group.objects.get(name='authors')
        if request.user.groups.filter(name='authors').exists():
            authors_group.user_set.remove(user)

        messages.success(request, "Congratulations, you are no longer an author")

        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        return reverse_lazy('profile')
