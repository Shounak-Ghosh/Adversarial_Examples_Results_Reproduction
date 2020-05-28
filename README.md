# Adversarial_Examples_Results_Reproduction
Results reproduction of the ECGAdv paper. 

### Setting up an environment for running the experiments
The dependency versions for the project are:  
  - python version 3.6.5
  - Tensorflow version 1.8.0
  - Keras version 2.2.0
  - Cleverhans version 2.0.0
  
For this, we need to install python 3.6.5 and then install virtualenv to create a vritual environment.
Then, create a folder to work on and inside it a folder (named env here) where environment is installed

`virtualenv -p python3.6 /Path/to/virtual/env/`

Then activate the virtual environment (from terminal inside the working folder):

`source env/bin/activate`

Check the python version (tensorflow 1.8.0 installation below requires python 3.6.5)

`python -V`

Install dependencies. (Cleverhans version 2.0.0 was not submitted to PyPi. so, I installed version 2.1.0 hoping everything works)

`pip install tensorflow==1.8.0
pip install cleverhans==2.1.0
pip install keras==2.2.0`


Install a kernel: ipython kernel install --user --name=.venv

 $ pip install jupyter notebook
 
 run juupyter notebook in venv 

###
Taking all the files from DNN based ECG Implementation. as seen here

### Notes
Since the accuracy of the model (DNN based ECG classification) is not 100%. The authors here create adversarial examples for only the data that was correctly classified. The frequency of this data is: 

###  Results

####  Results on the Local Deployment model

####  Results on the Cloud Deployment model
