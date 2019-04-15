Our Django supported web app!
To deploy locally –

```
$ cd website/
```

Create and enter virtual environment

```
$ python3 -m venv env
$ . env/bin/activate
```

Install necessary dependencies
```
pip3 install django
pip install --upgrade pip # pip will probably be out of date, so upgrade it
env LDFLAGS="-I/usr/local/opt/openssl/include -L/usr/local/opt/openssl/lib" pip3 install mysqlclient
```

Run server, default port is 8000
```
python3 manage.py runserver <optional port number>
```

Quit the server whenever with ^C (CONTROL - C)

To close the virtual environment:

```
$ deactivate
```
