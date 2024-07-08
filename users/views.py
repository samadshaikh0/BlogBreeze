from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model

class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset.html'

    def form_valid(self, form):
        
        user_model = get_user_model()
        email = form.cleaned_data['email']
        user = user_model.objects.filter(email=email).first()  # Filter for unique email

        if user:
            return super().form_valid(form)
        else:
            form.add_error('email', 'This email address is not associated with an account.')
            return self.render_to_response(self.get_context_data(form=form))


def register(req):
    if req.method == 'POST':
        form = UserRegisterForm(req.POST)
        if form.is_valid():
            form.save()  
            username = form.cleaned_data.get('username')
            messages.success(req, f'Your account now has been created! You can login now ${username}' )
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(req, 'users/register.html', {'form': form})


@login_required
def profile(req):
    if req.method == 'POST':
        u_form = UserUpdateForm(req.POST, instance=req.user)
        p_form = ProfileUpdateForm(req.POST,req.FILES,instance=req.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(req, f'Your account now has been Updated!')
            return redirect('profile') 

    else:
        u_form = UserUpdateForm(instance=req.user)
        p_form = ProfileUpdateForm(instance=req.user.profile)
        context = {
            'u_form' : u_form,
            'p_form' : p_form
        }

    return render(req, 'users/profile.html', context=context)