from django.test import TestCase
from .models import Component, Script
from django.contrib.auth.models import User


# Create your tests here.

class ComponentTest(TestCase):
    def setUp(self):


        # populate test data base with new user
        me= User.objects.create_user('gregory', 'gregory@email.com', 'gregory_password')

        # populate test data base with new components
        for i in range(1,5):
        	Component.objects.create(name="C%i" % i,
                                         description="Component %i" % i,
                                         author=me,
                                         function="f%i" % i,
                                         jacobian=Script(language="c",txt="j%i" % i))


    def test_scriptfield(self):

        C2 = Component.objects.get(name="C2")
        print(C2.__class__)
        F2=C2.function
        print(F2.__class__)
        J2=C2.jacobian
        print(J2.__class__)
        self.assertEqual(C2.jacobian.txt, "j2")


    def test_jsonfield(self):

        C2 = Component.objects.get(name="C2")
        print(C2.__class__)
        F2=C2.function
        print(F2.__class__)
        J2=C2.jacobian
        print(J2.__class__)
        self.assertEqual(C2.jacobian.txt, "j2")


  
