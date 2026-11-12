from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from diagnosis.models import Patient, Scan, Result

User = get_user_model()


class AuthenticationAndSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='dr_test',
            email='dr_test@hospital.org',
            password='TestPassword123!',
            role='doctor',
            first_name='Test',
            last_name='Doctor'
        )

    def test_registration_success(self):
        """Test registering a new doctor user successfully."""
        response = self.client.post(reverse('register'), {
            'username': 'dr_new',
            'email': 'dr_new@hospital.org',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!',
            'role': 'doctor',
            'first_name': 'New',
            'last_name': 'Doctor'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='dr_new').exists())

    def test_registration_password_mismatch(self):
        """Test registration fails when passwords don't match."""
        response = self.client.post(reverse('register'), {
            'username': 'dr_fail',
            'email': 'dr_fail@hospital.org',
            'password': 'Password1!',
            'confirm_password': 'Password2!',
            'role': 'doctor',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='dr_fail').exists())

    def test_registration_duplicate_username(self):
        """Test registration fails with existing username."""
        response = self.client.post(reverse('register'), {
            'username': 'dr_test',
            'email': 'different@hospital.org',
            'password': 'StrongPassword123!',
            'confirm_password': 'StrongPassword123!',
            'role': 'doctor',
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.filter(username='dr_test').count(), 1)

    def test_login_success(self):
        """Test successful login with valid credentials."""
        response = self.client.post(reverse('login'), {
            'username': 'dr_test',
            'password': 'TestPassword123!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_invalid_password(self):
        """Test login fails with incorrect password."""
        response = self.client.post(reverse('login'), {
            'username': 'dr_test',
            'password': 'WrongPassword999'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password')

    def test_logout(self):
        """Test logging out terminates the session."""
        self.client.login(username='dr_test', password='TestPassword123!')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class NavigationAndAccessControlTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='dr_clinical',
            email='dr_clinical@hospital.org',
            password='TestPassword123!',
            role='doctor',
            first_name='Clinical',
            last_name='User'
        )
        self.patient = Patient.objects.create(
            name='Test Patient',
            age=62,
            gender='M',
            phone='1234567890',
            email='patient@test.com'
        )

    def test_unauthenticated_redirects(self):
        """Verify protected routes redirect anonymous visitors to login."""
        protected_routes = [
            reverse('dashboard'),
            reverse('upload_scan'),
            reverse('results'),
            reverse('patients'),
            reverse('statistics'),
            reverse('patient_detail', args=[self.patient.id]),
        ]
        for url in protected_routes:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 302, f"Expected redirect for {url}")
            self.assertTrue(response.url.startswith('/login/'))

    def test_authenticated_navigation(self):
        """Verify all dashboard and clinical routes return 200 for logged in users."""
        self.client.login(username='dr_clinical', password='TestPassword123!')
        routes = [
            reverse('dashboard'),
            reverse('upload_scan'),
            reverse('results'),
            reverse('patients'),
            reverse('statistics'),
            reverse('patient_detail', args=[self.patient.id]),
            reverse('patient_scans', args=[self.patient.id]),
        ]
        for url in routes:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, f"Expected 200 for {url}")


class PublicSEOAndDeploymentTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_robots_txt_exists_and_configured(self):
        """Test robots.txt is accessible and disallows private data while allowing public pages."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        content = response.content.decode()
        self.assertIn('Allow: /login/', content)
        self.assertIn('Disallow: /dashboard/', content)
        self.assertIn('Disallow: /diagnosis/', content)
        self.assertIn('Sitemap: https://brainstroke-0w0m.onrender.com/sitemap.xml', content)

    def test_sitemap_xml_exists_and_valid(self):
        """Test XML sitemap returns valid XML with public canonical URLs."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertIn('application/xml', response['Content-Type'])
        content = response.content.decode()
        self.assertIn('https://brainstroke-0w0m.onrender.com/login/', content)
        self.assertIn('https://brainstroke-0w0m.onrender.com/register/', content)

    def test_public_pages_have_meta_and_canonical(self):
        """Test login and register have SEO meta tags and canonical URL."""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('name="robots" content="index, follow"', content)
        self.assertIn('rel="canonical"', content)
        self.assertIn('NeuroScan AI', content)
