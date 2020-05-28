# Adversarial_Examples_Results_Reproduction
Results reproduction of the ECGAdv paper. 

### Setup for running the experiments
  - python version 3.6
  - 
  
  Install python 3.6
Install virtualenv
create a folder to work on and folder env where environment is installed
virtualenv -p python3.6 /Users/bibekpoudel/Desktop/AE/env/
source env/bin/activate
python -V
pip install -r requirements.txt (may not install cleverhans)

pip install cleverhans==2.1.0

pip install -e git://github.com/tensorflow/cleverhans.git@v2.0.0#egg=cleverhans

Install a kernel: ipython kernel install --user --name=.venv

 $ pip install jupyter notebook
 
 run juupyter notebook in venv 

###
Taking all the files from DNN based ECG Implementation. as seen here

###  Results

####  Results on the Local Deployment model

####  Results on the Cloud Deployment model
