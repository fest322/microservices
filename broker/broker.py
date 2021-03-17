import requests
from flask import Flask, request, jsonify

broker = Flask(__name__)


@broker.route('/', methods=['POST'])
def message():
    message = 'Success'
    code = None
    if request:
        try:
            r = requests.post(worker_url, json={'url': request.json['url']})
            code = r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            code = 404
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            code = 500
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            code = 504
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps Error:", err)
            message = 'OOps Error'
        finally:
            return jsonify(({'message': message}), code)
    return jsonify(({'message': message}), code)



if __name__ == '__main__':
    worker_url = 'http://0.0.0.0:5004'
    broker.run(host='0.0.0.0', port='5001')
