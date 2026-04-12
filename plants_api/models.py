from django.db import models
from django.contrib.auth.models import User


class Plant(models.Model):
    """Model for storing plant information"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plants')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    moisture = models.IntegerField(default=0)  # 0-100 percentage
    last_watered = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.owner.username}"


class CareRequirements(models.Model):
    """Model for plant care requirements"""
    plant = models.OneToOneField(Plant, on_delete=models.CASCADE, related_name='care_requirements')
    water_frequency = models.CharField(max_length=100, default="Every 7 days")
    light_requirement = models.CharField(max_length=100, default="Bright indirect light")
    temperature = models.CharField(max_length=100, default="65-75°F")
    humidity = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Care Requirements"

    def __str__(self):
        return f"Care for {self.plant.name}"


class WateringHistory(models.Model):
    """Model for tracking watering history"""
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='watering_history')
    watered_at = models.DateTimeField(auto_now_add=True)
    moisture_before = models.IntegerField()
    moisture_after = models.IntegerField(default=80)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-watered_at']
        verbose_name_plural = "Watering Histories"

    def __str__(self):
        return f"{self.plant.name} - Watered at {self.watered_at}"


class SystemSettings(models.Model):
    """Model for system-wide settings"""
    critical_threshold = models.IntegerField(default=30)
    warning_threshold = models.IntegerField(default=50)
    healthy_threshold = models.IntegerField(default=70)
    notification_frequency = models.CharField(
        max_length=50,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('immediately', 'Immediately'),
        ],
        default='daily'
    )
    enable_email_notifications = models.BooleanField(default=True)
    enable_system_alerts = models.BooleanField(default=True)
    auto_archive_dead_plants = models.BooleanField(default=False)
    dead_plant_threshold = models.IntegerField(default=10)  # days without watering
    data_retention_days = models.IntegerField(default=90)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "System Settings"

    def __str__(self):
        return "System Settings"


class PlantType(models.Model):
    """Model for plant type definitions with care requirements"""
    name = models.CharField(max_length=100, unique=True)
    watering_frequency = models.CharField(max_length=100, default="Weekly")
    light_requirement = models.CharField(max_length=100, default="Moderate")
    temp_range = models.CharField(max_length=100, default="18-24°C")
    humidity = models.CharField(max_length=100, default="Moderate")
    soil_type = models.CharField(max_length=100, default="Well-draining")
    common_issues = models.TextField(blank=True)
    care_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    """Model for plant locations"""
    name = models.CharField(max_length=100, unique=True)
    light_level = models.CharField(max_length=100, default="Moderate")
    humidity = models.CharField(max_length=100, default="Moderate")
    temperature = models.IntegerField(default=20)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WateringSchedule(models.Model):
    """Model for watering schedules"""
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('every-2-days', 'Every 2 Days'),
        ('every-3-days', 'Every 3 Days'),
        ('weekly', 'Weekly'),
        ('bi-weekly', 'Bi-weekly'),
        ('monthly', 'Monthly'),
    ]
    
    name = models.CharField(max_length=100)
    plant_type = models.ForeignKey(PlantType, on_delete=models.CASCADE, related_name='schedules')
    frequency = models.CharField(max_length=50, choices=FREQUENCY_CHOICES, default='weekly')
    water_amount = models.IntegerField(default=50)  # percentage
    optimal_time_of_day = models.TimeField(default='06:00')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_schedules')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.plant_type.name}"


class AutomationRule(models.Model):
    """Model for automation rules"""
    TRIGGER_CHOICES = [
        ('moisture', 'Moisture Level'),
        ('time', 'Time-based'),
        ('weather', 'Weather-based'),
    ]
    
    ACTION_CHOICES = [
        ('send_alert', 'Send Alert'),
        ('trigger_watering', 'Trigger Watering'),
        ('send_notification', 'Send Notification'),
    ]
    
    name = models.CharField(max_length=100)
    trigger = models.CharField(max_length=50, choices=TRIGGER_CHOICES)
    trigger_value = models.CharField(max_length=200)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_rules')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AdminActionLog(models.Model):
    """Model for logging admin management actions"""
    ACTION_CHOICES = [
        ('create_user', 'Create User'),
        ('update_user', 'Update User'),
        ('delete_user', 'Delete User'),
        ('reset_password', 'Reset Password'),
        ('change_role', 'Change Role'),
    ]
    
    action_type = models.CharField(max_length=50, choices=ACTION_CHOICES)
    admin_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_actions_performed')
    target_user_id = models.IntegerField()
    target_username = models.CharField(max_length=150)
    target_user_email = models.CharField(max_length=254, blank=True, null=True)
    details = models.JSONField(default=dict, blank=True)  # Store extra details like old/new values
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['target_user_id', '-timestamp']),
            models.Index(fields=['admin_user', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.admin_user.username} - {self.action_type} on {self.target_username}"
