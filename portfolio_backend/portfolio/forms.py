from django import forms
from .models import ContactSubmission, Comment
import re


class ContactForm(forms.ModelForm):
    """Form for contact submissions."""
    
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'fname',
                'placeholder': 'Full Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'umail',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'phone',
                'placeholder': 'Phone'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control border-none',
                'id': 'subject',
                'placeholder': 'Subject'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'exampleFormControlTextarea1',
                'rows': 7,
                'placeholder': 'Message'
            }),
        }


class CommentForm(forms.ModelForm):
    """Form for blog comments with security measures."""
    
    # Honeypot field for spam protection - should remain empty
    website = forms.CharField(required=False, widget=forms.HiddenInput())
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    
    class Meta:
        model = Comment
        fields = ['author_name', 'author_email', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name *',
                'maxlength': '100',
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email *',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here... *',
                'rows': 4,
                'maxlength': '1000',
            }),
        }
    
    def clean_website(self):
        """Honeypot validation - if filled, it's likely a bot."""
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError("Spam detected.")
        return website
    
    def clean_content(self):
        """Sanitize content to prevent XSS."""
        content = self.cleaned_data.get('content', '')
        # Remove any HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Limit length
        if len(content) > 1000:
            raise forms.ValidationError("Comment is too long (max 1000 characters).")
        if len(content) < 3:
            raise forms.ValidationError("Comment is too short.")
        return content
    
    def clean_author_name(self):
        """Validate author name."""
        name = self.cleaned_data.get('author_name', '')
        # Remove any HTML tags
        name = re.sub(r'<[^>]+>', '', name)
        if len(name) < 2:
            raise forms.ValidationError("Name is too short.")
        return name
