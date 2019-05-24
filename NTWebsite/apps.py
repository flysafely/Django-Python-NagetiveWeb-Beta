from django.apps import AppConfig

class NTWebsiteConfig(AppConfig):
    name = 'NTWebsite'
    verbose_name='球莫名堂'
 
    def ready(self):
        # signals are imported, so that they are defined and can be used
        #import NTWebsite.signals.request_signal
        import NTWebsite.signals.models_signal