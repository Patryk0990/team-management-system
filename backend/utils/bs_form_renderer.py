from django.forms.renderers import TemplatesSetting


class BootstrapFormRenderer(TemplatesSetting):
    form_template_name = "core/bs_form_snippet.html"
