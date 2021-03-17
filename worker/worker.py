from flask import Flask, request, jsonify
import requests

worker = Flask(__name__)

"""Микросервис worker: обслуживает задачи сбора (запросить URL с интервалом interval), 
пишет результаты в микросервис db"""


@worker.route('/', methods=['POST'])
def monitor_url():
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0'}
    message = 'Success'
    code = 200
    if request:
        url = request.json['url']
        try:
            r = requests.get(url, headers=headers)
            code = r.status_code()
        except requests.exceptions.HTTPError:
            code = 404
            message = "Http Error"
        except requests.exceptions.ConnectionError:
            code = 500
            message = "Error Connecting"
        except requests.exceptions.Timeout:
            code = 504
            message = "Timeout Error"
        except requests.exceptions.RequestException:
            message = "Error"
        finally:
            data = {'url': url, 'status_code': code, 'message': message}
            db_insert(data)
            return jsonify(({'message': message}), code)
    else:
        return jsonify({'message': 'Empty data'})

def db_insert(data: dict):
    message = 'Success'
    try:
        r = requests.post(url_db, json={'data': data})
        code = r.raise_for_status()
    except requests.exceptions.HTTPError:
        code = 404
        message = "Http Error"
    except requests.exceptions.ConnectionError:
        code = 500
        message = "Error Connecting"
    except requests.exceptions.Timeout:
        code = 504
        message = "Timeout Error"
    except requests.exceptions.RequestException:
        message = "Error"
    finally:
        return jsonify(({'message': message}), code)


if __name__ == '__main__':
    url_db = 'http://0.0.0.0:5003'
    worker.run(host='0.0.0.0', port='5004', debug=True)
