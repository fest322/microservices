from flask import Flask, request, jsonify
from database import DataBase

db = Flask(__name__)


@db.route('/', methods=['POST'])
def insert():
    if request:
        data = request.json
        connection = DataBase().connect()
        connection.insert_request(data['data'])
        connection.close()
        return jsonify(({'task': 'send'}), 200)


@db.route('/get_status_url')
def get_status_url():
    if request:
        url = request.args.get('url', False)
        if url:
            query = "Select url, status, message from request_url " \
                    f"where url = '{url}' order by id_request desc limit 1"
            conn = DataBase().connect()
            url_request = conn.fetchone(query)
            conn.close()
            return jsonify({'data': url_request})
        else:
            return jsonify({'data': None})
    return jsonify({'data': None})

3
if __name__ == '__main__':
    db.run(host='0.0.0.0', port='5003', debug=True)
