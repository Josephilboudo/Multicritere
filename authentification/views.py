""" from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    # username = request.POST['username']
    # email = request.POST['email']
    # password = request.POST['password']
    # user = User.objects.create_user(username=username, email=email, password=password)
    # user.save()
    #messages.success(request, 'Compte créé avec succès, connecte-toi maintenant !')
    #return redirect('register')
    return render(request, 'register.html')
 """
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Mets le chemin correct vers ton fichier
    
class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirige vers la page de connexion après déconnexion
    
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirection après l'inscription
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

