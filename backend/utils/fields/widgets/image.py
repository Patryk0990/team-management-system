from django import forms


class ImageWidget(forms.ClearableFileInput):
    template_name = 'widgets/clearable_image_input.html'
