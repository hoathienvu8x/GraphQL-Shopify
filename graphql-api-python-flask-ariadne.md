# Build a GraphQL API with Python, Flask and Ariadne

![](https://twilio-cms-prod.s3.amazonaws.com/images/rjipQpwVK-XoL67Elc4HtOuuCX5bSvfiarVvQawxFB4kiJ.width-808.png)

You have probably come across the term [GraphQL](https://graphql.org/) but do you know what is it? Rest easy (pun not intended), as you will learn about it shortly.

GraphQL is a query language for APIs and a server-side runtime that allows clients to request only the data that they need from APIs. GraphQL is meant to be a more efficient and flexible alternative to [REST](https://en.wikipedia.org/wiki/Representational_state_transfer).

GraphQL was developed and used internally at Facebook and was open-sourced in 2015. It has since gained popularity with more and more developers and companies jumping on the GraphQL bandwagon, building supporting tools and GraphQL APIs. One of the most popular is the [Github GraphQL API](https://docs.github.com/en/free-pro-team@latest/graphql). GraphQL is language agnostic which means that we can build GraphQL APIs in Python, JavaScript, Java, Scala and many more programming languages.

### GraphQL vs. REST

With REST, we model our API as resources, provide endpoints to access particular resources and define which HTTP methods are allowed on a given endpoint.

With GraphQL, we model our API as a [graph](https://www.educative.io/edpresso/what-is-a-graph-data-structure), with the types defined in the schema being the nodes. Our clients then make queries to a single endpoint to get data at the particular “nodes”.

For example, a `Todo` REST API would expose an endpoint like /api/todos/<id> where `id` is the id of the `Todo` item on the database. The endpoint would support the methods `GET`, `PUT`, `DELETE` and `PATCH` to allow fetching and manipulating an item. We would also have another endpoint for fetching all the items and creating new ones, maybe /api/todos.

A `Todo` GraphQL API, on the other hand, would expose an endpoint like /api/graphql and clients would send different queries to that endpoint to get what they want. A query to fetch all todos would look like this:

```
query {
  todos {
    id
    description
    completed
    dueDate
  }
}
```

A query to fetch a single todo with an id of 2 would look like:

```
query {
  todo(todoId: "2") {
    id
    description
    completed
    dueDate
  }
}
```

The query above tells the server to return the `id`, `description`, `completed`, and `dueDate` fields of a `Todo` item with `id` of 2. If the client was only interested in the `id` and `description`, the query would say so as follows:

```
query {
  todo(todoId: "2") {
    id
    description
  }
}
```

See how much flexibility the client has in requesting only the data that it needs?

If you have been curious about GraphQL but haven’t yet got your hands dirty building a GraphQL server in Python yet, worry not. By the end of this tutorial, you will have a [GraphQL](https://graphql.org/) API using [Flask](https://flask.palletsprojects.com/) and [Ariadne](https://ariadnegraphql.org/). Our API will help us manage todo lists and it will be capable of the following:

- Create new items
- List all items
- Mark an item as done
- Change the due date of an item
- Delete an item

You can find the complete code for the tutorial [here](https://github.com/alexkiura/todo-api-graphql).

### Requirements

The only requirement you need to complete this tutorial is Python 3.6 or higher. If you don’t have it installed, get it [here](https://www.python.org/downloads/).

### Create a Python virtual environment

We will install several Python packages for our project. A virtual environment will come in handy as it will give us an isolated Python environment for our project. Let’s go ahead and create one.

Create a directory called `todo_api` and navigate to it.

```
mkdir todo_api
cd todo_api
```

Create the virtual environment:

```
python3 -m venv todo_api_env
```

If you are using a Mac or Unix computer, activate the virtual environment as follows:

```
source todo_api_env/bin/activate
```

To activate the virtual environment on Windows, use the following command:

```
todo_api_env\Scripts\activate.bat
```

We will now install the packages below:

- [Flask](https://flask.palletsprojects.com/en/1.1.x/): A simple framework for building web servers in Python
- [Ariadne](https://ariadnegraphql.org/): A library for using GraphQL applications
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/): An extension for Flask that makes it easier to use SQLAlchemy (an ORM) within a Flask application. SQLAlchemy allows us to interact with SQL databases using Python.

Let’s go ahead and install them:

```
pip install flask ariadne flask-sqlalchemy
```

### Introduction to GraphQL

GraphQL is a query language for APIs and a server-side runtime that allows clients to request only the data that they need. We build a GraphQL service by: defining the types of data and operations allowed on that data (schema) and functions for the fields on the data types.

GraphQL has its own language, the GraphQL Schema Definition Language (SDL), which is used to write GraphQL schemas.

We can define a `Todo` type using the SDL as follows:

```
type Todo {
    id: ID!
    description: String!
    completed: Boolean!
    dueDate: String!
}
```

The `!` after a type indicates that the field is non-nullable, or in other words, that it must always have a value.

### Fetching data

When working with REST, we usually fetch data by making HTTP GET requests to various endpoints. GraphQL works a little differently. We have a single endpoint, from where the client can request all the data that it needs. The client does this by posting a query.

A query to get all the `Todo` items can look as follows:

```
type Query {
    todos: [Todo]!
}
```

### Creating and modifying data

Most applications also need a way to modify data. We create, update and delete data in GraphQL using mutations. We write mutations similar to how we write queries but we use the keyword `mutation`. A mutation for creating a `Todo` would look as follows:

```
type Mutation {
    createTodo(description: String!, dueDate: String!): Todo!
}
```

This mutation accepts two strings: a description and a due date and returns a Todo object.

Learn more about queries and mutations [here](https://graphql.org/learn/queries/).

### Writing our GraphQL schema

Now that we are more familiar with the GraphQL SDL, let’s write the schema for our “ToDo” application. Inside the todo_api directory, create a new file called schema.graphql and add the following schema to it:

```
schema {
    query: Query
    mutation: Mutation
}

type Todo {
    id: ID!
    description: String!
    completed: Boolean!
    dueDate: String!
}

type TodoResult {
    success: Boolean!
    errors: [String]
    todo: Todo
}

type TodosResult {
    success: Boolean!
    errors: [String]
    todos: [Todo]
}

type Query {
    todos: TodosResult!
    todo(todoId: ID!): TodoResult!
}

type DeleteTodoResult {
    success: Boolean!
    errors: [String]
}

type Mutation {
    createTodo(description: String!, dueDate: String!): TodoResult!
    deleteTodo(todoId: ID!): DeleteTodoResult!
    markDone(todoId: String!): TodoResult!
    updateDueDate(todoId: String, newDate: String!): TodoResult!
}
```

We defined a few things in our schema:

1. A Todo type to represent an item in our to-do list
2. Queries to fetch a single and all items
3. Mutations to create and delete Todo items, mark an item as done and update its due date.
4. The return values of the queries and mutations include the corresponding data items plus two extra fields: success and errors. These fields will tell the client whether a query or mutation executed successfully and provide error messages when there was a failure.

### Choosing a Python library to implement a GraphQL server

We will build our API using [Ariadne](https://ariadnegraphql.org/), which is a popular Python library for building GraphQL servers. Ariadne is a schema-first library, which means that the schema written in the SDL is the ultimate source of truth.

This is unlike a code-first approach, where code is the source of truth and the schema is derived from it. Both approaches have their pros and cons and you can read more about the differences [here](https://blog.logrocket.com/code-first-vs-schema-first-development-graphql/#:~:text=Schema%2Dfirst%20indicates%20that%20we,represent%20the%20GraphQL%20data%20model.). [Graphene](https://graphene-python.org/) is another popular GraphQL library for Python that uses the code-first approach.

### Creating a Flask project

Now that we have already defined our schema, let’s implement it and put together our GraphQL API.

The code for our api will live inside a package called api. Inside todo_api, create a directory called api and inside it create a file called __init__.py. Add the code below to api/__init__.py to create a simple Flask server that returns the word `Hello!`:

```
from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello!'
```

In the project root, create another file called main.py and update it as follows:

```
from api import app, db
```

The directory structure should look as follows:

```
todo_api
├── api
│     └── __init__.py
├── main.py
├── schema.graphql
└── todo_api_env
```

Now we need to tell Flask where to find the `app` application instance. We do that by setting the environment variable `FLASK_APP` to the name of the top-level Python file that has the app, which in our case is main.py. Set it as follows:

```
export FLASK_APP=main.py
```

If you are using Windows, replace `export` in the command above with `set`.

Start the Flask server by running the following command:

```
flask run
```

Visit http://127.0.0.1:5000 in your web browser to confirm that the server is running and that everything is working correctly.

![](https://twilio-cms-prod.s3.amazonaws.com/images/xBmVTwuCqWhoc_Z5EXzF3NxNoyL7MHGDpYYX6-XxKTH7vl.width-500.png)

### Adding the database

Since we want to be able to view our to-do items any time we want, we will store them in a database so that they can be preserved. We will go with [sqlite](https://www.sqlite.org/index.html) because it’s lightweight and is simple enough to get started with. To manage this database from the Flask application we are going to use the [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/) extension.

Let’s go ahead and configure our database. Add the configuration to the api/__init__.py file:

```
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


@app.route('/')
def hello():
    return 'Hello!'
```

The `SQLALCHEMY_DATABASE_URI` setting tells Flask-SQLAlchemy where the database file is located. In our case, we will store it in the project directory with the name todo.db.

Setting `SQLALCHEMY_TRACK_MODIFICATIONS` to `False` disables tracking modifications of objects and sending signals to the application for every database change. It is a useful feature but can cause memory overhead, so it should only be used when necessary.

### Creating the Model

Our database will have one table, called `Todo`, where we will store our to-do items. SQLAlchemy makes it possible to create database tables by defining them as Python classes, with columns given as class variables. Awesome, right? We call them database models. Let’s define our `Todo` model.

Create a new file called models.py inside the api package and define the `Todo` model as shown below:

```
from main import db


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date)

    def to_dict(self):
        return {
            "id": self.id,
            "completed": self.completed,
            "description": self.description,
            "due_date": str(self.due_date.strftime('%d-%m-%Y'))
        }
```

Our `Todo` table will have columns called `id`, `description`, `completed` and `due_date`. The `id` column will be auto-generated. The `description` column will accept strings. The `completed` column will store a boolean and will default to `False`. The `due_date` column will store dates. We also added a nifty method called `to_dict` which will provide a dictionary representation of a `Todo` item. This will come in handy when we start writing mutations and queries.

The models file needs to be imported into the application. Edit your main.py file so that it looks as follows:

```
from api import app, db
from api import models
```

### Create some Todos

Fire up the terminal and start the python prompt by running the Python interpreter:

```
python
```

Create the database table as follows:

```
>>> from main import db
>>> db.create_all()
>>>
```

Next, create your first to-do item and save it to the database:

```
>>> from datetime import datetime
>>> from api.models import Todo
>>> today = datetime.today().date()
>>> todo = Todo(description="Run a marathon", due_date=today, completed=False)
>>> todo.to_dict()
{'id': None, 'completed': False, 'description': 'Run a marathon', 'due_date': '2020-10-22'}
>>> db.session.add(todo)
>>> db.session.commit()
>>>
```

### Queries and Mutations

After creating a GraphQL schema, we need to create functions (resolvers) that return values for the different fields defined in it. Inside api, create two files called queries.py and mutations.py.

### Writing the `todos` query

We defined a query called todos in our GraphQL schema:

```
type Query {
    todos: TodosResult!
    ...
}
```

This query returns a dictionary with the keys `success`, `errors` and `todos`. The `success` field is set to `True` if there are no errors. In the case of a problem, `success` is set to `False` and `errors` includes the list of errors that occurred during execution. The `todos` field contains the list of `Todo` items. As mentioned above, the `!` means that this query is non-nullable, so it must always return a result.

Let us write a resolver to fetch all the `Todo` items. Add the following to api/queries.py:

```
from .models import Todo


def resolve_todos(obj, info):
    try:
        todos = [todo.to_dict() for todo in Todo.query.all()]
        payload = {
            "success": True,
            "todos": todos
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload
```

A resolver function accepts two positional arguments, `obj` and `info`. `obj` is a value returned by a parent resolver, which in this case will be the root resolver. `info` contains any context information that the GraphQL server provided the resolver during execution. This data can include authentication information or an HTTP request.

Inside the resolver, we query the `Todo` table for all the items, convert them to Python dictionaries and add them to the response payload with the key `todos`. If there are any errors during execution, we return them in the key `errors` inside the response payload and also set `success` to False.

### Binding a resolver

Once we write a resolver, we need to tell Ariadne which field it corresponds to from the schema, so we need to bind the `resolve_todos` function to the field `todos` in our GraphQL schema.

Add the following at the bottom of main.py:

```
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.queries import resolve_todos

query = ObjectType("Query")

query.set_field("todos", resolve_todos)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, snake_case_fallback_resolvers
)
```

Don’t worry about the imports for now, we will get to them shortly.

We have imported `ObjectType`, which is initialized with the name of the type defined in the Schema. In our case, we have initialized `ObjectType` with `Query` since we are binding our resolver to a `Query` type. The `set_field` method binds the `todos` field of the query to our resolver function.

The `load_schema_from_path` function takes the name of a schema file. This function validates the schema and returns a string representation of it.

The `make_executable_schema` function takes the `type_defs` variable with the string representation of our schema and the `query` resolver we just created.

The `snake_case_fallback_resolvers` comes in handy because of the differences in how we write Python code and JavaScript code. In Python, we normally name variables and functions in “snake_case”, while “camelCase” is preferred in JavaScript. Most GraphQL schemas you come across will use the JavaScript convention to name the fields (including the one we wrote). `snake_case_fallback_resolvers` converts a field name to snake case before looking it up on the returned object.

### Exploring our API

Ariadne ships with [GraphQL Playground](https://github.com/graphql/graphql-playground), which is a graphical user interface that we can run to test our queries interactively. Let’s set that up so that we can begin testing our queries.

Add the following routes at the bottom of main.py:

```
@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
```

Start the Flask server with:

Visit [127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql) and if everything is setup correctly, you should see the page below:

![](https://twilio-cms-prod.s3.amazonaws.com/images/fOiJV6dW7f76dzOBupsng5VdjirYhPZf2h4Lo-ADmqwyl5.width-500.png)

Let’s write our first query. Paste the query below in the editor on the left side of the page:

```
query fetchAllTodos {
  todos {
    success
    errors
    todos {
      description
      completed
      id
    }
  }
}
```

We have named our query `fetchAllTodos` and requested for the fields `id`, `completed`, `dueDate` and `description` from the query `todos`.

Hit the play button to the right of the editor and you should see the list of todos. If successful, you should see your results on the right similar to this:

![](https://twilio-cms-prod.s3.amazonaws.com/images/Synb0ELryHr17bHawk45FGTp6aGtDFx1y3hIv2mA2-F2Ki.width-500.png)

### Fetching a single item

To fetch a single `Todo` item, we will need to write a special kind of resolver; one that takes arguments.

Here is a sample query that fetches the item with id of 1:

```
query fetchTodo {
  todo(todoId: "1") {
    success
    errors
    todo { id completed description dueDate }
  }
}
```

Paste it on the GraphQL Playground and see how when we execute it we get an obscure response that includes some error messages, among them one that reads “Cannot return null for non-nullable field Query.todo.” This happens because we haven’t written a resolver to resolve the `todo` field of the schema. The response to this query would be `null`, but because we have used the `!` to mark this query as non-nullable, Ariadne returns an error.

Let’s update api/queries.py to add our second resolver:

```
from ariadne import convert_kwargs_to_snake_case

...

@convert_kwargs_to_snake_case
def resolve_todo(obj, info, todo_id):
    try:
        todo = Todo.query.get(todo_id)
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }

    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo item matching id {todo_id} not found"]
        }

    return payload
```

Next add the code to bind the resolver to main.py:

```
from api.queries import resolve_todos, resolve_todo

...

query.set_field("todo", resolve_todo)
```

Now restart the Flask server and then run the query above once again and you should get back the `Todo` item matching the given `id`.

Note that we decorated our resolver with `convert_kwargs_to_snake_case`. This is because the argument is passed in as `todoId` on the query, but the corresponding argument on the resolver is named `todo_id`. We could define our resolver as `def resolve_todo(obj, info, todoId)`, but to avoid having to mix snake case and camel case we use the `convert_kwargs_to_snake_case` decorator to convert the incoming arguments to snake case.

The implementation of the resolver queries the `Todo` table for the `Todo` item with the given id and adds it to the response using the key `todo` and the key `success` is set to `True`. If there are any errors during execution, they are included in the `errors` key on the response payload and the key `success` on the response is set to `False`.

### Mutations

We write a mutation resolver in a similar way to how we have written the query resolvers above. The mutation resolver function takes in the `obj` and `info` arguments and any other arguments that are defined in the schema.

Let’s write our first mutation. As defined in the schema, our `createTodo` mutation takes two arguments: `description` and `dueDate`. Add the code below to api/mutations.py:

```
from datetime import datetime

from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Todo


@convert_kwargs_to_snake_case
def resolve_create_todo(obj, info, description, due_date):
    try:
        due_date = datetime.strptime(due_date, '%d-%m-%Y').date()
        todo = Todo(
            description=description, due_date=due_date
        )
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": [f"Incorrect date format provided. Date should be in "
                       f"the format dd-mm-yyyy"]
        }

    return payload
```

First, we decorate our resolver to convert the incoming arguments to snake case. The `due_date` argument is going to be passed as a string with the format `dd-mm-yyyy`, so we convert it to a date object using the `striptime` function.

We finally create a `Todo` object with the arguments given and persist it to the database. If there was an error parsing the date string, the `striptime` function throws a ValueError and we return an error message prompting the user to provide a date in the format `dd-mm-yyyy`.

Let’s bind the mutation resolver. To do this we need to update main.py. To help you make these changes correctly, below you can see the first few lines of this file modified to include the mutation. Keep the two Flask routes after these lines.

```
from api import app, db
from api import models
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify
from api.queries import resolve_todos, resolve_todo
from api.mutations import resolve_create_todo

query = ObjectType("Query")

query.set_field("todos", resolve_todos)
query.set_field("todo", resolve_todo)

mutation = ObjectType("Mutation")
mutation.set_field("createTodo", resolve_create_todo)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)
```

Restart the Flask server and then try the following mutation in the playground:

```
mutation newTodo {
  createTodo(description:"Go to the dentist", dueDate:"24-10-2020") {
    success
    errors
    todo {
      id
      completed
      description
    }
  }
}
```

The server should return the result below:

```
{
  "data": {
    "createTodo": {
      "errors": null,
      "success": true,
      "todo": {
        "completed": false,
        "description": "Go to the dentist",
        "id": "2"
      }
    }
  }
}
```

Let’s now add a resolver for the `markDone` mutation. Add the code below to api/mutations.py:

```
@convert_kwargs_to_snake_case
def resolve_mark_done(obj, info, todo_id):
    try:
        todo = Todo.query.get(todo_id)
        todo.completed = True
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors":  [f"Todo matching id {todo_id} was not found"]
        }

    return payload
```

Here we accept a `todo_id` argument which we use to query for the particular `Todo` item, and then set its `completed` field to `True`.

To make the mutation available on the GraphQL server, let’s bind it as follows in main.py:

```
from api.mutations import resolve_create_todo, resolve_mark_done

...

mutation.set_field("markDone", resolve_mark_done)
```

To test it, send a mutation to the server such as this one:

```
mutation markDone {
  markDone(todoId: "1") {
    success
    errors
    todo { id completed description dueDate }
  }
}
```

![](https://twilio-cms-prod.s3.amazonaws.com/images/Z8v-apdKp2KP3njdvXcYZSY1YJbmGMlInlb8AQ28sAFyA6.width-500.png)

Next we want to be able to delete items from the database. Go ahead and add one more mutation to api/mutations.py:

```
@convert_kwargs_to_snake_case
def resolve_delete_todo(obj, info, todo_id):
    try:
        todo = Todo.query.get(todo_id)
        db.session.delete(todo)
        db.session.commit()
        payload = {"success": True}

    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }

    return payload
```

This resolver function accepts a `todo_id`, queries the database for our `Todo` item and then deletes it if it exists. This one returns a `success` value with the type boolean, denoting whether the requested `Todo` was deleted or not and an `errors` value which is a list of any errors that happened during execution.

Let’s go ahead and bind our resolver as follows in main.py:

```
from api.mutations import resolve_create_todo, resolve_mark_done, \
    resolve_delete_todo

...

mutation.set_field("deleteTodo", resolve_delete_todo)
```

To test it, send a mutation like the following to the server:

```
mutation {
  deleteTodo(todoId: "1") {
    success
    errors
  }
}
```

![](https://twilio-cms-prod.s3.amazonaws.com/images/5jGp2wy2eGF5KCA7O4PEB3E6cy0g41xCiw-vd4CNU4l3Hp.width-500.png)

It’s possible our users will want to change the due date of an item. We will do that through the last of our mutations, which is called `updateDueDate`. Let’s add a resolver for this mutation in api/mutations.py:

```
@convert_kwargs_to_snake_case
def resolve_update_due_date(obj, info, todo_id, new_date):
    try:
        todo = Todo.query.get(todo_id)
        if todo:
            todo.due_date = datetime.strptime(new_date, '%d-%m-%Y').date()
        db.session.add(todo)
        db.session.commit()
        payload = {
            "success": True,
            "todo": todo.to_dict()
        }

    except ValueError:  # date format errors
        payload = {
            "success": False,
            "errors": ["Incorrect date format provided. Date should be in "
                       "the format dd-mm-yyyy"]
        }
    except AttributeError:  # todo not found
        payload = {
            "success": False,
            "errors": [f"Todo matching id {todo_id} not found"]
        }
    return payload
```

This mutation takes two arguments, `todoId` and `newDate`, which are passed on to our resolver as `todo_id` and `new_date` respectively after they are converted to snake case.


The `new_date` argument is a string in the format `dd-mm-yyyy`. As we did before, the string is converted to a `datetime.date` object which is set as the `due_date` field on the `Todo` object with the requested `id`. If the requested `Todo` item was not found or there was an error parsing the date string, we add a descriptive error message and add it to the response under the key `errors`

Like all other resolvers, let’s go ahead and bind it as follows in main.py:

```
from api.mutations import resolve_create_todo, resolve_mark_done, \
    resolve_delete_todo, resolve_update_due_date

...

mutation.set_field("updateDueDate", resolve_update_due_date)
```

Test the mutation on the server with the following example:

```
mutation updateDueDate {
  updateDueDate(todoId: "2", newDate: "25-10-2020") {
    success
    errors
  }
}
```

![](https://twilio-cms-prod.s3.amazonaws.com/images/YckR03FUJ6o060EAk09Cqwj3ix_uOnnJ7twvOTtUz3tfdq.width-500.png)

### Conclusion

Congratulations for completing this tutorial, you have now built a basic GraphQL server using Flask and Ariadne!

We covered queries, mutations, writing a schema and implementing resolvers. GraphQL defines a third operation besides queries and mutations called [subscriptions](https://ariadnegraphql.org/docs/subscriptions.html), which allow a server to send real time updates to subscribed clients each time new data is available, usually via [WebSocket](https://en.wikipedia.org/wiki/WebSocket). Learning GraphQL puts you next to [all these companies](https://graphql.org/users/) who are already using it.

Learn more about GraphQL [best practices here](https://graphql.org/learn/best-practices/).

Alex is a developer and technical writer. He enjoys building web APIs and backend systems. You can reach him at:

- Github: [https://github.com/alexkiura](https://github.com/alexkiura)
- Twitter: [https://twitter.com/mistr_qra](https://twitter.com/mistr_qra)
  
 > https://www.twilio.com/blog/graphql-api-python-flask-ariadne
