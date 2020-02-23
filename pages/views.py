from django.shortcuts import render

# Create your views here.
def IndexView(request):
    return render(request, 'pages/index.html')


def AboutView(request):
    return render(request, 'pages/about.html')


def FeedbackView(request):
    return render(request, 'pages/feedback.html')
