from account.backends import JWTBackend
from django.contrib.auth import get_user_model
from django.test import TestCase, TransactionTestCase
from django.test.client import Client

User = get_user_model()


class AuthenticatedTestCase(TestCase):
    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            is_active=True,
            email="example@gmail.com",
            first_name="test",
            last_name="test",
        )
        self.staff = User.objects.create_user(
            username="teststaff",
            password="testpass",
            is_active=True,
            is_staff=True,
            email="example2@gmail.com",
            first_name="test",
            last_name="test",
        )

        user_token = JWTBackend.get_token(self.user)
        staff_token = JWTBackend.get_token(self.staff)

        self.client = Client()
        self.user_client = Client(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        self.staff_client = Client(HTTP_AUTHORIZATION=f"Bearer {staff_token}")


class TransactionAuthenticatedTestCase(TransactionTestCase):
    def setUp(self) -> None:
        super().setUp()

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
            is_active=True,
            email="example@gmail.com",
            first_name="test",
            last_name="test",
        )
        self.staff = User.objects.create_user(
            username="teststaff",
            password="testpass",
            is_active=True,
            is_staff=True,
            email="example2@gmail.com",
            first_name="test",
            last_name="test",
        )

        user_token = JWTBackend.get_token(self.user)
        staff_token = JWTBackend.get_token(self.staff)

        self.client = Client()
        self.user_client = Client(HTTP_AUTHORIZATION=f"Bearer {user_token}")
        self.staff_client = Client(HTTP_AUTHORIZATION=f"Bearer {staff_token}")
