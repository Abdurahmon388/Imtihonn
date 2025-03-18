import factory
from .models import Teacher, Student
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    phone = factory.Sequence(lambda n: f"+9989000000{n}")
    full_name = factory.Faker("name")
    password = factory.PostGenerationMethodCall("set_password", "password123")

class TeacherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Teacher

    user = factory.SubFactory(UserFactory)
    description = factory.Faker("text")

class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    is_active = True
