
## Version
python 3.6

linters: Flake 8

## Installation

create envirnoment 
```
python3 -m venv venv 

```
Install with pip:
goto gmi_be directory and install requirement.txt 
```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
├── gmiapp
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── forms.cpython-36.pyc
│   │   ├── models.cpython-36.pyc
│   │   └── routes.cpython-36.pyc
│   ├── forms.py
│   ├── models.py
│   ├── routes.py
│   ├── site.db
│   ├── static
│   │   └── main.css
│   ├── templates
│   │   ├── dashboard.html
│   │   ├── home.html
│   │   └── layout.html
│   └── uploads
│       ├── flexstar-output.csv
│       └── hospital-data-input.xml
├── requirements.txt
└── run.py

```

## How to run the application

```
python run.py
```

open browser and goto 
```
http://localhost:5000/
```