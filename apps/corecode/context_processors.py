from .models import AcademicSession, AcademicTerm, SiteConfig, SchoolDetail
from apps.notifications.models import *


def site_defaults(request):
    current_session = AcademicSession.objects.get(current=True)
    current_term = AcademicTerm.objects.get(current=True)
    site_config = SchoolDetail.objects.first()
    delivered_notifications = DeliveredNotification.objects.filter(
        user=request.user.id,
        mark_as_read=False
    ).order_by('-delivered_at')

    notifications = []

    for dn in delivered_notifications:
        related_obj = None
        if dn.content_type == 'Notification':
            related_obj = Notification.objects.filter(id=dn.object_id).first()
        elif dn.content_type == 'Announcement':
            related_obj = Announcement.objects.filter(id=dn.object_id).first()
        elif dn.content_type == 'ShoutOut':
            related_obj = ShoutOut.objects.filter(id=dn.object_id).first()

        if related_obj:
            notifications.append({
                'title': related_obj.title,
                'message': related_obj.message,
                'created_at': dn.delivered_at
            })


    unread_count = delivered_notifications.filter(mark_as_read=False).count()

    
    contexts = {
        "current_session": current_session.name,
        "current_term": current_term.name,
        "school_name":site_config.name if site_config else "My School",
        "school_short_name":site_config.short_name if site_config else "My School",
        "slogan":site_config.slogan if site_config else "My School",
        "address":site_config.address if site_config else "My School",
        'notifications': notifications,
        'notifications_unread_count': unread_count,
        "letterheader_image":site_config.letterhead.url if site_config and site_config.letterhead else "#",
    }
    return contexts
