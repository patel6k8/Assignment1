import unittest
from datetime import datetime
from user import User
from comment import Comment

class TestComment(unittest.TestCase):

    def setUp(self):
        self.user = User("test_user", "test@example.com")
        self.valid_content = "This is a valid comment content."
        self.valid_tags = ["tag1", "tag2"]
        self.comment = Comment(self.user, self.valid_content, self.valid_tags)

    def test_valid_comment_creation(self):
        self.assertEqual(self.comment.content, self.valid_content)
        self.assertEqual(self.comment.tags, set(self.valid_tags))
        self.assertIsInstance(self.comment.created_on, datetime)
        self.assertEqual(self.comment._liked_by, [])

    def test_invalid_content(self):
        invalid_contents = ["ab", "a" * 2201]
        for invalid_content in invalid_contents:
            with self.assertRaises(ValueError):
                Comment(self.user, invalid_content)

    def test_invalid_tags(self):
        invalid_tags = ["invalid tag", "tag!" * 16]
        for invalid_tag in invalid_tags:
            with self.assertRaises(ValueError):
                Comment(self.user, self.valid_content, [invalid_tag])

    def test_add_tag(self):
        new_tag = "newtag"
        self.comment.add_tag(new_tag)
        self.assertIn(new_tag, self.comment.tags)

    def test_add_invalid_tag(self):
        with self.assertRaises(ValueError):
            self.comment.add_tag("invalid tag")

    def test_remove_tag(self):
        tag_to_remove = "tag1"
        self.comment.remove_tag(tag_to_remove)
        self.assertNotIn(tag_to_remove, self.comment.tags)

    def test_remove_nonexistent_tag(self):
        initial_tags = self.comment.tags.copy()
        self.comment.remove_tag("nonexistent_tag")
        self.assertEqual(self.comment.tags, initial_tags)

    def test_content_immutability(self):
        with self.assertRaises(AttributeError):
            self.comment.content = "New content"

    def test_created_on_immutability(self):
        with self.assertRaises(AttributeError):
            self.comment.created_on = datetime.now()

    def test_tags_immutability(self):
        with self.assertRaises(AttributeError):
            self.comment.tags = set(["newtag"])

    def test_valid_tag_edge_cases(self):
        self.assertTrue(Comment.is_valid_tag("a"))
        self.assertTrue(Comment.is_valid_tag("a" * 30))
        self.assertFalse(Comment.is_valid_tag("a" * 31))

    def test_valid_content_edge_cases(self):
        self.assertTrue(Comment.is_valid_content("abc"))
        self.assertTrue(Comment.is_valid_content("a" * 2200))
        self.assertFalse(Comment.is_valid_content("ab"))
        self.assertFalse(Comment.is_valid_content("a" * 2201))

    def test_comment_count(self):
        initial_count = Comment.get_comment_count()
        Comment(self.user, "Another comment")
        Comment(self.user, "Yet another comment")
        self.assertEqual(Comment.get_comment_count(), initial_count + 2)

if __name__ == '__main__':
    unittest.main()