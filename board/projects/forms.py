from django import forms 

from projects.models import Comment 

###### 

class CommentModelForm(forms.ModelForm):
    text = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':'2'}), 
        label="Add A Comment"
    )
    class Meta:
        model = Comment 
        fields = ["text"]

