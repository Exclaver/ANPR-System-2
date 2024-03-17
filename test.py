import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://number-plate-detection-56492-default-rtdb.asia-southeast1.firebasedatabase.app",

})
ref = db.reference('/Cars')
# print(ref)
new_data = {
    "ABC1234": {
        "name": "John Doe",
        "NumPlate": "ABC1234",
        "Credits": 80
    }
}
ref.update(new_data)
