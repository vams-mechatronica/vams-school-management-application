from django.apps import AppConfig


class StaffsConfig(AppConfig):
    name = "apps.staffs"
    def ready(self):
        import apps.staffs.signals