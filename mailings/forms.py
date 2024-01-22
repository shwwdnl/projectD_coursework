from django import forms

from mailings.models import Audience, Client


class AudienceForm(forms.ModelForm):
    class Meta:
        model = Audience
        fields = ("name", "recipients")

    def __init__(self, user, *args, **kwargs):
        super(AudienceForm, self).__init__(*args, **kwargs)
        self.fields["recipients"].queryset = Client.objects.filter(creator=user)
