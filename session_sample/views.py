# from urllib import request
from django.shortcuts import render
from rest_framework.views  import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Create your views here.
class VisitCounterView(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request):
        # last_visit_time = request.session.get('last_visit_time')
        # print(last_visit_time)
        visit_count=request.session.get('visit_count',0)

        visit_count +=1

        request.session['visit_count']=visit_count

        return Response(
            {'message':f'you visited this page {visit_count} times.'},
            status=status.HTTP_200_OK
        )
    
from datetime import datetime, timedelta

class VisitCounterViewAndExprieView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        # Get the current visit count and last visit time from the session
        visit_count = request.session.get('visit_count', 0)
        last_visit_time = request.session.get('last_visit_time')

        # Check if the session has expired (e.g., 1 hour)
        if last_visit_time:
            last_visit_time = datetime.fromisoformat(last_visit_time)
            if datetime.now() - last_visit_time > timedelta(minutes=5):
                # Reset the visit count if the session has expired
                visit_count = 0

        # Increment the visit count
        visit_count += 1

        # Save the updated visit count and current time in the session
        request.session['visit_count'] = visit_count
        request.session['last_visit_time'] = datetime.now().isoformat()

        # Return the visit count in the response
        return Response(
            {'message': f'You have visited this page {visit_count} times.'},
            status=status.HTTP_200_OK
        )