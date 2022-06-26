from django.test import TestCase
from django.utils import timezone
from ..models import *
from django.contrib.auth.models import User


def modelInst():
    t_usr = User.objects.create(
        username = 'testuser1',
        password = 'hfjknalc'
    )
    t_cat = Category.objects.create(
        name = "test category one",
        slug = "test_category_one"
    )
    t_ad = Ad.objects.create(
        title = "Test AD",
        category = t_cat,
        price = 5.99,
        text = "Lorem ipsum dolor sit amet, consectetur adipisicing elit.",
        #Picture
        owner = t_usr
    )

class TestCategoryModel(TestCase):
    def setUp(self):
        modelInst()
    def test_str(self):
        cat = Category.objects.get(pk=1)
        self.assertEqual(str(cat),"test category one")
class TestAdModel(TestCase):
    def setUp(self):
        modelInst()
    def test_str(self):
        cat = Ad.objects.get(pk=1)
        self.assertEqual(str(cat),"Test AD")
    pass
