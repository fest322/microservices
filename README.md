<h1>microservices</h1>

Приложения включает в себя такие микросервисы, как app, worker, db_service, reporter, broker. 

<h2>Api микрисервиса app</h2>
<p></p>
/add_task?name=name&url=url&delay=1
<p></p>
Пример:
http://0.0.0.0:5000/add_task?url=http://vk.com&name=1&delay=1
<p></p>
Ответ:
{
  "delay": "1", 
  "message": "Url success added", 
  "name": "1", 
  "url": "http://vk.com"
}
<p></p>
/all_task
<p></p>
Показывает список всех существующих задач
<p></p>
Пример вывода
<p></p>
{
  "tasks": [
    {
      "interval": "1.0 s", 
      "name": "1", 
      "state": "Stop", 
      "url": "http://vk.com"
    }
  ]
}
<p></p>
/run_task?name=name_task
<p></p>
Запусает задачу, если она не в состоянии running
<p></p>
/stop_task?name=name_task
<p></p>
Останавливает задачу
<p></p>

<h2>Api микрисервиса Reporter</h2>
<p></p>
/get_url?url=url
<p></p>
Получает от микросервиса бд последний результат мониторинга ссылки
