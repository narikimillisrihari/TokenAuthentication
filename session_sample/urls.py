from django.urls import path
from session_sample.views import VisitCounterView,VisitCounterViewAndExprieView



urlpatterns = [
    path('visit/', VisitCounterView.as_view(), name='visit'),
    path('visitandexprie/', VisitCounterViewAndExprieView.as_view(), name='visitandexprie'),
]