from django import forms
from admin_panel.models import Request

class AddRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['requirement', 'category', 'urgency_rating', 'address_allowed', 'address', 'city', 'state']

    def __init__(self, *args, **kwargs):

        super(AddRequestForm, self).__init__(*args, **kwargs)
        self.fields['requirement'].label = "<b>Requirement</b>"
        self.fields['category'].label = "<b>Category</b>"
        self.fields['urgency_rating'].label = "<b>Urgency (1-10)</b>"
        self.fields['address_allowed'].label = "<b>Display Address to Others?</b>"
        self.fields['address'].label = "<b>Address (optional)</b>"
        self.fields['city'].label = "<b>City (optional)</b>"
        self.fields['state'].label = "<b>State (optional)</b>"
