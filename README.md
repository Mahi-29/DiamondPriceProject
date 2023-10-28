# This is my End to End Project

## Steps to create the projects 
### First initialize the git
```git init```

### Publish the repo
```
git add . / git add abc.txt

git commit -m "This is my first commit"
```
### Sync changes from git :
```
git pull
```
### Setup Environment
Run the init.setup.sh file using below command to create a conda environment, activate env and install requirements.
```
. init_setup.sh
```
### Create your project template by running template.py
```
python template.py
```
### create your setup file and to install your package run below command
```
python setup.py install
```  
### Another way to install local package add -e . in your requirements.txt file and run
```
pip install -r requirements.txt
```