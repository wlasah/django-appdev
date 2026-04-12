from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Plant, WateringHistory, CareRequirements, SystemSettings, PlantType, Location, WateringSchedule, AutomationRule, AdminActionLog
from .serializers import (
    PlantSerializer, PlantCreateUpdateSerializer, 
    UserSerializer, UserRegistrationSerializer, 
    WateringHistorySerializer,
    SystemSettingsSerializer, PlantTypeSerializer, LocationSerializer,
    WateringScheduleSerializer, AutomationRuleSerializer, AdminActionLogSerializer
)


def is_admin(user):
    """Check if user is admin (for now, anyone logged in with 'admin' flag)"""
    return user.is_staff or user.username == 'admin'


class UserViewSet(viewsets.ModelViewSet):
    """Handle user registration and profile management"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register_admin(self, request):
        """Register an admin user (only if no superusers exist or with admin token)"""
        # Check if superuser already exists
        superuser_exists = User.objects.filter(is_superuser=True).exists()
        
        # If superusers exist, require admin authentication
        if superuser_exists:
            if not request.user.is_authenticated:
                return Response(
                    {'error': 'Admin authentication required'},
                    status=status.HTTP_403_FORBIDDEN
                )
            if not is_admin(request.user):
                return Response(
                    {'error': 'Admin access required'},
                    status=status.HTTP_403_FORBIDDEN
                )
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Make user admin
            user.is_staff = True
            user.is_superuser = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'is_admin': True
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """Login user and return token with user data"""
        from django.contrib.auth import authenticate
        
        username_display = request.data.get('username', '').strip()
        password = request.data.get('password')
        
        if not username_display or not password:
            return Response(
                {'error': 'username and password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Try to find user by display name (first_name field)
        # first_name stores the actual username with spaces
        user = User.objects.filter(first_name=username_display).first()
        
        if not user:
            # If not found by display name, try with underscores instead of spaces
            # (for backward compatibility if username was stored without spaces)
            username_alt = username_display.replace(' ', '_')
            user = User.objects.filter(username=username_alt).first()
        
        # Verify password
        if not user or not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'id': user.id,
            'username': user.first_name or user.username,  # Return display name (with spaces)
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'token': token.key
        })

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """Logout and delete token"""
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def all_users(self, request):
        """Get all users (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        users = User.objects.all().values('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
        return Response(list(users))

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def update_user_admin(self, request):
        """Update a user (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            
            # Prevent editing other admin accounts (unless it's yourself)
            if user.is_staff and user.id != request.user.id:
                return Response(
                    {'error': 'Cannot edit other admin accounts'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            # Update allowed fields
            if 'email' in request.data:
                user.email = request.data['email']
            if 'first_name' in request.data:
                user.first_name = request.data['first_name']
            if 'last_name' in request.data:
                user.last_name = request.data['last_name']
            
            # Handle password update (with proper hashing using set_password)
            if 'password' in request.data and request.data['password']:
                new_password = request.data['password']
                # Validate password length
                if len(new_password) < 6:
                    return Response(
                        {'error': 'Password must be at least 6 characters long'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # Use Django's set_password to properly hash the password
                user.set_password(new_password)
                print(f"[ADMIN] Password updated for user {user.username} (ID: {user.id})")
            
            # Prevent demoting other admins
            if 'is_staff' in request.data and not user.is_staff and request.data['is_staff']:
                # Allow promoting to admin
                user.is_staff = request.data['is_staff']
            elif 'is_staff' in request.data and user.is_staff and not request.data['is_staff'] and user.id != request.user.id:
                # Prevent demoting other admins
                return Response(
                    {'error': 'Cannot demote other admin accounts'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user.save()
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def delete_user_admin(self, request):
        """Delete a user (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            
            # Prevent deleting admin accounts
            if user.is_staff:
                return Response(
                    {'error': 'Cannot delete admin accounts'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            username = user.username
            user.delete()
            return Response({'message': f'User "{username}" deleted successfully'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def reset_password(self, request):
        """Reset a user's password (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        new_password = request.data.get('new_password')
        
        if not user_id or not new_password:
            return Response(
                {'error': 'user_id and new_password required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
            
            # Prevent resetting password for other admin accounts
            if user.is_staff and user.id != request.user.id:
                return Response(
                    {'error': 'Cannot reset password for other admin accounts'},
                    status=status.HTTP_403_FORBIDDEN
                )
            
            user.set_password(new_password)
            user.save()
            return Response({'message': f'Password for "{user.username}" has been reset'})
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def log_action(self, request):
        """Log an admin action (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        action_type = request.data.get('action_type')
        target_user_id = request.data.get('target_user_id')
        target_username = request.data.get('target_username')
        details = request.data.get('details', {})
        
        if not action_type or not target_user_id or not target_username:
            return Response(
                {'error': 'action_type, target_user_id, and target_username required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            target_user = User.objects.get(id=target_user_id)
            
            from .models import AdminActionLog
            action_log = AdminActionLog.objects.create(
                action_type=action_type,
                admin_user=request.user,
                target_user_id=target_user_id,
                target_username=target_username,
                target_user_email=target_user.email,
                details=details
            )
            
            serializer = AdminActionLogSerializer(action_log)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response(
                {'error': 'Target user not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def get_user_actions(self, request):
        """Get admin actions for a specific user"""
        target_user_id = request.query_params.get('target_user_id')
        limit = int(request.query_params.get('limit', 50))
        
        if not target_user_id:
            return Response(
                {'error': 'target_user_id query parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from .models import AdminActionLog
            actions = AdminActionLog.objects.filter(
                target_user_id=target_user_id
            ).order_by('-timestamp')[:limit]
            
            serializer = AdminActionLogSerializer(actions, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PlantViewSet(viewsets.ModelViewSet):
    """Handle plant CRUD operations"""
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return all plants for admin users, otherwise only current user's plants"""
        if is_admin(self.request.user):
            return Plant.objects.all()
        return Plant.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return PlantCreateUpdateSerializer
        return PlantSerializer

    def perform_create(self, serializer):
        """Automatically set the owner to current user"""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def water(self, request, pk=None):
        """Water a plant and record in history"""
        plant = self.get_object()
        
        # Get current moisture before watering
        moisture_before = plant.moisture
        
        # Update plant moisture and last watered time
        plant.moisture = min(100, plant.moisture + 20)  # Increase by 20% when watered
        plant.last_watered = timezone.now()
        plant.save()
        
        # Record in watering history
        WateringHistory.objects.create(
            plant=plant,
            moisture_before=moisture_before,
            moisture_after=plant.moisture,
            notes=request.data.get('notes', '')
        )
        
        return Response({
            'message': f'{plant.name} has been watered!',
            'plant': PlantSerializer(plant).data
        })

    @action(detail=False, methods=['get'])
    def needing_water(self, request):
        """Get plants that need watering (moisture < 40%)"""
        plants = self.get_queryset().filter(moisture__lt=40)
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get plant statistics for current user"""
        plants = self.get_queryset()
        return Response({
            'total_plants': plants.count(),
            'needing_water': plants.filter(moisture__lt=50).count(),
            'healthy': plants.filter(moisture__gte=50).count(),
            'average_moisture': sum([p.moisture for p in plants]) / max(plants.count(), 1)
        })

    @action(detail=False, methods=['get'])
    def admin_stats(self, request):
        """Get plant statistics for all users (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get ALL plants across all users
        plants = Plant.objects.all()
        return Response({
            'total_plants': plants.count(),
            'needing_water': plants.filter(moisture__lt=50).count(),
            'healthy': plants.filter(moisture__gte=50).count(),
            'average_moisture': sum([p.moisture for p in plants]) / max(plants.count(), 1)
        })

    @action(detail=False, methods=['get'])
    def all_plants(self, request):
        """Get all plants across all users (admin only) - for analytics and reporting"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get ALL plants across all users
        plants = Plant.objects.all()
        serializer = self.get_serializer(plants, many=True)
        return Response(serializer.data)


class WateringHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Handle watering history viewing"""
    serializer_class = WateringHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return watering history only for current user's plants"""
        return WateringHistory.objects.filter(plant__owner=self.request.user)

    @action(detail=False, methods=['get'])
    def by_plant(self, request):
        """Get watering history for a specific plant"""
        plant_id = request.query_params.get('plant_id')
        if not plant_id:
            return Response(
                {'error': 'plant_id query parameter required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            plant = Plant.objects.get(id=plant_id, owner=request.user)
            history = plant.watering_history.all()
            serializer = self.get_serializer(history, many=True)
            return Response(serializer.data)
        except Plant.DoesNotExist:
            return Response(
                {'error': 'Plant not found'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get'])
    def all_history(self, request):
        """Get all watering history across all users (admin only) - for analytics and reporting"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Get ALL watering history across all users
        history = WateringHistory.objects.all()
        serializer = self.get_serializer(history, many=True)
        return Response(serializer.data)


class SystemSettingsViewSet(viewsets.ModelViewSet):
    """Handle system settings (admin only)"""
    queryset = SystemSettings.objects.all()
    serializer_class = SystemSettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow admins to access
        if not is_admin(self.request.user):
            return SystemSettings.objects.none()
        return SystemSettings.objects.all()

    def list(self, request, *args, **kwargs):
        """Get system settings (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        settings = SystemSettings.objects.first()
        if not settings:
            settings = SystemSettings.objects.create()
        
        serializer = self.get_serializer(settings)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """Update system settings (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        settings = SystemSettings.objects.first()
        if not settings:
            settings = SystemSettings.objects.create()
        
        serializer = self.get_serializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PlantTypeViewSet(viewsets.ModelViewSet):
    """Handle plant type definitions"""
    queryset = PlantType.objects.all()
    serializer_class = PlantTypeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Create new plant type (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete plant type (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update plant type (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class LocationViewSet(viewsets.ModelViewSet):
    """Handle location definitions"""
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """Create new location (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete location (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update location (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class WateringScheduleViewSet(viewsets.ModelViewSet):
    """Handle watering schedules"""
    queryset = WateringSchedule.objects.all()
    serializer_class = WateringScheduleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically set creator to current user"""
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create new schedule (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete schedule (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update schedule (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)


class AutomationRuleViewSet(viewsets.ModelViewSet):
    """Handle automation rules"""
    queryset = AutomationRule.objects.all()
    serializer_class = AutomationRuleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Automatically set creator to current user"""
        serializer.save(created_by=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create new rule (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Delete rule (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Update rule (admin only)"""
        if not is_admin(request.user):
            return Response(
                {'error': 'Admin access required'},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)
