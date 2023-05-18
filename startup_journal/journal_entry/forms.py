from django import forms
from taggit.models import Tag
from .models import Entry

class EntryForm(forms.ModelForm):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        limit_choices_to={'pk__in': [1, 2, 3]}
    )

    class Meta:
        model = Entry
        fields = ['tags', 'text']
        labels = {'tags': 'Tags:', 'text': 'Entry:'}
        widgets = {
            'text': forms.Textarea(attrs={'cols':80, 'rows':15}),
        }

class SearchForm(forms.Form):
    query = forms.CharField()
