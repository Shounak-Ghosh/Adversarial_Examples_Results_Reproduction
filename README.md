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

-cloud_eval_l2.py, myattacks_l2.py, myattacks_tf_l2.py: Type-I Attack files (cloud deployment) for L2 metric
-cloud_eval_diffl2.py, myattacks_diffl2.py, myattacks_tf_diffl2.py : Type I Attack files (cloud deployment) for XXX metric
-cloud_eval_diff.py, myattacks_diff.py, myattacks_tf_diff.py: Type I Attack files (cloud deployment) for dsmooth metric

Copy the YY files named below (from this repository), these are associated with Type II attack (explained in the next section):
-LDM_Attack.py, LDM_EOT.py, LDM_EOT_tf.py
-LDM_UniversalEval.py

In addition, create a folder named 'cloud model' and 

### Attack Notes (IMPORTANT)
- Since the accuracy of the model (DNN based ECG classification) is not 100%. The authors here create adversarial examples for only the data that was correctly classified. The frequency of this data is: 

ZZZ

__Type I and Type II are just two ways of specifying threat models__
- Type I attack: The adversary can access the ECG recordings and curropt them by adding perturbations. For example, a cardiologist who wants to fool an insurance company (local deployed) or a hacker who wants to curropt a cloud deployed model)

- Type II attack: The adversary cannot access the ECG directly or wants to fool the system without leaving digital tampering. So, on the fly injection is done by physical process (electro magnetic interference) on a locally deployed model (to mimic this, Expectation over Transformation (EOT) criteria are added in the optimization problem)

- For Type I attack (Local Deployment model), The authors select first 360 correct predictions for classes A, N and O respectively. For the class ~ the authors take the first 220 correct predictions. __('segments'?)__ . For a targeted attack each class has 3 possible misclassification targets. There are 12 possibilities. But, this has to be evaluated for each distance metric (given below). So, in total there are total 36 target possibilities.

      dl2 (Similarity metric L2 perturbations)
      dsmooth (Authors devised new metric)
      dsmooth,l2 (
      
 All the metrics have the same optimization and hyperparameters 

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
