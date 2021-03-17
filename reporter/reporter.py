import requests
from flask import Flask, request, jsonify
from logger.logger import Logger

reporter = Flask(__name__)
logger = Logger('reporter_logs')


@reporter.route('/get_url')
def message():
    if request:
        code = 200
        error = {}
        url = request.args.get('url')
        if url:
            try:
                r = requests.get(db_url + f'/get_status_url?url={url}')
                code = r.status_code()
            except requests.exceptions.HTTPError as errh:
                code = 404
                error = {"Http Error:": str(errh)}
            except requests.exceptions.ConnectionError as errc:
                code = 500
                error = {"Error Connecting:": str(errc)}
            except requests.exceptions.Timeout as errt:
                code = 504
                error = {"Timeout Error:": str(errt)}
            except requests.exceptions.RequestException as err:
                error = {"OOps Error:": str(err)}
            finally:
                logger.logging(f'Answer db for url {url}: {str(code)}, {r.json()}')
                return jsonify({'code': str(code), 'answer': r.json(), 'error': error})
        else:
            logger.logging(f'{error}')
            return jsonify({'message': 'Empty Url'})


if __name__ == '__main__':

    db_url = 'http://0.0.0.0:5003'
    reporter.run(host='0.0.0.0', port='5002', debug=True)
