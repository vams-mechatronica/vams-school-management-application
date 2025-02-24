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

class CreateResultView(LoginRequiredMixin, PermissionRequiredMessageMixin, FormView):
    template_name = "result/create_result.html"
    form_class = CreateResults
    permission_required = "result.result.add_result"

    def form_valid(self, form):
        request = self.request
        if "finish" in request.POST:
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
            return redirect("edit-results")
        
        id_list = request.POST.getlist("students")
        if id_list:
            studentlist = ",".join(id_list)
            return render(
                request,
                "result/create_result_page2.html",
                {"students": studentlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didn't select any student.")
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students"] = Student.objects.all()
        return context

class EditResultsView(LoginRequiredMixin, PermissionRequiredMessageMixin, ListView):
    model = Result
    template_name = "result/edit_results.html"
    context_object_name = "results"
    # paginate_by = 10  # Adjust this number as needed
    permission_required = "result.result.update_result"
    
    def get_queryset(self):
        return Result.objects.filter(
            session=self.request.current_session, term=self.request.current_term
        )

    def post(self, request, *args, **kwargs):
        results = self.get_queryset()
        formset = EditResults(request.POST, queryset=results)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
        return self.get(request, *args, **kwargs, formset=formset)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "formset" not in context:
            context["formset"] = EditResults(queryset=self.get_queryset())
        return context


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
                }

            term_data = bulk[student_id]["terms"][result.term.id]
            term_data["subjects"].append(result)
            term_data["test_total"] += result.test_score
            term_data["exam_total"] += result.exam_score
            term_data["total_total"] += result.test_score + result.exam_score
        
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
