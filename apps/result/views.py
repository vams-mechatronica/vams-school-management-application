from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, View

from apps.students.models import Student

from .forms import CreateResults, EditResults
from .models import Result
from .utils import has_permission

@has_permission('result.result.can_add_result')
@login_required
def create_result(request):
    students = Student.objects.all()
    if request.method == "POST":

        # after visiting the second page
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
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

        # after choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResults(
                initial={
                    "session": request.current_session,
                    "term": request.current_term,
                }
            )
            studentlist = ",".join(id_list)
            return render(
                request,
                "result/create_result_page2.html",
                {"students": studentlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didnt select any student.")
    return render(request, "result/create_result.html", {"students": students})

@has_permission('result.result.can_update_result')
@login_required
def edit_results(request):
    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
    else:
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        form = EditResults(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})


from .models import Result, AcademicTerm

class ResultListView(LoginRequiredMixin, View):

    # @method_decorator(has_permission('result.result.can_view_result'),name='dispatch')
    def get(self, request, *args, **kwargs):
        session = request.current_session
        selected_term = request.GET.get("term")

        # Filter results based on the selected term, or get results for all terms if no term is selected
        if selected_term:
            results = Result.objects.filter(session=session, term=selected_term)
        else:
            results = Result.objects.filter(session=session)

        # Organize results by student and term
        bulk = {}
        for result in results:
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
            "selected_term": selected_term,
        }
        return render(request, "result/all_results.html", context)