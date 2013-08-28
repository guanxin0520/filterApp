filterApp
=========

A simple demo show how the Active SVM works in general text classification usage

About
-----
This web application demo shows how to use Active SVM classifier in general text classification.
The project was motivted by the DHNow Filter project, which help editors find the
vaulable blogs or articles from thousands of feeds. This poject is written in Python,
and it use django framwork to buld the web application demo. You can change the sources databas,
and design the UI. (the UI is pretty simple right now). Please have fun with it. 

Installation notes for developers
---------------------------------
The demo is tested under Ubuntu. This demo is using libSVM, so before run the server, please run 'make' in terminal under the folder

```bash
make
```

Install pip if you don't have it:
easy_install pip (or sudo easy_install pip)

(sudo) pip install -r requirements.txt

Add new python dependencies to requirements.txt as needed.

Run syncdb to do initial database setup:

```bash
python manage.py syncdb
```

To start the local dev server:

```bash
python manage.py runserver
```

Customize it!
-------------------------------
You can change the souces to fit your own usage. Changing the sources needs some programming.
The userdefine.py file include a init_database function. It is the function to generate the 'fixture'
file, which is the initial data when run syncdb.

See more detail in 'userdefine.py' or leave a message.

Acknowledgement
-------------------------------
In this project we use libSVM, nltk API and stop words. Both of them are free and open source library.
Thanks for their excentlent job.

Chih-Chung Chang and Chih-Jen Lin, LIBSVM : a library for support vector machines. ACM Transactions on Intelligent Systems and Technology, 2:27:1--27:27, 2011. Software available at http://www.csie.ntu.edu.tw/~cjlin/libsvm

Bird, Steven, Edward Loper and Ewan Klein (2009). Natural Language Processing with Python. O’Reilly Media Inc.
