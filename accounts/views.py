from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .forms import SignUpForm


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            auth_login(request, user)

            return redirect('home')

    else:
        form = SignUpForm()

    return render(request, 'sign_up.html', {'form': form})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email')
    template_name = 'my_account.html'
    success_url = reverse_lazy('my_account')

    def get_object(self, queryset=None):
        queryset = User.objects.get(pk=self.request.user.pk)

        return queryset
