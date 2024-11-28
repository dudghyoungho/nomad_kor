from django.shortcuts import render

def signup_view(request):
    """
    사용자 위치를 기반으로 주변 카페를 표시하는 HTML 렌더링.
    """
    return render(request, 'signup.html')
