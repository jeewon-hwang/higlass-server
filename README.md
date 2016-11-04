# higlass-server

## Installation

1. clone repo
2. `cd higlass-server/api`
3. `pip install --upgrade -r requirements.txt`
4. resolve personal dependency issues that pip can't
5. ensure access to port 8000
6. `mkdir /higlass-server/api/data`
7. `python run_tornado.py` or `python manage.py runserver localhost:8000`
8. `wget https://s3.amazonaws.com/pkerp/public/dixon2012-h1hesc-hindiii-allreps-filtered.1000kb.multires.cool`
9. `mv https://s3.amazonaws.com/pkerp/public/dixon2012-h1hesc-hindiii-allreps-filtered.1000kb.multires.cool data`
10. `wget https://s3.amazonaws.com/pkerp/public/db.sqlite3`

## Usage

Usage:

`python manage.py runserver localhost:8000`

Get a tile:

`curl http://localhost:8000/coolers/12/tiles/?d=0.0.0&d=1.0.0`

