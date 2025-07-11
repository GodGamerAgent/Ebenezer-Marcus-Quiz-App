import os
from firebase_admin import credentials, db, initialize_app, get_app, _apps

auth_path = os.path.join(os.getcwd(), "serviceAccountKey.json")

def firebase_ini():
    if not _apps:  # <- prevents re-initializing if already initialized
        cred = credentials.Certificate(auth_path)
        initialize_app(cred, {
            "databaseURL": "https://ebenezermarcustestuserdetail-default-rtdb.asia-southeast1.firebasedatabase.app/"
        })

def get_ref(path):
    firebase_ini()
    return db.reference(path)
