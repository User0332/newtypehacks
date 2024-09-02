import os


if os.path.isfile("./instance/SECRET_KEYS"):
	with open("./instance/SECRET_KEYS", 'r') as f:
		APP_SECRET_KEY = f.readline()
		AUTH_URL = f.readline()
		AUTH_API_KEY = f.readline()
else:
	APP_SECRET_KEY = os.getenv("APP_SECRET_KEY")
	AUTH_URL = os.getenv("AUTH_URL")
	AUTH_API_KEY = os.getenv("AUTH_API_KEY")