import requests
from flask import Flask, request, jsonify, redirect
import asyncio
import validators
from state_task import State
from task import Task
from threading import Thread
import urllib

tasks = []  # Запушенные задачи
app = Flask(__name__)
loop = asyncio.new_event_loop()
"""Микросервис app_main: позволяет добавлять, проверять статус (stopped/running/failed/etc.) 
и останавливать задачи вида (URL, interval)"""
thread = None

async def url_task(url: str, delay: float):
    while True:
        try:
            r = requests.post(broker_url, json={'url': url, 'delay': delay}, proxies=urllib.request.getproxies())
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
        finally:
            await asyncio.sleep(delay)


def start_loop():
    global thread
    thread = Thread(target=loop.run_forever)
    thread.start()


@app.route('/add_task')
def add_task():
    name_task = request.args.get('name')
    url = request.args.get('url')
    delay = request.args.get('delay')
    if url and delay and name_task:
        if [task for task in tasks if task.name == name_task]:
            return jsonify({'message': 'Task already create'})
        else:
            if validators.url(url):
                task = Task(name_task, url, delay, State.Stop.value)
                tasks.append(task)
                return jsonify({'name': name_task,
                                'url': url,
                                'delay': delay,
                                'message': 'Url success added'})
            else:
                return jsonify({'url': url,
                                'message': 'Not valid url'})
    else:
        return jsonify({'message': 'error data'})


@app.route('/all_task')
def all_task():
    return jsonify({'tasks': [{'name': task.name, 'state': task.state, 'url': task.url,
                               'interval': f'{task.interval} s'} for task in tasks]})


@app.route('/run_task')
def run_task():
    global loop
    name_task = request.args.get('name')
    if name_task:
        task = list(filter(lambda task: task.name == name_task, tasks))
        if task:
            task = task[0]
            if task.state == State.Stop.value:
                task_loop = loop.create_task(url_task(task.url, task.interval))
                task.task = task_loop
                task.state = State.Running.value
                if not loop.is_running():
                    start_loop()
        else:
            return jsonify({'error': f'Task with name \'{name_task}\' don\'t exist'})
    return redirect('/all_task')


@app.route('/stop_task')
def stop_task():
    global thread
    name_task = request.args.get('name')
    if name_task:
        task = list(filter(lambda task: task.name == name_task, tasks))
        if task:
            task = task[0]
            task.task.cancel()
            task.task = None
            task.state = State.Stop.value
            if not list(filter(lambda task: task.task != None, tasks)):
                thread
                loop.stop()
            return redirect('/all_task')
        else:
            return jsonify({'error': f'No exist task with name = {name_task}'})
    else:
        return jsonify({'error': 'Empty name'})


if __name__ == '__main__':
    broker_url = "http://localhost:5001/"
    app.run(host='0.0.0.0', port='5000', debug=True)
