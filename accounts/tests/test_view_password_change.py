from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(
            username='john',
            email='john@doe.com',
            password='old_password'
        )

        self.url = reverse('password_change')

        self.client.login(username='john', password='old_password')

        self.response = self.client.post(self.url, data)


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('password_change')

        login_url = reverse('login')

        response = self.client.get(url)

        self.assertRedirects(response, f'{login_url}?next={url}')


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })

    def test_redirection(self):
        """
        A valid form submission should redirect the user
        """

        password_change_done_url = reverse('password_change_done')

        self.assertRedirects(self.response, password_change_done_url)

    def test_password_changed(self):
        """
        refresh the user instance from database to get the new password
        hash updated by the change password view
        """

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password('new_password'))

    def test_user_authentication(self):
        """
        Create a new request to an arbitrary page.
        The resulting response should now have an 'user' to its context,
        after a successful sign up.
        """

        home_url = reverse('home')

        response = self.client.get(home_url)

        user = response.context.get('user')

        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        """
        An invalid form submission should return to the same page
        """

        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')

        self.assertTrue(form.errors)

    def test_didnt_change_password(self):
        """
        Refresh the user instance from the database to make
        sure we have the latest data.
        """

        self.user.refresh_from_db()

        self.assertTrue(self.user.check_password('old_password'))
