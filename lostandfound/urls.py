from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import submit_lost_item, submit_found_item, display_images

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('signup/', views.signup, name='signup'),  # User signup
    path('login/', views.login_view, name='login'),  # User login
    path('homepage/', views.homepage, name='homepage'),  # Homepage for found items
    path('report-found-item/', views.report_found_item, name='report_found_item'),  # Report a found item
    path('found-items/', views.found_items, name='found_items'),  # View found items
    path('confirmation/', views.confirmation, name='confirmation'),  # Confirmation page after actions
    path('search-lost-item/', views.search_lost_item, name='search_lost_item'),  # Search for lost items
    path('match-lost-items/<int:lost_item_id>/', views.match_lost_items, name='match_lost_items'),  # Match lost items with id
    path('verification/<int:lost_item_id>/', views.verification, name='verification'),  # Verification form
    path('logout/', views.logout_view, name='logout'),  # User logout
    path('submit-lost-item/', submit_lost_item, name='submit_lost_item'),
    path('submit-found-item/', submit_found_item, name='submit_found_item'),
    path('lost-items/images/', display_images, name='display_images'),
    path('claim/<int:lost_item_id>/', views.claim, name='claim'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
