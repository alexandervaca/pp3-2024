from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class  ModificarUser(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']