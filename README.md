<div align="center">
 <h1> Let's Check V2 </h1>
 
 ![version](https://img.shields.io/badge/version-2.1.9-blue.svg)

 Let's check is a GPT powered end-to-end fact checking platform

![mockupv2](https://user-images.githubusercontent.com/48002577/233338000-ef6955df-2339-421d-b23b-8387709d077a.jpeg)
</div>

## Background
This repository is part of a computer science research project aimed at creating a dependable end-to-end fact-checking platform. 

The primary goal is to investigate the use of claim decompositions in breaking down complex claims into simpler components that can be more effectively verified by autonomous systems. This approach is expected to enhance the predicted veracity of claims, especially in sophisticated and novel situations.

## Overview
The fact-checking platform is designed to perform the following tasks:

1. **Claim Decomposition:** 
      
      The system will decompose the input claims into minimal, binary sub-questions. 
      While doing so, we aim to maximize the extensiveness of the  sub-questions to capture the nuance presented in the original claim.

1. **User Validation:** 
      
      The system will allow users to validate the generated sub-questions after the initial decomposition. Here, users may choose to modify, add or delete any sub-questions generated.
      
1. **Sub-Question to Hypothesis Conversion:** 
      
      To effectively verify each sub-question, the system will convert them into an equivalent sub-claim hypothesis.
        
1. **Evidence Retrieval:** 
  
    The platform will retrieve relevant evidence from trusted sources that can support or refute each sub-claim.

1. **Fact Verification:**
    
    The system will use machine learning models to verify the truthfulness of the claim by comparing it with the retrieved evidence.

1. **Reporting:**
    
    The platform will generate a report that summarizes the findings of the fact-checking process and aggregate results across all sub-claims to derive the overall veracity score.

## Demo

<div align="center">
 
 ![Product Gif](https://user-images.githubusercontent.com/48002577/233365986-7d3ce39b-8c75-491a-88e0-46bdb9bd0535.gif)

 Try it out on our live website! Write to `minglim.low@gmail.com` for Beta Access!
</div>
    
## Project Structure
The repository contains the following directories:

1. [**``data:``**](https://github.com/Avalionnet/gpt_factchecker/tree/main/data) This directory contains the dataset used to train the models that power the platform. Scripts used for training purposes are also included.
2. [**``frontend:``**](https://github.com/Avalionnet/gpt_factchecker/tree/main/frontend) This directory contains the files required to host the frontend of the platform.
3. [**``backend:``**](https://github.com/Avalionnet/gpt_factchecker/tree/main/backend) This directory contains scripts used to power our backend APIs.

## Get Started
To get started with the platform, follow these steps:

1. Clone the repository to your local machine.
1. Download the necessary datasets and pre-trained models.
1. Host the necessary backend services in our ``backend`` folder
1. Install the required libraries and dependencies by navigating to our frontend directory and run `npm install`
1. Run the platform by executing ``npm run serve``

## Proposed Architecture
The following diagram showcases a potential software architecture we can adopt for the platform

![image](https://user-images.githubusercontent.com/48002577/233361808-e5eea333-37a6-4dc5-bc2f-0fd9b656ae25.png)


## Acknowledgements
This research project is inspired by and uses the dataset from the following paper:
```
@article{chen-etal-2022-generating,
  title={Generating Literal and Implied Subquestions to Fact-check Complex Claims},
  author={Chen, Jifan and Sriram, Aniruddh and Choi, Eunsol and Durrett, Greg},
  journal={arxiv preprint},
  year={2022}
}
```

Our evidence retrieval and entailment system is made possible by the Quin system from the following paper:
```
@article{Samarinas-etal-2020,
  title = {Latent Retrieval for Large-Scale Fact-Checking and Question Answering with NLI training},
  author = {Samarinas, Chris and Hsu, Wynne and Lee, Mong},
  year = {2020}
}
```
