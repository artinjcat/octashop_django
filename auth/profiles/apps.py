from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'auth.profiles'
    

    def ready(self):
        import auth.profiles.signals
