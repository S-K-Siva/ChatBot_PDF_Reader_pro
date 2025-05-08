## Demo
[![Watch the video](https://t4.ftcdn.net/jpg/01/43/23/83/360_F_143238306_lh0ap42wgot36y44WybfQpvsJB5A1CHc.jpg)](https://drive.google.com/file/d/10MvQJBAag5iKuyw37kDwOrruXsISNuIC/view?usp=sharing)

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
