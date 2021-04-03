import firebase_admin
from firebase_admin import auth, credentials, db

default_app = firebase_admin.initialize_app(options={
    'databaseURL': 'https://movementauth-default-rtdb.firebaseio.com/',
})


def get_reference(reference_path: str) -> object:
    """ Returns a reference object for the specified path
    Args:
        reference_path (str):   Path to be used to retrieve reference from
                                real time database.
    Returns:
        object: Returns a real time database Reference object
    """
    return db.reference('/' + reference_path)