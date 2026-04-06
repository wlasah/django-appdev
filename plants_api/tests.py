from django.test import TestCase
from django.contrib.auth.models import User
from plants_api.models import Plant, CareRequirements


class PlantModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_plant(self):
        plant = Plant.objects.create(
            owner=self.user,
            name='Monstera',
            type='Tropical',
            location='Living Room',
            moisture=50
        )
        self.assertEqual(plant.name, 'Monstera')
        self.assertEqual(plant.owner, self.user)

    def test_create_care_requirements(self):
        plant = Plant.objects.create(
            owner=self.user,
            name='Pothos',
            type='Vine',
            location='Bedroom'
        )
        care = CareRequirements.objects.create(
            plant=plant,
            water_frequency='Every 5 days',
            light_requirement='Low to bright light'
        )
        self.assertEqual(care.plant, plant)
