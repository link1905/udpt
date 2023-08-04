from django import forms
from taggit.forms import TagField
from taggit.models import Tag


class TagForm(forms.ModelForm):
    name = TagField(required=True)

    def clean_name(self) -> str:
        return self.cleaned_data["name"][0]

    class Meta:
        model = Tag
        fields = ("name",)
