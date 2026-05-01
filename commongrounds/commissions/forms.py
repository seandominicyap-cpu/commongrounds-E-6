from django.forms import inlineformset_factory
from django import forms
from .models import Commission, Job

JobFormSet = inlineformset_factory(
    Commission,
    Job,
    fields=["role", "manpower_required", "status"],
    extra=1,
    can_delete=True,
)

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        fields = ['title', 'maker', 'commission_type', 'description', 'people_required', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["maker"].disabled = True
