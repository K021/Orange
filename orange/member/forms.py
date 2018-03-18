from django import forms

from member.models import TeamBase, Member


class TeamBaseForm(forms.Form):

    class Meta:
        model = TeamBase
        fields = (
            'name',
        )
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


class MemberFrom(forms.Form):

    class Meta:
        model = Member
        fields = {
            'name',
            'leader',
            'clouder',
            'sex',
            'activity',
            'age',
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'leader': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'clouder': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'sex': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'activity': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'age': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }


class Closeness(forms.Form):
    closeness = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    )