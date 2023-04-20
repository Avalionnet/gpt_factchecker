# Navigating The Data Folder
This folder contains all the files used in our research and experimentation with the T5x and GPT-3 models to enhance the veracity predictions of end-to-end fact-checking systems.

## Structure
This folder contains the following directories:

#### 1. `claimdecomp_data:` 
This directory contains the datasets used for training our models. 
They are retrieved from the CLAIMDECOMP dataset described in the following paper:
> [**Generating Literal and Implied Subquestions to Fact-check Complex Claims**](https://arxiv.org/pdf/2205.06938.pdf)<br/>
> Jifan chen, Aniruddh Sriram, Eunsol Choi, Greg Durrett<br/>
> arxiv preprint

Some modications were made and you may find the cleaned dataset used for fine-tuning in the `3_filtered_data` directory. 

#### 2. `eval_data:`
In this directory, you can find the results of the evaluation of our claim decomposition module and the overall performance of our pipeline.
  
#### 3. `scripts:`
This directory contains all scripts used for dataset retrieval, experimentation, fine-tuning and evaluation.

#### 4. `t5x_model_checkpoint:`
You may find our fine-tuned T5x Model checkpoint for claim decomposition here. 

This is built upon the following base model: `google/t5-v1_1-large`
