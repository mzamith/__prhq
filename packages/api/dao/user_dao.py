from api.models import User
from api.app import db

class UserDAO:
    
    def save_to_db(self, user: User):
        db.session.add(user)
        db.session.commit()

    def find_by_username(self, username):
        return User.query.filter_by(username = username).first()

    def return_all(self):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password_hash
            }
        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    def delete_all(self):
        try:
            num_rows_deleted = db.session.query(User).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}