from django.urls import path
from . import views


urlpatterns = [
    # API endpoint listing vegetarian/vegan users
    path('vegetarian_vegan/', views.VegetarianVeganListView.as_view(), name='vegetarian_vegan'),
]