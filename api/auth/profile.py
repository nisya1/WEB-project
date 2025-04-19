from flask import jsonify, session, make_response
from flask_restful import Resource, abort

from data.db_session import global_init, create_session
from data.users_models.users import Users


class UserProfileApi(Resource):
    def get(self, user_name: str):
        if 'name' not in session.keys():
            return make_response(jsonify({'error': 'Access denied'}), 403)
        if user_name != session['name']:
            return make_response(jsonify({'error': 'Access denied'}), 403)

        global_init(f"database/users.db")
        sess1 = create_session()
        user = sess1.query(Users).filter(Users.Name == user_name).first()
        tickets = tuple(map(lambda x: x.split(':'), user.Tickets.split(';')))
        output = {}
        for ticket in tickets:
            if ticket[0] != '':
                output[ticket[0]] = ticket[1].split(',')

        return jsonify({"tickets": output})
