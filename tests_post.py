import unittest
from datetime import datetime
from user import User
from post import Post

class TestPost(unittest.TestCase):

    def setUp(self):
        self.user = User("test_user", "test@example.com")
        self.valid_content = "This is a valid post content."
        self.valid_tags = ["tag1", "tag2"]
        self.post = Post(self.user, self.valid_content, self.valid_tags)

    def test_valid_post_creation(self):
        self.assertEqual(self.post.content, self.valid_content)
        self.assertEqual(self.post.tags, set(self.valid_tags))
        self.assertIsInstance(self.post.created_on, datetime)
        self.assertEqual(self.post._liked_by, [])
        self.assertEqual(self.post._comments, [])

    def test_invalid_content(self):
        invalid_contents = ["ab", "a" * 2201]
        for invalid_content in invalid_contents:
            with self.assertRaises(ValueError):
                Post(self.user, invalid_content)

    def test_invalid_tags(self):
        invalid_tags = ["invalid tag", "tag!" * 16]
        for invalid_tag in invalid_tags:
            with self.assertRaises(ValueError):
                Post(self.user, self.valid_content, [invalid_tag])

    def test_add_tag(self):
        new_tag = "newtag"
        self.post.add_tag(new_tag)
        self.assertIn(new_tag, self.post.tags)

    def test_add_invalid_tag(self):
        with self.assertRaises(ValueError):
            self.post.add_tag("invalid tag")

    def test_remove_tag(self):
        tag_to_remove = "tag1"
        self.post.remove_tag(tag_to_remove)
        self.assertNotIn(tag_to_remove, self.post.tags)

    def test_remove_nonexistent_tag(self):
        initial_tags = self.post.tags.copy()
        self.post.remove_tag("nonexistent_tag")
        self.assertEqual(self.post.tags, initial_tags)

    def test_liked_by_property(self):
        liker = User("liker", "liker@example.com")
        self.post._liked_by.append(liker)
        self.assertIn(liker, self.post.liked_by)

    def test_content_immutability(self):
        with self.assertRaises(AttributeError):
            self.post.content = "New content"

    def test_created_on_immutability(self):
        with self.assertRaises(AttributeError):
            self.post.created_on = datetime.now()

    def test_tags_immutability(self):
        with self.assertRaises(AttributeError):
            self.post.tags = set(["newtag"])

    def test_valid_tag_edge_cases(self):
        self.assertTrue(Post.is_valid_tag("a"))
        self.assertTrue(Post.is_valid_tag("a" * 30))
        self.assertFalse(Post.is_valid_tag("a" * 31))

    def test_valid_content_edge_cases(self):
        self.assertTrue(Post.is_valid_content("abc"))
        self.assertTrue(Post.is_valid_content("a" * 2200))
        self.assertFalse(Post.is_valid_content("ab"))
        self.assertFalse(Post.is_valid_content("a" * 2201))

    def test_post_count(self):
        initial_count = Post.get_post_count()
        Post(self.user, "Another post")
        Post(self.user, "Yet another post")
        self.assertEqual(Post.get_post_count(), initial_count + 2)

if __name__ == '__main__':
    unittest.main()