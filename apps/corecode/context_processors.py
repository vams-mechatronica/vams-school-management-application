from .models import AcademicSession, AcademicTerm, SiteConfig, SchoolDetail


def site_defaults(request):
    current_session = AcademicSession.objects.get(current=True)
    current_term = AcademicTerm.objects.get(current=True)
    site_config = SchoolDetail.objects.first()
    contexts = {
        "current_session": current_session.name,
        "current_term": current_term.name,
        "school_name":site_config.name,
        "school_short_name":site_config.short_name,
        "slogan":site_config.slogan,
        "address":site_config.address,
    }
    return contexts
