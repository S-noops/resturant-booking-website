from server import app
import unittest

class FlaskTestCase(unittest.TestCase):

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that the login/SignUp page loads correctly
    def test_login_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertIn(b'Login', response.data)

    # Ensure SignUp route works properly
    def test_signup_works(self):
        tester = app.test_client(self)
        response = tester.post("/sign_up_check", 
        data=dict(email="example@example.com", pass_="12345"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Ensure SignIn route works properly
    def test_signin_works(self):
        tester = app.test_client(self)
        response = tester.post("/sign_in_check", 
        data=dict(email="example@example.com", pass_="12345"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    # Ensure dashboard route works properly 
    def test_dashboard(self):
        tester = app.test_client(self)
        response = tester.get('/dashboard')
        self.assertIn(b'Click on the link below to Book tables in our resturant. ', response.data)

    # Ensure that bookings page loads properly 
    def test_bookings(self):
        tester = app.test_client(self)
        response = tester.get('/booking')
        self.assertIn(b'Resturant Booking Form', response.data)

    # Ensure that tables overview page loads properly 
    def test_tables_overview(self):
        tester = app.test_client(self)
        response =  tester.get('/tables')
        self.assertIn(b'Available seats', response.data)

    # Ensure the check_tables route is working properly
    def test_tables(self):
        tester = app.test_client(self)
        response = tester.post('/check_tables',
        data=dict(name="John Smith", email="johndoe@example.com", phone="321-321-1234", date="2021-06-06", time="12:21:00", guest_ids="5"), follow_redirects=True)
        self.assertIn(b"Chosen tables for you are", response.data)

    # Ensure the confirmation post route is working properly
    def test_confirmation(self):
        tester = app.test_client(self)
        response = tester.post('/confirmation',
        data=dict(name="John Smith", email="johndoe@example.com", phone="321-321-1234", date="2021-06-06", time="12:21:00", guest_ids="5", seat_ids="A1, A2, A3, A4, B1"), 
        follow_redirects=True)
        self.assertIn(b"no show", response.data)

    # Ensure the validate_signup post route is working properly
    def test_validate_signup(self):
        tester = app.test_client(self)
        response = tester.post('/validate_signup',
        data= dict(name_signup="John Smith", email_signup="johndoe@example.com", phone_signup="321-321-1234", date_signup="2021-06-06", time_signup="12:21:00", guest_ids_signup="5", seat_ids_signup="A1, A2, A3, A4, B1", signup_email="johndoe@example.com", signup_pass="12345"), follow_redirects=True)
        self.assertIn(b"no show", response.data)

    # Ensure the profile route is working properly
    def test_user_profile(self):
        tester = app.test_client(self)
        response = tester.get('/profile/johndoe@example.com')
        self.assertIn(b'Your Profile', response.data)

    # Ensure the update_details route is working properly
    def test_update_details(self):
        tester = app.test_client(self)
        response = tester.post('/update_details',
        data = dict(email="johndoe@example.com", name="John Doe", mailing_address="ABC Street, USA", billing_address="ABC Street, USA", pay="Cash"), 
        follow_redirects=True)
        self.assertIn(b"Your Profile", response.data)


if __name__ == '__main__':
    unittest.main()
