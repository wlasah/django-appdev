from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Plant, WateringHistory, CareRequirements, SystemSettings, PlantType, Location, WateringSchedule, AutomationRule


class CareRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareRequirements
        fields = ['id', 'water_frequency', 'light_requirement', 'temperature', 'humidity']


class WateringHistorySerializer(serializers.ModelSerializer):
    plant_name = serializers.CharField(source='plant.name', read_only=True)
    
    class Meta:
        model = WateringHistory
        fields = ['id', 'plant', 'plant_name', 'watered_at', 'moisture_before', 'moisture_after', 'notes']
        read_only_fields = ['watered_at']


class PlantSerializer(serializers.ModelSerializer):
    care_requirements = CareRequirementsSerializer(read_only=True)
    watering_history = WateringHistorySerializer(many=True, read_only=True)
    owner_username = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = Plant
        fields = ['id', 'name', 'type', 'location', 'moisture', 'last_watered', 
                  'description', 'care_requirements', 'watering_history', 'created_at', 'owner_username']
        read_only_fields = ['id', 'created_at', 'owner_username']


class PlantCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating plants with nested care requirements"""
    care_requirements = CareRequirementsSerializer(required=False)

    class Meta:
        model = Plant
        fields = ['id', 'name', 'type', 'location', 'moisture', 'last_watered', 
                  'description', 'care_requirements']
        read_only_fields = ['id']

    def create(self, validated_data):
        care_req_data = validated_data.pop('care_requirements', None)
        plant = Plant.objects.create(**validated_data)
        
        if care_req_data:
            CareRequirements.objects.create(plant=plant, **care_req_data)
        else:
            CareRequirements.objects.create(plant=plant)
        
        return plant

    def update(self, instance, validated_data):
        care_req_data = validated_data.pop('care_requirements', None)
        
        # Update plant fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update care requirements if provided
        if care_req_data:
            if hasattr(instance, 'care_requirements'):
                for attr, value in care_req_data.items():
                    setattr(instance.care_requirements, attr, value)
                instance.care_requirements.save()
            else:
                CareRequirements.objects.create(plant=instance, **care_req_data)
        
        return instance


class UserSerializer(serializers.ModelSerializer):
    # Return display name (with spaces) instead of internal username
    username = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        # Return first_name if it has the display username, otherwise return username
        return obj.first_name if obj.first_name else obj.username
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        
        # Dont convert spaces - we'll store them in first_name
        username_display = data.get('username', '').strip()
        if not username_display:
            raise serializers.ValidationError({"username": "Username cannot be empty"})
        
        # Check if username already exists (check against first_name which stores the display name)
        if User.objects.filter(first_name=username_display).exists():
            raise serializers.ValidationError({"username": "This username is already taken"})
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        username_display = validated_data.pop('username', '').strip()
        
        # Convert spaces to underscores for the Django username field (database requirement)
        # Django username can only be 150 chars, alphanumeric + underscore/hyphen
        django_username = username_display.replace(' ', '_')
        
        # Ensure uniqueness of the django username
        counter = 1
        original_django_username = django_username
        while User.objects.filter(username=django_username).exists():
            django_username = f"{original_django_username}_{counter}"
            counter += 1
        
        # Store the display name (with spaces) in first_name
        # The username field stores the internal django username
        user = User.objects.create_user(
            username=django_username,
            first_name=username_display,  # Store the original name with spaces for display
            **validated_data
        )
        user.set_password(password)
        user.save()
        return user


class SystemSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSettings
        fields = ['id', 'critical_threshold', 'warning_threshold', 'healthy_threshold',
                  'notification_frequency', 'enable_email_notifications', 'enable_system_alerts',
                  'auto_archive_dead_plants', 'dead_plant_threshold', 'data_retention_days',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PlantTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantType
        fields = ['id', 'name', 'watering_frequency', 'light_requirement', 'temp_range',
                  'humidity', 'soil_type', 'common_issues', 'care_instructions',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'name', 'light_level', 'humidity', 'temperature',
                  'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class WateringScheduleSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    plant_type_name = serializers.CharField(source='plant_type.name', read_only=True)

    class Meta:
        model = WateringSchedule
        fields = ['id', 'name', 'plant_type', 'plant_type_name', 'frequency', 'water_amount',
                  'optimal_time_of_day', 'created_by', 'created_by_username', 'notes',
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class AutomationRuleSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = AutomationRule
        fields = ['id', 'name', 'trigger', 'trigger_value', 'action', 'is_active',
                  'created_by', 'created_by_username', 'notes', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']
