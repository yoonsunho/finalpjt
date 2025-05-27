from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings  # 이걸 추가!
# User = settings.AUTH_USER_MODEL

class SavingRoom(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField(blank=True)
    goal_amount = models.PositiveIntegerField()
    deadline = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

        

    def total_saved(self):
        return sum([p.total_saved_amount() for p in self.participants.all()])

    def achievement_rate(self):
        if self.goal_amount == 0:
            return 0
        return round(self.total_saved() / self.goal_amount * 100, 2)

class SavingParticipant(models.Model):
    room = models.ForeignKey(SavingRoom, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')

    def total_saved_amount(self):
        return sum([d.amount for d in self.deposits.all()])

class SavingDeposit(models.Model):
    participant = models.ForeignKey(SavingParticipant, on_delete=models.CASCADE, related_name='deposits')
    amount = models.PositiveIntegerField()
    memo = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
