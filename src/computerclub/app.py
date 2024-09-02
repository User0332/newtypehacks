import datetime
import os
import secrets
import secret_keys
from sockioevents import socketio
from typing import TypeVar
from flask import Response, jsonify, request
from webpy import App
from propelauth_flask import current_user, init_auth
from propelauth_flask.user import LoggedInUser


current_user: LoggedInUser
auth = init_auth(secret_keys.AUTH_URL, secret_keys.AUTH_API_KEY)

app = App(__name__, template_folder="html")

def webpy_setup(app: App):
	# expose auth & db for API routes
	global auth
	global db

	# expose db models for API routes
	global User, Message

	# expose db util methods
	global query_by_id
	global query_all_of
	global ensure_user
	global gen_id

	# Init application, auth, socketio & db
	app.secret_key = secret_keys.APP_SECRET_KEY
	
	db = app.sqlalchemy.init("sqlite:///database.db")
	socketio.init_app(app)

	# Define database models

	class User(db.Model):
		__tablename__ = "user"
		id: str = db.Column(db.String, primary_key=True, unique=True, nullable=False)
		name: str = db.Column(db.String, unique=True, nullable=False)
		messages = db.relationship("Message", backref=db.backref("author"), lazy=True)
	
		# schedule

		@property
		def authorized_channels(self) -> list[str]:
			return list(
				filter(None, self.authorized_channels_comma_sep.split(','))
			)
			
		@authorized_channels.setter
		def authorized_channels(self, value: list[str]):
			self.authorized_channels_comma_sep = ','.join(value)

	class CalendarItem(db.Model):
		__tablename__ = "calendaritem"

		id: str = db.Column(db.String, primary_key=True, unique=True, nullable=False)
		name: str = db.Column(db.String, unique=True, nullable=False)
		date: str = db.Column(db.String, unique=True, nullable=False)

	class Message(db.Model):
		__tablename__ = "message"

		id: str = db.Column(db.String, primary_key=True, unique=True, nullable=False)
		parent_user_id: str = db.Column(db.String, db.ForeignKey("user.id"), nullable=False)

		content: str = db.Column(db.String, nullable=False)
		timestamp: str = db.Column(db.String, nullable=False)

		# author: User


	T = TypeVar('T')

	def query_by_id(model_type: type[T], model_id: str) -> T: #I think  this is a beautiful line of code
		return db.session.execute(
			db.select(model_type).where(model_type.id == model_id)
		).scalar()
	
	def query_all_of(model_type: type[T]) -> list[T]:
		return list(
				db.session.execute(
				db.select(model_type)
			).scalars().all()
		)
	
	def ensure_user() -> User:		
		user = query_by_id(User, current_user.user_id)

		if user is None:
			user = User(
				id=current_user.user_id,
				name=current_user.user.first_name,
			)

			db.session.add(user)

			db.session.commit()

			return user

		return user
	
	def gen_id():
		return secrets.token_urlsafe(10)+str(datetime.datetime.now().timestamp())

	# reset db
	with app.app_context():
		if os.path.exists("instance/database.db"): os.remove("instance/database.db")
		
		db.create_all()

@app.route("/api/get-self")
@auth.require_user
def get_self():
	user = ensure_user()
				
	return jsonify({
		"id": user.id, 
		"name": user.name
	})


@app.route("/api/get-user")
@auth.require_user
def get_user():
	ensure_user()
	user_id = request.args.get("id")

	if not user_id: return Response(status=404)

	user = query_by_id(User, user_id)
 
	return jsonify({
		"id": user.id, 
		"name": user.name,
	})

@app.route("/api/list-messages")
@auth.require_user
def get_messages():
	ensure_user()

	return jsonify([message.id for message in query_all_of(Message)])

@app.route("/api/get-message")
@auth.require_user
def get_message():
	ensure_user()

	message = query_by_id(Message, request.args.get("id"))

	if not message: return Response(status=400)

	return jsonify({
		"author": message.author.id,
		"content": message.content
	})


@app.route("/api/send-message", methods=["POST"])
@auth.require_user
def send_message():
	user = ensure_user()

	content = request.json.get("content")

	if not content: return Response(status=400)

	message = Message(
		id=gen_id(),
		content=content,
		timestamp=datetime.datetime.now().isoformat(),
		parent_user_id=user.id
	)

	db.session.add(message)
	db.session.commit()

	socketio.emit("new-message", {
		"content": content,
		"authorName": user.name,
		"authorID": user.id
	})

	return jsonify({
		"status": "success",
		"reason": message.id
	})