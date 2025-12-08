from django.utils import timezone
import logging
from django.urls import resolve
from django.db.models import F
from resources.models import Resource
from users.models import Profile
import time

logger = logging.getLogger(__name__)

class IntensiveMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response
        
    def __call__(self,request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time()
        if duration > 2.0:
            logger.warning(f"⚠️ SLOW REQUEST: {request.path} took {duration:.2f} seconds")

        if request.user.is_authenticated:
            Profile.objects.filter(user=request.user).update(last_activity=timezone.now())
            self.track_source_views(request)

    def track_source_views(self,request):
        try:
            current_url = resolve(request.path_info)
            if current_url.url_name == 'resource_detail':
                resource_id = current_url.kwargs.get('pk')
                if resource_id:
                    Resource.objects.filter(pk=resource_id).update(view_count=F('view_count')+1)
        except Exception:
            pass 
            