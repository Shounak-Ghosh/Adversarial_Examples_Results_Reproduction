# Adversarial Examples Results Reproduction.
Results reproduction of the Type I attack explained as given in ECGAdv [paper](https://arxiv.org/abs/1901.03808). I have given a brief explanation of the Type I attack [here](https://github.com/Bibek-Poudel/Adversarial_Examples_Results_Reproduction/blob/master/Type_I_Attack_Explanation.pdf). 
This tutorial is based on the companion code of the paper, as given [here](https://github.com/codespace123/ECGadv)

### Step 1: Setting up a virtual environment for running the experiments
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

Although the original code has implemented everything in python script, I have also used Jupyter Notebook 
Lets install Jupyter Notebook inside our virtual environment.
 
      $ pip install jupyter notebook

Now Install a kernel so that the version of dependencies that we installed above are used by jupyter

      $ ipython kernel install --user --name=.venv

Run Jupyter. Be sure to check the presence of .venv in while creating a new file in 'New' at the top right.

      $ jupyter notebook 

###  Step 2: Getting the files Ready
Copy all the files from DNN based ECG classification implementation as seen [here](https://github.com/Bibek-Poudel/DNN_ECG_Implementation).This contains the victim model as well as all the files from preciction made by that model. Make a copy of the file revised_label.csv and rename it to REFERENCE-v3.csv 

ECGAdv internally uses Cleverhans [Library](https://github.com/tensorflow/cleverhans). Type I attack is contained in the 9 files given below. Copy them,(from this repository. Each file is based on some metric to measure distance between adversarial and real ECG signal (explained in next section):

  - cloud_eval_l2.py, myattacks_l2.py, myattacks_tf_l2.py: For L2 metric
  
  - cloud_eval_diffl2.py, myattacks_diffl2.py, myattacks_tf_diffl2.py : For DSmooth,L2 metric
  
  - cloud_eval_diff.py, myattacks_diff.py, myattacks_tf_diff.py: For dsmooth metric

Now, create a folder named 'cloud model' in the working folder and create folders named 'l2_eval', 'smooth_eval' and 'l2smooth_0_01_eval' to store the perturbations for L2, dsmooth and dsmooth l2 metrics respectively. I did not decide these folder names, the original implementation has this.

### Step 3: Explaining the Attacks

The adversary aims to engineer ECGs so that the classification system is mislead to give the diagnosis that he/she desires. Meanwhile, data perturbations should be sufficiently subtle that they are either imperceptible to humans or it perceptible seems natural and not representative of an attack. There are two types of attacks, Type I and Type II, each with its own threat model: 

__Type I attack:__ Adversary can access the ECG signals, and curropt them by adding perturbations i.e. a digital access to ECG signals without showing up physically on the scene where an ECG was taken.

- eg. a cardiologist with monetary incentives to fool the insurance company. (local deployment)
- A hacker who could manipulate a cloud deployed model for fun or for profit. (cloud deployment)

The evaluation of Type I attack is a bit more ambitious, i.e. it evaluates targeted attacks (Not just a misclassification, but a misclassification to a specific target class)

For a targeted attack, each class has 3 possible misclassification targets so, there are 12 possibilities. But, each target attack has to be evaluated for every distance metric (3 distance metrics were studied here). So, in total there are total 36 target possibilities. Due to time and computation limitations for the given table we will only show each of the attack as a proof of concept. The table from original experiments in the paper with 36 possibilities is shown below (The percentage represents the success rate of each attack). 

![Group](https://user-images.githubusercontent.com/15305740/83802116-cf6f9b00-a66f-11ea-99e5-9599077ea27e.png)

In the original experiment by the authors, they select first 360 correct predictions for classes A, N and O and first 220 correct predictions  for the class ~ to evaluate the success rate of targeted attack. But here one for each of the 36 possibilities is evaluated.

### Notes on the Attack (IMPORTANT)
- Since the accuracy of the model (DNN based ECG classification) is not 100%. The authors here create adversarial examples for only the data that was correctly classified. 
- Only type I is implemented for a cloud deployed model (Although it is said to be cloud deployed, as allowed from the threat model there is no actual cloud deployment here, just the files are named cloud deployed and evaluation results are produces inside the folder named cloud_eval). whereas type II attack is implemented for a local deployment model. 

###  Step 4: Proof of concept results. 
It takes very long time to generate perturbations. In some cases it took me 10 minutes to generate perturbation for 1 ECG.

__1.Generate Attack Perturbations for Type I attack using the 3 metrics__
There are 12 variations created by the combination of distance metric and correct prediction for each class. First step is to create perturbations for all variations.

Attack File: Specifies the distance metric (eval_l2, eval_diff, eval_diffl2)
Index File: Specifies the class of correctly classified data for which perturbation is to be generated

      python attack_file index_file start_idx end_idx
      
      python cloud_eval_l2.py data_select_A.csv 1 2 (*)
      python cloud_eval_l2.py data_select_N.csv 1 2
      python cloud_eval_l2.py data_select_O.csv 1 2
      python cloud_eval_l2.py data_select_i.csv 1 2
      
      python cloud_eval_diff.py data_select_A.csv 1 2 (*)
      python cloud_eval_diff.py data_select_N.csv 1 2
      python cloud_eval_diff.py data_select_O.csv 1 2
      python cloud_eval_diff.py data_select_i.csv 1 2
      
      python cloud_eval_diffl2.py data_select_A.csv 1 2 (*)
      python cloud_eval_diffl2.py data_select_N.csv 1 2
      python cloud_eval_diffl2.py data_select_O.csv 1 2
      python cloud_eval_diffl2.py data_select_i.csv 1 2

The end_idx is set to 2, means that we are only generating one adversarial example per attack file (for each attack file 3 examples are generated, one for each metric. So if we execute all 9 we get 36 variations as shown in table 3 above.) 

The 3 files for each record correspond to the 3 classes other than the ground truth for which the given signal can be targeted. For example: when I execute __python cloud_eval_l2.py data_select_A.csv 1 2__ , The first ECG record from data_select_A.csv (meaning ground truth is class A) is used to craft adversarial examples for classes N, O and ~.

For simplicity, in this repository I have executed only the scripts denoted as (*). Each execution of this script generate 3 files for each record (9 files in total). This corresponds to the green colored regions in the table 3 from paper shown above.

__2. Verify the Generated Adversarial Examples__

Above, we generated perturbations for each class N,0,~ for the record file (A00005) which happens to be the first file in data_select_A.csv with ground truth class A. 
Here for each of the 9 samples generate from above, inside corresponding sub-folders in the 'cloud model' folder we want to feed them to the model and see if they work as expected.

I modified the metric_compare_.py file given in the original implementation to create a file Modified_Metric_compare.ipynb


__3. Lets have a look at some Adversarial Example plots__


![1](https://user-images.githubusercontent.com/15305740/83810400-af46d880-a67d-11ea-9a96-1b598cf222cc.png)
Plot 1: Ground Truth- class Atrial Fibrilation, Predicted as- class Normal Rhythm, Distance metric- DsmoothL2


![Unknown-1](https://user-images.githubusercontent.com/15305740/83810465-cc7ba700-a67d-11ea-99f8-204285c629ef.png)
Plot 2: Ground Truth- class Atrial Fibrilation, Predicted as- class ~ (Noise), Distance metric- DsmoothL2
