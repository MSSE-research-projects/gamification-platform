from django.shortcuts import render


def test(request):
    user = request.user
    return render(request, 'test.html')


def test_survey_template(request):
    user = request.user
    return render(request, 'test-survey-template.html')


def test_report(request):
    return render(request, 'test-report.html')
