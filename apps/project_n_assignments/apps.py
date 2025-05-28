from django.apps import AppConfig


class ProjectNAssignmentsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.project_n_assignments"
    
    def ready(self):
        import apps.project_n_assignments.signals