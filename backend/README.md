# Navigating the Backend
This folder contains all the files required to setup your backend API services. Since these services do not require any memory retention, sessions do not need to be preserved. As such, we would recommend deploying them to serverless cloud services like Google Cloud Functions or AWS Lambda.

To expedite the setup process, you may find the python files needed to establish our 2 backend API services in this directory.

## Structure
This folder contains files for 2 services:

#### 1. `Claim Decomposition Service:` 
You may upload the following file `decomp.py` as is to Google Cloud Functions to run this service.
However, do remember to add your own OpenAI key.

The model used here has also undergone fine-tuning with the datasets found in our `data` directory. As such, you will need to fine-tune them on your own before being able to utilize this service properly.

#### 2. `Sub-Question to Hypothesis Conversion Service:` 
You may upload the following file `hypothesize.py` as is to Google Cloud Functions to run this service.
However, do remember to add your own OpenAI key.

#### 3. `requirements.txt:` 
Add this file to all Google Cloud Function instances for the required libraries to be installed.

## Google Cloud Function
Setup Used:

1. **Region Used:** Asia-Southeast1
1. **Version:** 2nd Gen
1. **Runtime:** Python 3.9

![image](https://user-images.githubusercontent.com/48002577/233360860-4e2cd8b2-8e21-4527-9025-624ff1f5a780.png)
