# Library 
This project is a library system written in flask python module, which is connected to a postgresql database.
The main goal of this project was to create simple system that allows to manage a library. 
 
 # Instalation
 Check the file `requirements.txt` and follow it.
 Next step is to create local postgresql database (check `librarydb/__init__.py` file for database config i.e. password, database name, address and username). Then you should load database files (`db_files/my_create.sql`, `db_files/my_insert.sql`, `db_files/my_views.sql`).

# Run
To start the application you have to start web server by typing `python run.py` in your cmd. It should run localhost server at port `5000`. 
Next you should type in your browser `localhost:5000`.

![](https://github.com/Infam852/library_db/blob/dawid/librarydb/static/admin_panel.PNG)
*admin panel - user account management*

![](https://github.com/Infam852/library_db/blob/dawid/librarydb/static/book_admin.PNG)
*admin panel - book information*

# Features
* registration/login system
* book reservation
* borrowing books
* penalties
* comments
* different privileges for admin and library user
* simple search engine

# Authors
* Kutyba Piotr
* Jakóbczak Dawid
