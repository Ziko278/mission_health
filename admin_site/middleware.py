from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


class AdminStudentRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip checking for URLs containing 'login'
        if 'login' in request.path:
            response = self.get_response(request)
            return response

        # Check for admin access
        if request.path.startswith('/myadmin/'):
            if request.user.is_authenticated and not request.user.is_superuser and not hasattr(request.user, 'user_staff_profile'):
                messages.error(request, 'ACCESS DENIED FOR CURRENT USER, LOGIN WITH APPROPRIATE ACCOUNT')
                return redirect(reverse('student_dashboard'))

        # Check for student access
        elif request.path.startswith('/student/'):
            if request.user.is_authenticated and not hasattr(request.user, 'user_student_profile'):
                messages.error(request, 'ACCESS DENIED FOR CURRENT USER, LOGIN WITH APPROPRIATE ACCOUNT')
                return redirect(reverse('admin_dashboard'))

        # Process the request
        response = self.get_response(request)
        return response
