from user import User
from post import Post
from comment import Comment

class InstaMimicApp:

    def __init__(self):
        self.user_list = [] 
        self.posts_db = [] 

    def create_user(self, username, email):
        if any(existing_user.username == username for existing_user in self.user_list):
            raise ValueError(f"Username '{username}' is already taken.")
        
        new_user = User(username, email)
        self.user_list.append(new_user)
        return new_user

    def create_post(self, user, content, tags=None):
        new_post = Post(user, content, tags)
        self.posts_db.append(new_post)
        user._posts.append(new_post) 
        return new_post

    def delete_post(self, user, post):
        if post in user._posts:
            user._posts.remove(post)
            self.posts_db.remove(post)
            for liker in post.liked_by:
                liker._liked_posts.remove(post)
            for comment in post._comments:
                comment._author._comments.remove(comment)
                for liker in comment._liked_by:
                    liker._liked_comments.remove(comment)
                Comment.total_comments -= 1
            Post.total_posts -= 1

    def like_post(self, user, post):
        if post not in user._liked_posts:
            user._liked_posts.append(post)
            post.liked_by.append(user)

    def unlike_post(self, user, post):
        if post in user._liked_posts:
            user._liked_posts.remove(post)
            post.liked_by.remove(user)

    def comment_on_post(self, user, post, content, tags=None):
        new_comment = Comment(user, content, tags)
        post._comments.append(new_comment)
        user._comments.append(new_comment)
        return new_comment

    def delete_comment(self, user, post, comment):
        if comment in user._comments and comment in post._comments:
            user._comments.remove(comment)
            post._comments.remove(comment)
            for liker in comment._liked_by:
                liker._liked_comments.remove(comment)
            Comment.total_comments -= 1

    def like_comment(self, user, comment):
        if comment not in user._liked_comments:
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
