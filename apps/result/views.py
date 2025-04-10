from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View, FormView
from django.core.paginator import Paginator

from apps.students.models import Student
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass

from .forms import CreateResults, EditResults
from .models import Result
from .utils import has_permission,PermissionRequiredMessageMixin

class CreateResultView(LoginRequiredMixin, PermissionRequiredMessageMixin, View):
    template_name = "result/create_result.html"
    second_template_name = "result/create_result_page2.html"
    form_class = CreateResults
    permission_required = "result.add_result"

    def post(self,request):
        if "finish" in request.POST: 
            form = self.form_class(request.POST)
            if form.is_valid():
                return self.final_submission(request, form)
            return self.handle_invalid_form(request, form)
        selected_ids = request.POST.getlist('students')
        
        if not selected_ids:
            messages.warning(request, "Please select at least one student.")
            return redirect('student-selection')  # Redirect back if no selection
            

        studentlist = ",".join(selected_ids)
        form = self.form_class()
        classes = StudentClass.objects.all()
        return render(request, self.second_template_name, {
            'students': studentlist,
            'count': len(selected_ids),
            'form':form,
            'classes':classes
        })

    def final_submission(self, request, form):
        subjects = form.cleaned_data["subjects"]
        session = form.cleaned_data["session"]
        term = form.cleaned_data["term"]
        students = request.POST["students"]
        
        results = []
        for student in students.split(","):
            stu = Student.objects.get(pk=student)
            if stu.current_class:
                for subject in subjects:
                    check = Result.objects.filter(
                        session=session,
                        term=term,
                        current_class=stu.current_class,
                        subject=subject,
                        student=stu,
                    ).first()
                    if not check:
                        results.append(
                            Result(
                                session=session,
                                term=term,
                                current_class=stu.current_class,
                                subject=subject,
                                student=stu,
                            )
                        )
        
        Result.objects.bulk_create(results)
        messages.success(request, "Results created successfully!")
        return redirect("edit-results")

    def handle_invalid_form(self, request, form):
        # If form is invalid, get the original student selection
        studentlist = request.POST.get("students", "")
        selected_count = len(studentlist.split(",")) if studentlist else 0
        
        return render(request, self.second_template_name, {
            'students': studentlist,
            'form': form,
            'count': selected_count
        })
    
    def get(self, request):
        students = Student.objects.all()
        classes = StudentClass.objects.all()
        return render(request, self.template_name, {'students': students,'classes':classes})
from django.forms import modelformset_factory

class EditResultsView(LoginRequiredMixin, PermissionRequiredMessageMixin, FormView):
    template_name = "result/edit_results.html"
    permission_required = "result.update_result"
    
    def get_form_class(self):
        return modelformset_factory(
            Result,
            fields=('test_score', 'exam_score'),
            extra=0,
            can_delete=True
        )

    def get_queryset(self):
        return Result.objects.filter(
            session=self.request.current_session,
            term=self.request.current_term
        ).select_related('student', 'subject', 'current_class')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['queryset'] = self.get_queryset()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['results'] = self.get_queryset()
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Results successfully updated")
        return redirect("edit-results")

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below")
        return self.render_to_response(
            self.get_context_data(form=form)
        )

from .models import Result, AcademicTerm

class ResultListView(LoginRequiredMixin, PermissionRequiredMessageMixin, View):
    permission_required = 'result.view_result'
    model = Result
    paginate_by = 10  # Set default pagination limit

    def get_queryset(self):
        user = self.request.user
        
        if user.is_superuser or user.is_staff:
            return self.model.objects.all()

        if user.groups.filter(name='Students').exists():
            student = Student.objects.get(user=user)
            return self.model.objects.filter(student=student)
        
        return self.model.objects.none()
    
    def getGrade(self,obt_score,mm_score):
        perc = (float(obt_score)/float(mm_score)) * 100

        if perc == 100:
            grade = 'A+'
        elif perc <100 and perc >= 90:
            grade = 'A'
        elif perc < 90 and perc >= 80:
            grade = 'B+'
        elif perc < 80 and perc >= 70:
            grade = 'B'
        
        elif perc < 70 and perc >= 60:
            grade = 'C+'
        
        elif perc < 60 and perc >= 50:
            grade = 'C'
        
        elif perc < 50 and perc >= 40:
            grade = 'D+'
        elif perc < 40 and perc >= 33:
            grade = 'D'
        else:
            grade = 'F'
        return grade


    def get(self, request, *args, **kwargs):
        session = request.GET.get("session")
        selected_term = request.GET.get("term")
        selected_class = request.GET.get("class")
        selected_student = request.GET.get("student")

        queryset = self.get_queryset()
        
        if session:
            queryset = queryset.filter(session_id=session)
        if selected_term:
            queryset = queryset.filter(term_id=selected_term)
        if selected_class:
            queryset = queryset.filter(current_class_id=selected_class)
        if selected_student:
            queryset = queryset.filter(student_id=selected_student)
        
        paginator = Paginator(queryset, self.paginate_by)
        page = request.GET.get('page')
        paginated_results = paginator.get_page(page)
        
        bulk = {}
        for result in paginated_results:
            student_id = result.student.id
            if student_id not in bulk:
                bulk[student_id] = {"student": result.student, "terms": {}}
            
            if result.term.id not in bulk[student_id]["terms"]:
                bulk[student_id]["terms"][result.term.id] = {
                    "term": result.term,
                    "subjects": [],
                    "test_total": 0,
                    "exam_total": 0,
                    "total_total": 0,
                    "total_mm":0,
                    "total_grade":None
                }

            term_data = bulk[student_id]["terms"][result.term.id]
            term_data["subjects"].append(result)
            term_data["test_total"] += result.test_score
            term_data["exam_total"] += result.exam_score
            term_data["total_total"] += result.test_score + result.exam_score
            term_data['total_mm'] += result.subject.test_max_marks + result.subject.exam_max_marks
            term_data['total_grade'] = "{grade}/ {remarks}".format(grade=self.getGrade(obt_score=term_data['total_total'],\
                                                     mm_score=term_data['total_mm']),remarks="Pass" if self.getGrade(obt_score=term_data['total_total'],\
                                                     mm_score=term_data['total_mm']) != 'F' else 'Fail')
        
        
        context = {
            "results": bulk,
            "terms": AcademicTerm.objects.all(),
            "sessions": AcademicSession.objects.all(),
            "classes": StudentClass.objects.all(),
            "students": Student.objects.all(),
            "selected_term": selected_term,
            "selected_session": session,
            "selected_class": selected_class,
            "selected_student": selected_student,
            "paginated_results": paginated_results,
        }
        return render(request, "result/all_results.html", context)
