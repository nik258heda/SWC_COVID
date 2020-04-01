from django import forms
from admin_panel.models import Request, Comment

class AddRequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['requirement', 'category','address_allowed', 'address', 'city', 'state', 'user_remarks']

    def __init__(self, *args, **kwargs):

        super(AddRequestForm, self).__init__(*args, **kwargs)
        self.fields['requirement'].label = "<b>Requirement</b>"
        self.fields['category'].label = "<b>Category</b>"
        self.fields['address_allowed'].label = "<b>Display Request to Others? (or just admins)</b>"
        self.fields['address'].label = "<b>Address</b>"
        self.fields['city'].label = "<b>City</b>"
        self.fields['state'].label = "<b>State</b>"
        self.fields['user_remarks'].label = "<b>Remarks (Optional)</b>"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {'content',}

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].label = "<b>Add Comment</b>"
