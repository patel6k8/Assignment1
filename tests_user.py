import unittest
from datetime import datetime
from user import User

class TestUser(unittest.TestCase):

    def setUp(self):
        self.valid_username = "valid_user123"
        self.valid_email = "valid@example.com"
        self.user = User(self.valid_username, self.valid_email)

    def test_valid_user_creation(self):
        self.assertEqual(self.user.username, self.valid_username)
        self.assertEqual(self.user.email, self.valid_email)
        self.assertIsInstance(self.user.joined_on, datetime)
        self.assertEqual(self.user.bio, "")
        self.assertEqual(self.user._posts, [])
        self.assertEqual(self.user._liked_posts, [])
        self.assertEqual(self.user._comments, [])
        self.assertEqual(self.user._liked_comments, [])
        self.assertEqual(self.user.following, [])
        self.assertEqual(self.user.followers, [])

    def test_invalid_username(self):
        invalid_usernames = ["ab", "a" * 31, "invalid user", "user@name", "user!name"]
        for invalid_username in invalid_usernames:
            with self.assertRaises(ValueError):
                User(invalid_username, self.valid_email)

    def test_invalid_email(self):
        invalid_emails = ["invalid", "invalid@", "@invalid.com", "invalid@.com", "invalid@com."]
        for invalid_email in invalid_emails:
            with self.assertRaises(ValueError):
                User(self.valid_username, invalid_email)

    def test_bio_setter(self):
        new_bio = "This is a valid bio."
        self.user.bio = new_bio
        self.assertEqual(self.user.bio, new_bio)

    def test_bio_setter_too_long(self):
        with self.assertRaises(ValueError):
            self.user.bio = "a" * 151

    def test_posts_property(self):
        self.assertEqual(self.user.posts, [])
        self.user._posts.append("test_post")
        self.assertEqual(self.user.posts, ["test_post"])

    def test_joined_on_immutability(self):
        with self.assertRaises(AttributeError):
            self.user.joined_on = datetime.now()

    def test_username_immutability(self):
        with self.assertRaises(AttributeError):
            self.user.username = "new_username"

    def test_email_immutability(self):
        with self.assertRaises(AttributeError):
            self.user.email = "new_email@example.com"

    def test_valid_username_edge_cases(self):
        self.assertTrue(User.is_valid_username("abc"))
        self.assertTrue(User.is_valid_username("a" * 30))
        self.assertTrue(User.is_valid_username("user.name_123"))

    def test_valid_email_edge_cases(self):
        self.assertTrue(User.is_valid_email("a@b.c"))
        self.assertTrue(User.is_valid_email("user.name+tag@example.co.uk"))

    def test_user_count(self):
        initial_count = User.get_user_count()
        User("new_user1", "new1@example.com")
        User("new_user2", "new2@example.com")
        self.assertEqual(User.get_user_count(), initial_count + 2)

if __name__ == '__main__':
    unittest.main()