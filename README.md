# Summer 2020 Internships - Engineering Pre-assignment Niklas Kuusisto

## About
Language: Python3
Framework: Flask
Requirements : pip and python 3.5 or newer (tested on 3.7.4)
External dependencies:
```
- Flask
- haversine
- pytest (for unit tests)
```
## Setup Instructions

Extract zip file
Navigate into wolt_backend_task:
```bash
$ cd Wolt-Backend-Task
```
Create virutalenv:
```bash
$ python3 -m venv venv
```
On Windows:
```bash
$ py -m venv venv
```
Activate virtualenv:
```bash
$ . venv/bin/activate
```
On Windows:
```bash
$ venv\Scripts\activate
```
_Shell prompt should change to the name of the activated environment_

Install dependencies:
```bash
$ pip install Flask, haversine, pytest
```
Run tests with:
```bash
$ pytest -v
```
Run API on development server with:
```bash
$ python3 api.py
```
On Windows:
```bash
$ py api.py
```
The API is now running on http://127.0.0.1:5000/
Test on a browser or on Postman with: http://127.0.0.1:5000/restaurants/search?q=a&lat=60.17045&lon=24.93147



