from django.shortcuts import render


def test(request):
    user = request.user
    return render(request, 'three_test.html')

def test2(request):
    user = request.user
    return render(request, 'three_test_dashboard.html')

def test3(request):
    user = request.user
    return render(request, 'three_test_survey.html')

def test_survey_template(request):
    user = request.user
    return render(request, 'test-survey-template.html')


def test_report(request):
    return render(request, 'test-report.html')
