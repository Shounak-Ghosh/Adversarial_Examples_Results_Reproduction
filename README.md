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

### Explaining the Attacks

The adversary aims to engineer ECGs so that the classification system is mislead to give the diagnosis that he/she desires. Meanwhile, data perturbations should be sufficiently subtle that they are either imperceptible to humans or it perceptible seems natural and not representative of an attack. There are two types of attacks, Type I and Type II, each with its own threat model: 

__Type I attack:__ Adversary can access the ECG signals, and curropt them by adding perturbations i.e. a digital access to ECG signals without showing up physically on the scene where an ECG was taken.

- eg. a cardiologist with monetary incentives to fool the insurance company. (local deployment)
- A hacker who could manipulate a cloud deployed model for fun or for profit. (cloud deployment)

The evaluation of Type I attack is a bit more ambitious, i.e. it evaluates targeted attacks (Not just a misclassification, but a misclassification to a specific target class)

For a targeted attack, each class has 3 possible misclassification targets so, there are 12 possibilities. But, each target attack has to be evaluated for every distance metric (3 distance metrics were studied here). So, in total there are total 36 target possibilities. Due to time and computation limitations for the given table we will only show each of the attack as a proof of concept. The table from original experiments in the paper with 36 possibilities is shown below (The percentage represents the success rate of each attack). 

<img width="1046" alt="Screen Shot 2020-05-30 at 3 24 01 PM" src="https://user-images.githubusercontent.com/15305740/83338517-db7fe500-a28a-11ea-9527-cb02027b4ba0.png">

In the original experiment by the authors, they select first 360 correct predictions for classes A, N and O and first 220 correct predictions  for the class ~ to evaluate the success rate of targeted attack. But here one for each of the 36 possibilities is evaluated.

__Type II Attack:__ A physical injection attack where the attacker is closer to the victim. Done using electro magnetic interference. Adversary may not be able to access the ECG directly or they want to perform attack without leaving a digital tampering footage. Hence, without a digital access to the ECGs, attack is injected on-the-fly via physical processes. 
  - Since Type II attacks are done by electromagnetic interference,  'skewing in time domain between perturbation and ECG' due to attackers lack of knowledge of the exact start time of the ECG may affect the end result. So, this is modeled here by shifting perturbation at various amounts before adding to victim (Inspired by the 'Expectation over Transformation' from another paper ), such shifting is considered as a ' shifting transformation' of the original measurement (of what?) and specifued in the optimization problem. 
  - Filtering of the incoming signals is also modeled. 2 widely used filters are shown. In the generation (of what?), rectangular filter removes all the power within the selected frequency range.  To generate filtering resistant perturbations, the power (why is power constrained?) of perturbations is constrained within the filtered frequency bands during the optimization procedure. Using Fast Fourier Transform, perturbation is transformed from time domain to frequency domain, and the power of frequency domains less than 0.05 Hz and 50/60 Hz is masked to zero. And then inverse fourier transform to time domain.
  - The duration of attack (smaller duration means lower exposure risk) is also studied here. Termed as 'Perturbation window size'.
  - UNIVERSARIALITY OF AN ATTACK (I DO NOT UNDERSTAND)

### Notes on the Attacks (IMPORTANT)
- Since the accuracy of the model (DNN based ECG classification) is not 100%. The authors here create adversarial examples for only the data that was correctly classified. The frequency of this data is: 

ZZZ
- Only type I is implemented for a cloud deployed model (Although it is said to be cloud deployed, as allowed from the threat model there is no actual cloud deployment here, just the files are named cloud deployed and evaluation results are produces inside the folder named cloud_eval). whereas type II attack is implemented for a local deployment model. 

- In the type I attack evaluation, all the metrics have the same optimization and hyperparameters.

- Type II Attack is only implemented in the Local Deployement model

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
