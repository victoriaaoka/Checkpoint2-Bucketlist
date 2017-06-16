from my_app import db


class User(db.Model):
    """This class represents the users table."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255))
    backetlists = db.relationship(
        "Bucketlist", order_by="Bucketlist.id", cascade="all, delete-orphan")

    def __init__(self, username):
        """initialize with username."""
        self.username = username

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Bucketlist(db.Model):
    """This class represents the bucketlists table."""

    __tablename__ = "bucketlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    items = db.relationship(
        "BucketlistItem", order_by="BucketlistItem.bucketlist_id",
        cascade="all, delete-orphan")

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Bucketlist.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)


class BucketlistItem(db.Model):
    """This class represents the bucketlist items table."""

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        Bucketlist.id), nullable=False)

    def __init__(self, name):
        """Initialize with name."""
        self.name = name
        self.bucketlist_id = bucketlist_id

    def save(self):
        """Save a new/edited bucketlist item"""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(bucketlist_id):
        """Retrieve all the bucketlists items in a given bucketlist"""
        return BucketListItem.query.filter_by(bucketlist_id=bucketlist_id)

    def delete(self):
        """Delete a bucketlist item"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<BucketlistItem: {}>".format(self.name)
