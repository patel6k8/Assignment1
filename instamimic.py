# File: main.py
from user import User
from post import Post
from comment import Comment

class InstaMimicApp:

    def __init__(self):
        self.users = []
        self.posts = []

    def create_user(self, username, email):
        # Check if a user with the given username already exists
        if any(user._username == username for user in self.users):
            raise ValueError(f"Username '{username}' is already taken.")
        user = User(username, email)
        self.users.append(user)
        return user

    def create_post(self, user, content, tags=None):
        post = Post(user, content, tags)
        self.posts.append(post)
        user._posts.append(post)
        return post

    def delete_post(self, user, post):
        if post in user._posts:
            # Remove the post from the user's posts
            user._posts.remove(post)
            
            # Remove the post from the global posts list
            self.posts.remove(post)
            
            # Remove likes on this post
            for liker in post._liked_by:
                liker._liked_posts.remove(post)
            
            # Remove comments on this post
            for comment in post._comments:
                # Remove the comment from the author's comments
                comment._author._comments.remove(comment)
                
                # Remove likes on this comment
                for comment_liker in comment._liked_by:
                    comment_liker._liked_comments.remove(comment)
                
                # Decrease the comment count
                Comment.comment_count -= 1
            
            # Decrease the post count
            Post.post_count -= 1

    def like_post(self, user, post):
        if post not in user._posts and post not in user._liked_posts:
            user._liked_posts.append(post)
            post._liked_by.append(user)

    def unlike_post(self, user, post):
        if post in user._liked_posts:
            user._liked_posts.remove(post)
            post._liked_by.remove(user)

    def comment_on_post(self, user, post, content, tags=None):
        comment = Comment(user, content, tags)
        post._comments.append(comment)
        user._comments.append(comment)
        return comment

    def delete_comment(self, user, post, comment):
        if comment in user._comments and comment in post._comments:
            # Remove the comment from the user's comments
            user._comments.remove(comment)
            
            # Remove the comment from the post's comments
            post._comments.remove(comment)
            
            # Remove likes on this comment
            for liker in comment._liked_by:
                liker._liked_comments.remove(comment)
            
            # Decrease the comment count
            Comment.comment_count -= 1

    def like_comment(self, user, comment):
        if comment not in user._comments and comment not in user._liked_comments:
            user._liked_comments.append(comment)
            comment._liked_by.append(user)

    def unlike_comment(self, user, comment):
        if comment in user._liked_comments:
            user._liked_comments.remove(comment)
            comment._liked_by.remove(user)

    def follow_user(self, follower, followee):
        if follower != followee and followee not in follower.following:
            follower.following.append(followee)
            followee.followers.append(follower)

    def unfollow_user(self, follower, followee):
        if followee in follower.following:
            follower.following.remove(followee)
            followee.followers.remove(follower)