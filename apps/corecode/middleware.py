from .models import AcademicSession, AcademicTerm


class SiteWideConfigs:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_session,_ = AcademicSession.objects.get_or_create(current=True)
        current_term,_ = AcademicTerm.objects.get_or_create(current=True)

        request.current_session = current_session
        request.current_term = current_term

        response = self.get_response(request)

        return response
