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

app = App(__name__, template_folder="html")

def webpy_setup(app: App):
	# Init application, auth, socketio & db
	app.secret_key = secret_keys.APP_SECRET_KEY
	
	db = app.sqlalchemy.init("sqlite:///database.db")
	socketio.init_app(app)
	auth = init_auth(secret_keys.AUTH_URL, secret_keys.AUTH_API_KEY)

	# Define database models

	class User(db.Model):
		__tablename__ = "user"
		id: str = db.Column(db.String, primary_key=True, unique=True, nullable=False)
		name: str = db.Column(db.String, unique=True, nullable=False)
		email: str = db.Column(db.String, unique=True, nullable=False)
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

	class CalendarEvent(db.Model):
		__tablename__ = "calendarevent"

		id: str = db.Column(db.String, primary_key=True, unique=True, nullable=False)
		title: str = db.Column(db.String, nullable=False)
		description: str = db.Column(db.String, nullable=False)
		start_datetime: str = db.Column(db.String, nullable=False)
		end_datetime: str = db.Column(db.String, nullable=False)

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
				email=current_user.user.email
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

		events = []

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Club Meeting",
				description="Our kick-off meeting for the year. We will get to know each other and come up with plans for the rest of the year. Donuts will be provided 😉",
				start_datetime="2024-09-03T10:30:00",
				end_datetime="2024-09-03T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Club Meeting",
				description="First computer club challenge of the year! (Definately NOT just a renamed leetcode problem)",
				start_datetime="2024-09-05T10:30:00",
				end_datetime="2024-09-05T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Project",
				description="First computer club challenge of the year! (Definately NOT just a renamed leetcode problem)",
				start_datetime="2024-09-05T10:30:00",
				end_datetime="2024-09-05T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Personal Projects and Tutoring",
				description="Come and work on what you want! We'll be there to help 😊",
				start_datetime="2024-09-06T14:15:00",
				end_datetime="2024-09-06T16:00:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Club Meeting",
				description="Rust. A language of the future or a fad? Find out. meeting.hasTreats = True",
				start_datetime="2024-09-10T10:30:00",
				end_datetime="2024-09-10T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Club Meeting",
				description="Machine Learning fundementals! Bootcamp Week One",
				start_datetime="2024-09-12T10:30:00",
				end_datetime="2024-09-12T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Personal Projects and Tutoring",
				description="All welcome! Make some progress 💪",
				start_datetime="2024-09-13T14:15:00",
				end_datetime="2024-09-13T16:00:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Monday Mayhem",
				description="Weekly Challenge Launch!",
				start_datetime="2024-09-16T10:30:00",
				end_datetime="2024-09-16T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Club Meeting",
				description="Machine Learning Bootcamp week 2: Electric Boogaloo",
				start_datetime="2024-09-17T10:30:00",
				end_datetime="2024-09-17T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Robotics Meeting",
				description="Plan our team's strategy for the year",
				start_datetime="2024-09-18T8:30:00",
				end_datetime="2024-09-18T9:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Personal Projects and Tutoring",
				description="You know the drill. Be there or be square.",
				start_datetime="2024-09-20T14:15:00",
				end_datetime="2024-09-20T16:00:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Monday Mayhem",
				description="Weekly Challenge Launch!",
				start_datetime="2024-09-23T10:30:00",
				end_datetime="2024-09-23T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Club Meeting",
				description="Machine Learning Bootcamp week 3: Lets implement it!",
				start_datetime="2024-09-24T10:30:00",
				end_datetime="2024-09-24T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Club Meeting",
				description="Back to the basics: writing good code",
				start_datetime="2024-09-26T10:30:00",
				end_datetime="2024-09-26T11:15:00"
			)
		)

		events.append(
			CalendarEvent(
				id=gen_id(),
				title="Monday Mayhem",
				description="Weekly Challenge Launch!",
				start_datetime="2024-09-30T10:30:00",
				end_datetime="2024-09-30T11:15:00"
			)
		)

		for event in events:
			db.session.add(event)

		db.session.commit()

	@app.route("/api/get-self")
	@auth.require_user
	def get_self():
		user = ensure_user()
					
		return jsonify({
			"id": user.id, 
			"name": user.name,
			"email": user.email,
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
			"email": user.email
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

	@app.route("/api/calendar/list-events")
	@auth.require_user
	def list_events():
		ensure_user()

		events = query_all_of(CalendarEvent)

		return jsonify([event.id for event in events])

	@app.route("/api/calendar/get-aggregated-event-info")
	@auth.require_user
	def list_event_objects():
		ensure_user()

		events = query_all_of(CalendarEvent)

		return jsonify([{
			"id": event.id,
			"title": event.title,
			"description": event.description,
			"startTime": event.start_datetime,
			"endTime": event.end_datetime	
		} for event in events])

	@app.route("/api/calendar/get-event")
	@auth.require_user
	def get_event():
		ensure_user()

		event = query_by_id(CalendarEvent, request.args.get("id"))

		if not event: return Response(status=400)

		return jsonify({
			"id": event.id,
			"title": event.title,
			"description": event.description,
			"startTime": event.start_datetime,
			"endTime": event.end_datetime	
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