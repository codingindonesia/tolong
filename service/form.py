from django import forms
from service.models import Invitation

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = '__all__'