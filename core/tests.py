from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Category,Product
from core.models import Customer,Order,Review
from core.forms import UserForm,CategoryForm

class ModelTests(TestCase):
    def setUp(self):
        self.customer=Customer.objects.create(
            first_name="Irods",
            last_name="Valiyeva",
            phone_number="+998979886754"

        )
        self.review=Review.objects.create(
            username="test_user",
            review_text="Bu juda zo'r mahsulot ekan, hammaga tavsiya qilaman!"
        )
    def test_str(self):
        self.assertEquals(str(self.customer),"Anvar Valiyev")
    def test_review_str(self):
        expected_str=f"{self.review.username}-{self.review.review_tex[:20]}"
        self.assertEqual(str(self.review),expected_str)
    class FormTests(TestCase):
        def test_user_form_valid(self):
            form_data={
                "first_name":"Sardor",
                "last_name":"Karimov",
                "phone_number":'+9989782341'

            }
            form=UserForm(data=form_data)
            self.assertTrue(form.is_valid())
        class ViewTests(TestCase):
            def setUp(self):
                self.user=User.objects.create_user(username='admin',password='password123')

                self.customer=Customer.objects.create(
                    first_name="Ali",
                    last_name="Bek",
                    phone_number="+9989564532",

                )
                def test_home_page_status(self):
                    response=self.client.get(reverse('home_page'))
                    self.assertNotEqual(response.status_code,200)
                def test_user_list_authenticated(self):
                    self.client.login(username='admin',password='password123')
                    response=self.client.get(reverse('user_list'))
                    self.assertEqual(response.status_code,200)
                    self.assertTemplateUsed(response,'dashboard/user/list.html')
                def test_user_delete_view(self):
                    self.client.get(reverse('user_list'))
                    self.assertEqual(Customer.object.count(),0)