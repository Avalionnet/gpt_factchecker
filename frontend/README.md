# Let's Check Frontend


 ![version](https://img.shields.io/badge/version-2.1.9-blue.svg)
 
<div align="center">

![Product Gif](https://user-images.githubusercontent.com/48002577/233365914-f31c445e-b9f6-437b-87e8-58bb27752bf9.gif)

</div>

## Snapshots

| Landing Page | Decomposition Process | Edit Sub-Questions | Modify Decompositions  | Hypothesis Conversion | Result Screen | Reviewing Evidence  |
| --- | --- | --- | ---  | --- | --- | ---  |
| ![stage0](https://user-images.githubusercontent.com/48002577/233344622-68c7b700-3a0c-45c7-be74-81f8a3e31c20.jpg) |  ![stage1](https://user-images.githubusercontent.com/48002577/233343752-5b13f40f-ee8a-4f84-b0ff-fba736b2d1c0.jpg) |  ![stage 2](https://user-images.githubusercontent.com/48002577/233343790-2abaabbb-9c54-4e91-b7a3-230ec0e98529.jpg)|  ![stage2edit](https://user-images.githubusercontent.com/48002577/233343846-10bdc041-24e9-4564-b021-3f906be73133.jpg)|  ![stage3](https://user-images.githubusercontent.com/48002577/233343883-46455449-34d4-42ff-8990-8546cad86857.jpg)|  ![stage5](https://user-images.githubusercontent.com/48002577/233343903-e997169e-37be-495e-ad5e-ce5f946c5f79.jpg)|  ![stage5evi](https://user-images.githubusercontent.com/48002577/233344176-bc949eb5-6e5e-452c-9029-0f939cc9aaab.jpg)

# Quick start

## Project setup

Run the following command on your terminal/cmd:
```
npm install
```
If you face any dependency issues during the installation, you may replace the following in package.json:

```
"scripts": {
    "serve": "export NODE_OPTIONS=--openssl-legacy-provider && vue-cli-service serve",
    "build": "export NODE_OPTIONS=--openssl-legacy-provider && vue-cli-service build",
    "lint": "export NODE_OPTIONS=--openssl-legacy-provider && vue-cli-service lint"
}
```

### To compile and load local development server (ie. 192.168....)
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

## File Structure
Within the download you'll find the following directories and files:

1. **`public:`** The directory where our image assets lie
1. **`src:`** The directory where we store all our components for the site
    1. **`firebase:`** The directory which stores files essential to setup your firebase deployment
    1. **`routes:`** You may modify the content displayed by different site routes (eg. abc.com/route) here via the router
    1. **`views:`** The directory which stores the main components which power the frontend
      
      There are 2 main files within the `views` folder that you affects the current frontend website:
      1. **`./Console.vue:`** Changes to the landing page of the site should be made here
      1. **`./Dashboard/QuestionTable.vue:`** 
        Powers the result table that displays the decomposed sub-questions and sub-claims. 
        It also encapsulates the column that displays the evidence collated by Quin in Stage 5
  
      1.  **`./NotFoundPage.vue:`** Displayed when users enter an invalid site route that is not specified in the router

## Deploying with Firebase
1. Create a firebase project on the Google Firebase Console.
1. Add the necessary details to the `firebase/firebaseInit.js` file to link your project to this repository
1. Run the following command to save the current vueJS build: `npm run build`
1. To deploy, run `firebase deploy`

## Acknowledgements
The frontend platform is built on the `vue argon dashboard` created by `Creative Tim` and uses some of its bootstrap components.

- Copyright 2020 Creative Tim (https://www.creative-tim.com/?ref=bvad-github-readme)
- Licensed under MIT (https://github.com/creativetimofficial/vue-argon-dashboard/blob/master/LICENSE.md)
