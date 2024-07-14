#!/usr/bin/python3
""" Check response
"""


if __name__ == "__main__":
    try:
        from models.user_session import UserSession

        user_id = "User10"
        session_id = "The User 10 session ID"

        user_session = UserSession()
        user_session.user_id = user_id
        user_session.session_id = session_id
        user_session.save()

        from api.v1.auth.session_db_auth import SessionDBAuth

        user_id_r = SessionDBAuth().user_id_for_session_id(session_id)
        print("==>", user_id_r)
        if user_id_r is None:
            print("user_id_for_session_id should return the User ID linked to the Session ID")
            exit(1)
        if user_id_r != user_id:
            print("user_id_for_session_id should return the User ID linked to the Session ID")
            exit(1)

        print("OK", end="")
    except:
        import sys
        print("Error: {}".format(sys.exc_info()))
