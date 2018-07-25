## Welcome to MyDiary app
[![Build Status](https://travis-ci.org/j0flintking02/MyDiary.svg?branch=api)](https://travis-ci.org/j0flintking02/MyDiary) ![GitHub package version](https://img.shields.io/github/package-json/v/badges/shields.svg)   

these are the routes that are available

# Setting Up the Project
Clone the repo
```
git clone https://github.com/j0flintking02/MyDiary.git
``` 
navigate to the project directory
```
cd myDiary
```
set up your virtual environment 
```
virtualenv venv
```
activate the virtual environment
```
. /venv/Scripts/activate.bat
``` 
install all the dependence
```
pip install -r requirements.txt
```
run the application
```
python run.py
```
| End point                                            |   Function          |
|------------------------------------------------------|---------------------|
| '/api/v1/entries', methods=['GET']                   | Return all entries  |
| /api/v1/entries/<int:entry_id> [GET]                 | Return single entry |
| '/api/v1/entries', methods=['POST']                  | add new entry       |
| '/api/v1/entries/<int:entry_id>', methods=['Delete'] | delete entry        |
|'/api/v1/entries/<int:entry_id>', methods=['PUT']     | edit single entry   |
You can use the [index page](https://j0flintking02.github.io/MyDiary/) to  preview the content for your website.