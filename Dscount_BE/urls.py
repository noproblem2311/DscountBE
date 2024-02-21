from django.contrib import admin
from django.urls import path, include  # include is needed for including router URLs
from rest_framework.routers import DefaultRouter
from src.srcviews.record_views import VideoTranscriptionViewSet, handle_video

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'videos', VideoTranscriptionViewSet, basename='video')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('handle_video/', handle_video),
    # Use the router URLs, which now includes all the URLs for the VideoTranscriptionViewSet
    path('', include(router.urls)),
    # Include the src URLs
    path('', include('src.urls')),
]