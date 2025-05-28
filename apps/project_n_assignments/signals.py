from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .models import ClassAssignmentNProject, StudentAssignmentStatus, Student

@receiver(post_save, sender=ClassAssignmentNProject)
def create_for_all_students(sender, instance, created, **kwargs):
    if created and instance.is_assignment_for_all:
        students = Student.objects.filter(current_class=instance.for_class)
        for student in students:
            StudentAssignmentStatus.objects.get_or_create(
                assignment=instance,
                student=student
            )

@receiver(m2m_changed, sender=ClassAssignmentNProject.students.through)
def create_for_selected_students(sender, instance, action, pk_set, **kwargs):
    if action == "post_add" and not instance.is_assignment_for_all:
        # Only create for selected students after they've been added
        for student_id in pk_set:
            student = Student.objects.get(pk=student_id)
            StudentAssignmentStatus.objects.get_or_create(
                assignment=instance,
                student=student
            )