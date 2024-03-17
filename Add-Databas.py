import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# import speechrecognition as sp

# file_name=sp.speech()

cred = credentials.Certificate("ServiceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://number-plate-detection-56492-default-rtdb.asia-southeast1.firebasedatabase.app"
})
ref = db.reference('Cars')
data = {
    "HR26DK8337":
        {
            "name": "Devansh Matha",
            "NumPlate": "HR26DK8337",
            "Credits": 69
        },
    "Deepak":
    {
        "name": "Deepak",
        "NumPlate": "HR26DK8337",
        "Credits": 70
    }
}
for key, value in data.items():
    ref.child(key).update(value)
