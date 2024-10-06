import unittest
from instamimic import InstaMimicApp
from user import User
from post import Post
from comment import Comment

class TestInstaMimicApp(unittest.TestCase):

    def setUp(self):
        self.app = InstaMimicApp()
        self.user1 = self.app.create_user("user1", "user1@example.com")
        self.user2 = self.app.create_user("user2", "user2@example.com")

    def test_create_user(self):
        user = self.app.create_user("newuser", "newuser@example.com")
        self.assertIsInstance(user, User)
        self.assertIn(user, self.app.users)

    def test_create_user_duplicate_username(self):
        with self.assertRaises(ValueError):
            self.app.create_user("user1", "different@example.com")

    def test_create_post(self):
        post = self.app.create_post(self.user1, "Test post", ["tag1", "tag2"])
        self.assertIsInstance(post, Post)
        self.assertIn(post, self.app.posts)
        self.assertIn(post, self.user1._posts)

    def test_create_post_invalid_content(self):
        with self.assertRaises(ValueError):
            self.app.create_post(self.user1, "a" * 2201)

    def test_delete_post(self):
        post = self.app.create_post(self.user1, "Test post")
        self.app.like_post(self.user2, post)
        comment = self.app.comment_on_post(self.user2, post, "Great post!")
        self.app.like_comment(self.user1, comment)
        
        initial_post_count = Post.get_post_count()
        initial_comment_count = Comment.get_comment_count()
        
        self.app.delete_post(self.user1, post)
        
        self.assertNotIn(post, self.app.posts)
        self.assertNotIn(post, self.user1._posts)
        self.assertNotIn(post, self.user2._liked_posts)
        self.assertNotIn(comment, self.user2._comments)
        self.assertNotIn(comment, self.user1._liked_comments)
        self.assertEqual(Post.get_post_count(), initial_post_count - 1)
        self.assertEqual(Comment.get_comment_count(), initial_comment_count - 1)

    def test_delete_nonexistent_post(self):
        post = Post(self.user1, "Not in app")
        initial_post_count = Post.get_post_count()
        self.app.delete_post(self.user1, post)
        self.assertEqual(Post.get_post_count(), initial_post_count)

    def test_like_post(self):
        post = self.app.create_post(self.user1, "Test post")
        self.app.like_post(self.user2, post)
        self.assertIn(post, self.user2._liked_posts)
        self.assertIn(self.user2, post._liked_by)

    def test_like_own_post(self):
        post = self.app.create_post(self.user1, "Test post")
        self.app.like_post(self.user1, post)
        self.assertNotIn(post, self.user1._liked_posts)
        self.assertNotIn(self.user1, post._liked_by)

    def test_unlike_post(self):
        post = self.app.create_post(self.user1, "Test post")
        self.app.like_post(self.user2, post)
        self.app.unlike_post(self.user2, post)
        self.assertNotIn(post, self.user2._liked_posts)
        self.assertNotIn(self.user2, post._liked_by)

    def test_unlike_not_liked_post(self):
        post = self.app.create_post(self.user1, "Test post")
        self.app.unlike_post(self.user2, post)  # Should not raise an error
        self.assertNotIn(post, self.user2._liked_posts)
        self.assertNotIn(self.user2, post._liked_by)

    def test_comment_on_post(self):
        post = self.app.create_post(self.user1, "Test post")
        comment = self.app.comment_on_post(self.user2, post, "Great post!")
        self.assertIsInstance(comment, Comment)
        self.assertIn(comment, post._comments)
        self.assertIn(comment, self.user2._comments)

    def test_comment_on_post_invalid_content(self):
        post = self.app.create_post(self.user1, "Test post")
        with self.assertRaises(ValueError):
            self.app.comment_on_post(self.user2, post, "a" * 2201)

    def test_delete_comment(self):
        post = self.app.create_post(self.user1, "Test post")
        comment = self.app.comment_on_post(self.user2, post, "Great post!")
        self.app.like_comment(self.user1, comment)
        
        initial_comment_count = Comment.get_comment_count()
        
        self.app.delete_comment(self.user2, post, comment)
        
        self.assertNotIn(comment, post._comments)
        self.assertNotIn(comment, self.user2._comments)
        self.assertNotIn(comment, self.user1._liked_comments)
        self.assertEqual(Comment.get_comment_count(), initial_comment_count - 1)

    def test_delete_nonexistent_comment(self):
        post = self.app.create_post(self.user1, "Test post")
        comment = Comment(self.user2, "Not in app")
        initial_comment_count = Comment.get_comment_count()
        self.app.delete_comment(self.user2, post, comment)
        self.assertEqual(Comment.get_comment_count(), initial_comment_count)

    def test_like_comment(self):
        post = self.app.create_post(self.user1, "Test post")
        comment = self.app.comment_on_post(self.user2, post, "Great post!")
        self.app.like_comment(self.user1, comment)
        self.assertIn(comment, self.user1._liked_comments)
        self.assertIn(self.user1, comment._liked_by)

    def test_like_own_comment(self):
        post = self.app.create_post(self.user1, "Test post")
        comment = self.app.comment_on_post(self.user2, post, "Great post!")
        self.app.like_comment(self.user2, comment)
        self.assertNotIn(comment, self.user2._liked_comments)
        self.assertNotIn(self.user2, comment._liked_by)

    def test_unlike_comment(self):
        post = self.app.create_post(self.user1, "Test post")
        comment = self.app.comment_on_post(self.user2, post, "Great post!")
        self.app.like_comment(self.user1, comment)
        self.app.unlike_comment(self.user1, comment)
        self.assertNotIn(comment, self.user1._liked_comments)
        self.assertNotIn(self.user1, comment._liked_by)

    def test_unlike_not_liked_comment(self):
        post = self.app.create_post(self.user1, "Test post")
        comment = self.app.comment_on_post(self.user2, post, "Great post!")
        self.app.unlike_comment(self.user1, comment)  # Should not raise an error
        self.assertNotIn(comment, self.user1._liked_comments)
        self.assertNotIn(self.user1, comment._liked_by)

    def test_follow_user(self):
        self.app.follow_user(self.user1, self.user2)
        self.assertIn(self.user2, self.user1.following)
        self.assertIn(self.user1, self.user2.followers)

    def test_follow_self(self):
        self.app.follow_user(self.user1, self.user1)
        self.assertNotIn(self.user1, self.user1.following)
        self.assertNotIn(self.user1, self.user1.followers)

    def test_follow_already_following(self):
        self.app.follow_user(self.user1, self.user2)
        self.app.follow_user(self.user1, self.user2)  # Should not duplicate
        self.assertEqual(self.user1.following.count(self.user2), 1)
        self.assertEqual(self.user2.followers.count(self.user1), 1)

    def test_unfollow_user(self):
        self.app.follow_user(self.user1, self.user2)
        self.app.unfollow_user(self.user1, self.user2)
        self.assertNotIn(self.user2, self.user1.following)
        self.assertNotIn(self.user1, self.user2.followers)

    def test_unfollow_not_following(self):
        self.app.unfollow_user(self.user1, self.user2)  # Should not raise an error
        self.assertNotIn(self.user2, self.user1.following)
        self.assertNotIn(self.user1, self.user2.followers)

if __name__ == '__main__':
    unittest.main()