from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ================= USERS TABLE =================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    profile_photo = db.Column(
        db.String(255),
        default="default.png"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


# ================= PREDICTIONS TABLE =================

class Prediction(db.Model):

    __tablename__ = "predictions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    username = db.Column(
        db.String(100),
        nullable=False
    )

    # User's Input Text (post/content analyzed)
    input_text = db.Column(
        db.Text,
        nullable=True
    )

    # OCEAN Scores
    openness = db.Column(
        db.Float,
        nullable=False
    )

    conscientiousness = db.Column(
        db.Float,
        nullable=False
    )

    extraversion = db.Column(
        db.Float,
        nullable=False
    )

    agreeableness = db.Column(
        db.Float,
        nullable=False
    )

    neuroticism = db.Column(
        db.Float,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    user = db.relationship(
        "User",
        backref="predictions"
    )