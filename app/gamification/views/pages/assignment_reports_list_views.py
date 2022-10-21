import pytz
from pytz import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from app.gamification.decorators import user_role_check
from app.gamification.forms import AssignmentForm
from app.gamification.models import Assignment, Course, Registration, Team, Membership, Artifact, Individual, FeedbackSurvey


@login_required
@user_role_check(user_roles=[Registration.UserRole.Instructor, Registration.UserRole.TA, Registration.UserRole.Student])
def view_reports(request, course_id, assignment_id):
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    userRole = Registration.objects.get(
        users=request.user, courses=course_id).userRole
    course = get_object_or_404(Course, pk=course_id)
    assignment_type = assignment.assignment_type
    is_individual = True
    if userRole == Registration.UserRole.Instructor or userRole == Registration.UserRole.TA:
        assignment_id = assignment.id
        students = []
        teams = []
        if assignment_type == "Individual":
            is_individual = True
            users = Registration.objects.filter(courses=course_id, userRole = Registration.UserRole.Student)
            counter = 0
            student_row = []
            for user in users:
                student_row.append(user)
                counter += 1
                if counter == 3:
                    students.append(student_row)
                    counter = 0
                    student_row = []
            students.append(student_row)
                
        elif assignment_type == "Team":
            is_individual = False
            all_teams = Team.objects.filter(course = course)
            team_row = []
            counter = 0
            for team in all_teams:
                team_row.append(team)
                counter += 1
                if counter == 3:
                    teams.append(team_row)
                    counter = 0
                    team_row = []
            teams.append(team_row)
        print(students)
        context = {'course_id': course_id,
                   'assignment_id': assignment_id,
                   'is_individual': is_individual,
                   'students': students,
                   'teams': teams

                   }
        return render(request, 'assignment_report_list.html', context)
    