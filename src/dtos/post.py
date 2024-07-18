from ..models.post import Post
from src import db

class PostDTO:
    def __init__(self, model):
        self.model = model    
    # get all posts
    def get_all(self):
        return Post.query.order_by(Post.created_at.desc()).all()
    # get all posts by user
    def get_by_user(self, user_id):
        return (
            Post.query.filter(Post.created_by==user_id)
            .order_by(Post.created_at.desc())
            .all()
        )
    # get a post by id
    def get_by_id(self, id: int):
        return (
            Post.query.get(id)
         )
    # create a post
    def create_post(self, new_post: Post):
        db.session.add(new_post)
        db.session.commit()
    # update a post by id
    def update_by_id(self, id: int, updated_obj: object):
        post = db.session.query(self.model).filter(self.model.id==id)
        post.update(updated_obj)
        db.session.commit()
    # delete a post by id
    def delete_by_id(self, id:int):
        delete_post = Post.query.filter(Post.id==id)
        delete_post.delete()
        db.session.commit()
    # def get_by_email(self, email -> str):
    #     return (
    #         session.query(self.model)
    #         .filter_by(email=email)
    #         .first()
    #      )
post_dto = PostDTO(Post)