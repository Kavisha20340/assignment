import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("my_auth/assignment-e7f3a-firebase-adminsdk-dx1d3-da1a4a10f0.json")

firebase_admin.initialize_app(cred)
