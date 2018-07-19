# todo-restful-api-falcon
Simple TODO RESTful API on Falcon framework.

| HTTP Method | URI                                  | Action                  |
| ------- | ---------------------------------------- | ----------------------- |
| GET     | http://[hostname]/api/v0.1/task          | Retrieve list of tasks  |
| GET     | http://[hostname]/api/v0.1/task/[task_id]| Retrieve a task         |
| POST    | http://[hostname]/api/v0.1/task          | Create a new task       |
| PUT     | http://[hostname]/api/v0.1/task/[task_id]| Update an existing task |
| DELETE  | http://[hostname]/api/v0.1/task/[task_id]| Delete a task           |
| POST    | http://[hostname]/api/v0.1/auth          | Create account          |

The task has the following fields: 
+ **id:** unique identifier for tasks. [ObjectId](https://docs.mongodb.com/manual/reference/method/ObjectId/) type.
+ **owner:** author of tasks. ReferenceField(User object).
+ **title:** short task description. StringField.
+ **body:** long task description. StringField.
+ **timestamp:** date of creation. ComplexDateTimeField.
+ **done:** task completion state. BooleanField.
+ **tags:** tags to which the task belongs. ListField(StringField).

The user has the following fields:
+ **username:** user login. StringField.
+ **email:** user email. EmailField.
+ **first_name:** user first name StringField.
+ **last_name:** user last name. StringField.
+ **password_hash:** user password. StringField.

## Quickstart
First you must install MongoDB and set up settings.py.
Install pipenv and config virtualenv
~~~bash
$ pip install pipenv
$ pipenv install
$ pipenv shell
~~~
~~~bash
(todo-restful-api-falcon)$ python server.py
~~~
**Registrate:**
~~~bash
$ curl -d '{
	"username": "User",
	"email": "example@mail.com",
	"password": "good pass"
}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/v0.1/auth
~~~
**Response:**
~~~
{"msg": "OK", "description": "User 'User' created!"}
~~~

**Create new task:**
~~~bash
$ curl -u 'User':'good pass' -d '{
    "title": "Buy products",
    "body": "buy bread, milk and asparagus.",
    "tags": [
            "Shopping"
    ]
}' -H "Content-Type: application/json" -X POST http://localhost:8000/api/v0.1/task
~~~
**Response:**
~~~
{
   "error":false,
   "msg":"Task created!",
   "data":{
      "task":[
         {
            "id":"5b5068a08124f432fef08ed0",
            "owner":"User",
            "title":"Buy products",
            "body":"buy bread, milk and asparagus.",
            "timestamp":"2018-07-19 13:32:00.372132",
            "done":"False",
            "tags":[
               "Shopping"
            ]
         }
      ]
   }
}
~~~
**Get all task:**
~~~bash
$ curl -u 'User':'good pass' -X GET http://localhost:8000/api/v0.1/task
~~~
**Response:**
~~~
{
   "data":{
      "tasks":[
         {
            "id":"5b5068a08124f432fef08ed0",
            "owner":"User",
            "title":"Buy products",
            "body":"buy bread, milk and asparagus.",
            "timestamp":"2018-07-19 13:32:00.372132",
            "done":"False",
            "tags":[
               "Shopping"
            ]
         }
      ],
      "total":1
   },
   "error":false,
   "msg":"Task(s) successfully retrieved."
}
~~~
**Update task:**
~~~bash
curl -u 'User':'good pass' -d '{
    "title": "Buy products",
    "body": "buy bread, milk and asparagus and juice.",
    "tags": [
            "Shopping"
    ]
}' -H "Content-Type: application/json" -X PUT http://localhost:8000/api/v0.1/task/5b5068a08124f432fef08ed0
~~~
**Response:**
~~~
{
   "data":{
      "task":[
         {
            "id":"5b5068a08124f432fef08ed0",
            "owner":"User",
            "title":"Buy products",
            "body":"buy bread, milk and asparagus and juice.",
            "timestamp":"2018-07-19 13:32:00.372132",
            "done":"False",
            "tags":[
               "Shopping"
            ]
         }
      ]
   },
   "error":false,
   "msg":"Task updated!"
}
~~~
**Delete task:**
~~~bash
curl -u 'User':'good pass' -X DELETE http://localhost:8000/api/v0.1/task/5b5068a08124f432fef08ed0
~~~
**Response:**
~~~
{
   "data":{
      "task":[
         {
            "id":"5b5068a08124f432fef08ed0",
            "owner":"User",
            "title":"Buy products",
            "body":"buy bread, milk and asparagus and juice.",
            "timestamp":"2018-07-19 13:32:00.372132",
            "done":"False",
            "tags":[
               "Shopping"
            ]
         }
      ]
   },
   "error":false,
   "msg":"Task deleted!"
}
~~~