Task Management API
This Flask API provides endpoints for managing tasks and user authentication.

Setup
To set up the project environment:
Make sure you have python and postgreSQL

Create a virtual environment:
py -m venv venv

Activate the virtual environment:
venv\Scripts\activate

Install the required dependencies, including psycopg2 for PostgreSQL database interaction:
pip install -r requirements.txt

Database Setup
To set up the database and create models in PostgreSQL:

Activate the virtual environment if not already activated:
venv\Scripts\activate\

Start the Flask shell:
flask shell

Create the database tables using SQLAlchemy's create_all() method:
db.create_all()


Endpoints
/signup: Register a new user.

Method: POST
Payload: JSON object with name and password fields.
Response:
200 OK if user created successfully.
404 Not Found if user already exists.
500 Internal Server Error if unable to create user.
/signin: User login.

Method: POST
Payload: JSON object with name and password fields.
Response:
200 OK with a JWT token if login successful.
404 Not Found if user does not exist or incorrect credentials.
500 Internal Server Error if login fails.
/tasks: Manage tasks.

Method: GET
Get all tasks.
Requires JWT token in header for authentication.
Method: POST
Create a new task.
Requires JWT token in header for authentication.
Payload should contain title, description, priority, due_date, and category.
Method: PUT, DELETE
Update or delete a task.
Requires JWT token in header for authentication.
Requires task ID in the URL.
Payload should contain updated task details.
/tasksByUser: Get tasks by user ID.

Method: GET
Requires JWT token in header for authentication.
Response: List of tasks belonging to the authenticated user.
/tasksByUser/<id>: Get a specific task by task ID.

Method: GET
Requires JWT token in header for authentication.
Requires task ID in the URL.
Response: Task details.
/tasksByCateg/<code>: Get tasks by category code.

Method: GET, DELETE
Get or delete tasks by category code.
Requires category code in the URL.
GET response: List of tasks with the specified category code.
DELETE response: Message confirming deletion.
Validations
Validation of task data is performed using the TaskValidator class in a separate module.

Dont forget to change this app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:password@localhost:5432/postgres" according to your postgreSQL credentials.
use this so you start your apis on Postman : flask run --port 8000

This section now includes instructions on setting up the project environment,
 installing dependencies, and creating database models in PostgreSQL. 
It also explains the purpose of using psycopg2 library for PostgreSQL database interactions. 
Let me know if you need further clarification or assistance!
