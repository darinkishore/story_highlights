from django.test import TestCase
from django.urls import reverse
from .forms import TextProcessingForm
from django.http import HttpResponse



class TextProcessingFormTests(TestCase):
    def test_form_valid(self):
        data = {'text': 'Sample text', 'choice': 'edit_one'}
        form = TextProcessingForm(data)
        self.assertTrue(form.is_valid())

    def test_form_invalid(self):
        data = {'text': '', 'choice': 'edit_one'}
        form = TextProcessingForm(data)
        self.assertFalse(form.is_valid())


class Edit1ViewTests(TestCase):
    def test_valid_form_submission(self):
        data = {'text': 'Sample text', 'choice': 'edit_one'}
        response = self.client.post(reverse('edit_1'), data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_submission(self):
        response = self.client.post(reverse('edit_1'))
        self.assertEqual(response.status_code, 400)


class Edit2ViewTests(TestCase):
    def test_valid_form_submission(self):
        data = {'text': 'Another sample text', 'choice': 'edit_two'}
        response = self.client.post(reverse('edit_2'), data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_submission(self):
        response = self.client.post(reverse('edit_2'))
        self.assertEqual(response.status_code, 400)


class HighlightViewTests(TestCase):
    def test_valid_form_submission(self):
        data = {'text': 'Highlight this text', 'choice': 'highlight'}
        response = self.client.post(reverse('highlight'), data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_form_submission(self):
        response = self.client.post(reverse('highlight'))
        self.assertEqual(response.status_code, 400)

# Create your tests here.
