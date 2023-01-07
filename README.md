# tentaP Django API

Thank you for visiting our Django API! This API was built using the [Django](https://www.djangoproject.com/). web framework for Python.

## Prerequisites
Before you begin, make sure you have the following software installed on your system:

- [PostgreSQL](https://www.postgresql.org/download/)
- [pgAdmin](https://www.pgadmin.org/download/) (optional, but recommended for managing your database)

### installation of PostgreSQL

- Download and install PostgreSQL from the link above.
- During the installation process, you will be prompted to create a password for the postgres user. Make sure to remember this password, as you will need it later to connect to the database.
- Once the installation is complete, open pgAdmin (if you chose to install it) and connect to the server by double-clicking on the "PostgreSQL" icon in the left pane.
- Enter the password for the postgres user when prompted.
- In the left pane, right-click on "Databases" and select "New Database..."
- Enter a name for the database, and select the owner from the dropdown menu.
- Click "Save" to create the database.

### The secret file (important to run the project!)
In order to use this application, you will need to create a secret.py file in the root directory of the project. In this file, you should include your database credentials, your SECRET_KEY, your Amazon S3 credentials (if you are using S3 for file storage), and your mailtrap.io credentials (if you are using mailtrap.io for testing email functionality).

Here is an example of what the secret.py file might look like:

```
DB_SETTING = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydatabase',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

SECRET_KEY = 'mysecretkey'

AWS_CONFIG = {
    "AWS_S3_ACCESS_KEY_ID": "myaccesskey",
    "AWS_S3_SECRET_ACCESS_KEY": "mysecretaccesskey",
    "AWS_STORAGE_BUCKET_NAME": "mybucket",
    "AWS_QUERYSTRING_AUTH": False,
    "AWS_S3_FILE_OVERWRITE": False
}

mailtrap_setting = {
        "EMAIL_HOST": 'smtp.mailtrap.io',
        "EMAIL_HOST_USER": 'myusername',
        "EMAIL_HOST_PASSWORD": 'mypassword',
        "EMAIL_PORT": '2525',
    }

```

Make sure to replace the placeholder values with your own credentials.

Once you have created the secret.py file and included your credentials, you should be able to run the application and connect to your database, use your SECRET_KEY, access your Amazon S3 bucket, and send emails using mailtrap.io.

## Installation
To run this API locally on your machine, follow these steps:
1. Make sure you have [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) installed on your system.
2. Clone this repository to your local machine: 

```
git clone https://github.com/TentaP/Backend.git
```

3. Navigate to the cloned directory:
```
cd Backend
```
4. Create a virtual environment and activate it:
```
python3 -m venv env
source env/bin/activate
```
5. Install the required dependencies:
```
pip install -r requirements.txt
```
6. Run the Django migrations:
```
python manage.py migrate
```
7. Start the development server:
```
python manage.py runserver
```
This will start the development server at http://localhost:8000/.

## Endpoints
This API has the following endpoints:
- Auth
  - 'api/login' 
  - api/signup'
  - 'api/verifection/<str:email>/<str:hash_>'
  - 'api/set_superuser'
  - 'api/set_admin'
  - 'api/remove_admin'
  - 'api/request_password_reset_token'
  - 'api/reset_password_via_token'
  - 'api/reset_password'
- User
  - 'api/user'
  - 'api/user/uni/<int:pk>'
  - 'api/user/avatar'
  - 'api/user/avatar/<int:pk>'
  - 'api/user/<int:pk>'
  - 'api/user/files'
  - 'api/user/courses'
  - 'api/users'
- UserSearch
  - 'api/user/<int:pk>/files'
- Course/s
   - 'api/courses'
   - 'api/courses/uni/<str:uni>'
   - 'api/course/<int:pk>'
   - 'api/course/<str:course_name>/files'
   - 'api/course/<int:pk>/reviews'
- File
  - 'api/file'
  - 'api/files'
  - 'api/file/<int:pk>'
  - 'api/file/<int:pk>/reviews'
  - 'api/file/<int:pk>/comments' 
- University
  - 'api/uni'
  - 'api/uni/<int:pk>' 
- Review/s
  - 'api/review/course/<int:course_pk>'
  - 'api/review/file/<int:file_pk>'
  - 'api/review/<int:pk>' 
- Comment
  - 'api/comment/<int:pk>'
