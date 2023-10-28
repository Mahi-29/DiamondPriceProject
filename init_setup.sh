echo [$(date)]: "Start"

echo [$(date)]: "Creating the python 3.8 environment using conda" 
conda create --prefix ./env python=3.8 -y

echo [$(date)]: "Activating the environment"
conda activate env/

echo [$(date)]: "Installing the Requirements"
pip install -r requirements.txt

echo [$(date)]: "End"

