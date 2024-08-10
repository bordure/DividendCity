from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from Dywidendy_GPW.models import UserProfile
from Dywidendy_GPW.signals import create_user_profile, save_user_profile
from django.db.models.signals import post_save

class UserProfileModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        post_save.disconnect(create_user_profile, sender=User)
        post_save.disconnect(save_user_profile, sender=User)
        cls.user = User.objects.create_user(username='userprofiletest', password='testpassword')
        cls.user_profile = UserProfile.objects.create(
            user=cls.user,
            monthly_dividend_goal=500.00
        )
    
    @classmethod
    def tearDownClass(cls):
        cls.user_profile.delete()
        cls.user.delete()
        super().tearDownClass()
    
    def test_string_representation(self):
        self.assertEqual(str(self.user_profile), 'userprofiletest')
    
    def test_monthly_dividend_goal_field(self):
        self.assertEqual(self.user_profile.monthly_dividend_goal, 500.00)
    
    def test_negative_dividend_goal(self):
        user_profile = UserProfile(user=self.user)
        user_profile.monthly_dividend_goal = -100.00
        
        with self.assertRaises(ValidationError):
            user_profile.full_clean()