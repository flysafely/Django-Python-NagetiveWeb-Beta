from django.apps import AppConfig
 
 
class NTWebsiteConfig(AppConfig):
    name = 'NTWebsite'
 
    def ready(self):
        # signals are imported, so that they are defined and can be used
        #import NTWebsite.signals.request_signal
        import NTWebsite.signals.models_signal
