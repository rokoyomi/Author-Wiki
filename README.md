# Author's Wiki
Database project - A simple online too for storytellers to store their ideas and bring them together them to create stories and worlds.
## Setup
### 1. Clone this Repository
```bash
git clone https://www.github.com/rokoyomi/author-wiki
```
### 1. Install Dependencies
Navigate to the project directory in your terminal and run the following command to install the required dependencies:
```
pip install -r requirements.txt
```
I'd recommend you do this in a virtual environment
```bash
python3 -m venv venv
source venv\bin\activate
pip install -r requirements.txt
```
### 2. Database Configuration
Create a file named `config.ini` and fill in your MySQL details.
```
[MYSQL]
USER = your_database_user
PASSWORD = your_database_password
HOST = localhost
DB = author_wiki
```
Run the two provided scripts to initialize the database
```
mysql -u <user> -p<password> schema.sql
mysql -u <user> -p<password> default_values.sql
```
**Notes:**
- Make sure that your user has permissions to create databases.
- If you use a different database name in config.ini, you need to edit the database name inside the provided scripts as well.
### 3. Run the Application
Execute the following command to run the Flask application:
```
flask run
```
The application will be accessible at `http://localhost:5000` by default.
