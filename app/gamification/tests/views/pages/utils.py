from app.gamification.models import CustomUser


class LogInUser:
    def createAndLogInUser(client, test_andrew_id, test_password):
        user = CustomUser.objects.create(andrew_id=test_andrew_id)
        user.set_password(test_password)
        user.save()
        client.login(andrew_id=test_andrew_id, password=test_password)
