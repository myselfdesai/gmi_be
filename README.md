## gmi_be
Its a application for data processing

## Features
- Enable user to upload both input files
- Parse input files and save data to DB
- Display data
- Simple Search

## Version
python 3.6
linters: Flake 8


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

## How to Use

To use this project, follow these steps:
1. Create your working environment.
2. Install requirements (`$ pip install -r requirements.txt`)
3. Run application (` python run.py `)
4. Go To browser (` http://localhost:5000/ `)
