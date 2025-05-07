# Install python 3.11
```bash
brew install python@3.11 or install python 3.11 version from official document
```
# Create virtual env
```bash
py -3.11 -m venv venv
```

# run the command
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
# activate the virual env
```bash
.\venv\Scripts\activate
```
# install requirements.txt
```bash
pip3 install -r requirements.txt
```
# make sure you installed the following dependencies
```bash
pip3 install setuptools wheel flask
```
# run the server
```bash
python app.py
```
