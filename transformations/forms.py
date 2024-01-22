from django import forms

class TextProcessingForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Your Text")
    choice = forms.ChoiceField(choices=[('edit_one', 'Edit One'), ('edit_two', 'Edit Two'), ('highlight', 'Highlight')], label="Processing Type")
    
