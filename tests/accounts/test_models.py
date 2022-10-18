from django.test import TestCase

from accounts.models import User,UserManager


class TestUserModel(TestCase):
    def setUp(self) -> None:
        self.employee = {
            "first_name": "Dulqar",
            "last_name": "Salman",
            "username":"username",
            "email": "dulqar@gmail.com",
            "phone_number":"9876543210",
            "role": 2,
            "password": "Password@123",
        }
        self.user = User.objects.create(**self.employee)

    def test_string_representation(self):
        self.assertEqual(str(self.user), self.user.email)

    def test_verbose_name_plural(self):
        self.assertEqual(str(User._meta.verbose_name_plural), "users")

    def test_full_name(self):
        self.assertEqual(self.user.get_full_name(), "Dulqar Salman")

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("email").verbose_name
        self.assertEqual(field_label, "email")
    def test_get_role(self):
        role=self.user.role
        if role == 1:
            role = 'Employer'
        elif role == 2:
            role = 'Jobseeker'
        self.assertEqual(role,self.user.get_role())

class TestUserManager(TestCase):
    def setUp(self) -> None:
        pass

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "first_name": "Mamooty",
            "last_name": "Salman",
            "username": "username",
            "email": "Mamoty@gmail.com",
            "password": "Password@123",
        }

        cls.user=UserManager.objects.create(**cls.user_data)
        cls.super_user=UserManager(**cls.user_data)
        cls.super_user.is_admin = True
        cls.super_user.is_active = True
        cls.super_user.is_staff = True
        cls.super_user.is_superadmin = True
        cls.super_user.save()

    def test_username_max_length(self):
        max_length = self.job._meta.get_field("username").max_length
        self.assertEqual(max_length, 300)

    def test_username_label(self):
        field_label = self.job._meta.get_field("username").verbose_name
        self.assertEqual(field_label, "username")

    def test_str(self):
        self.assertEqual(self.user.__str__(), self.user.get_full_name())