from .models import AcademicSession, AcademicTerm, SiteConfig, SchoolDetail


def site_defaults(request):
    current_session = AcademicSession.objects.get(current=True)
    current_term = AcademicTerm.objects.get(current=True)
    site_config = SchoolDetail.objects.first()
    
    contexts = {
        "current_session": current_session.name,
        "current_term": current_term.name,
        "school_name":site_config.name if site_config else "My School",
        "school_short_name":site_config.short_name if site_config else "My School",
        "slogan":site_config.slogan if site_config else "My School",
        "address":site_config.address if site_config else "My School",
        "letterheader_image":site_config.letterhead.url if site_config and site_config.letterhead else "#",
    }
    return contexts
