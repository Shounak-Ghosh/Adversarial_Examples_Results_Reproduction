# Adversarial_Examples_Results_Reproduction
Results reproduction of the ECGAdv paper. 

### Setting up a virtual environment for running the experiments
The dependency versions for the project are:  
  - python version 3.6.5
  - Tensorflow version 1.8.0
  - Keras version 2.2.0
  - Cleverhans version 2.0.0
  
For this, we need to install python 3.6.5 and then install virtualenv to create a vritual environment.
Then, create a folder to work on and inside it a folder (named env here) where environment is installed

      $ virtualenv -p python3.6 /Path/to/virtual/env/

Then activate the virtual environment (from terminal inside the working folder not inside env folder):

      $ source env/bin/activate

Check the python version (tensorflow 1.8.0 installation below requires python 3.6.5)

      $ python -V

Install dependencies. (Cleverhans version 2.0.0 was not submitted to PyPi. so, I installed version 2.1.0 hoping everything works)

      $ pip install tensorflow==1.8.0
      $ pip install cleverhans==2.1.0
      $ pip install keras==2.2.0

If working directly from python scripts you are done (in this repo too this method is done). Skip to Next title.
But this can further be extended to work in Jupyter Notebook inside a virtual environment.
 
      $ pip install jupyter notebook

Now Install a kernel so that the version of dependencies that we installed above are used by jupyter

      $ ipython kernel install --user --name=.venv

Run Jupyter. Be sure to check the presence of .venv in while creating a new file in 'New' at the top right.

      $ jupyter notebook

###  Getting the files Ready
Copy all the files from DNN based ECG classification implementation as seen [here](https://github.com/Bibek-Poudel/DNN_ECG_Implementation).This contains the victim model as well as all the files from preciction made by that model. Make a copy of the file revised_label.csv and rename it to REFERENCE-v3.csv 

Copy the 9 files named below (from this repository), these are associated with Type I attack (explained in the next section):

  - cloud_eval_l2.py, myattacks_l2.py, myattacks_tf_l2.py: For L2 metric
  
  - cloud_eval_diffl2.py, myattacks_diffl2.py, myattacks_tf_diffl2.py : For XXX metric
  
  - cloud_eval_diff.py, myattacks_diff.py, myattacks_tf_diff.py: For dsmooth metric

Copy the YY files named below (from this repository), these are associated with Type II attack (explained in the next section):
  - LDM_Attack.py, LDM_EOT.py, LDM_EOT_tf.py
  
  - LDM_UniversalEval.py

In addition, create a folder named 'cloud model' and 

### Notes on the Attacks (IMPORTANT)
- Since the accuracy of the model (DNN based ECG classification) is not 100%. The authors here create adversarial examples for only the data that was correctly classified. The frequency of this data is: 

ZZZ
- Only type I is implemented for a cloud deployed model (Although it is said to be cloud deployed, as allowed from the threat model there is no actual cloud deployment here, just the files are named cloud deployed and evaluation results are produces inside the folder named cloud_eval). whereas type II attack is implemented for a local deployment model. 


###  Results. 
It takes very long time to generate perturbations. In some cases it took me 10 minutes to generate perturbation for 1 ECG.

__1.Generate Attack Perturbations for cloud Deployment model using the 3 metrics__
There are 12 variations created by the combination of distance metric and correct prediction for each class. First step is to create perturbations for all variations.

      python attack_file index_file start_idx end_idx
      
      python cloud_eval_l2.py data_select_A.csv 1 360
      python cloud_eval_l2.py data_select_N.csv 1 360
      python cloud_eval_l2.py data_select_O.csv 1 360
      python cloud_eval_l2.py data_select_i.csv 1 220
      
      python cloud_eval_diff.py data_select_A.csv 1 360
      python cloud_eval_diff.py data_select_N.csv 1 360
      python cloud_eval_diff.py data_select_O.csv 1 360
      python cloud_eval_diff.py data_select_i.csv 1 220
      
      python cloud_eval_diffl2.py data_select_A.csv 1 360
      python cloud_eval_diffl2.py data_select_N.csv 1 360
      python cloud_eval_diffl2.py data_select_O.csv 1 360
      python cloud_eval_diffl2.py data_select_i.csv 1 220

__2.For perturbations in each class compare the target to other 3 classes __

- Type I, Type II (Can both type I and type II have local and cloud deployed models?)
- Cloud deployed, Local deployed
- with EOT and without
- Effect of window
- Type I results, different similarity metrics (is it for cloud or local?)
####  Results on the Local Deployment model

####  Results on the Cloud Deployment model

####  Understanding the attack algorithm
