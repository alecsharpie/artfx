# Daily Artwork by GPT based on WIkiQuote of the day.

#### Backend
A google cloud function reaches out to openai and generates code output, saving it in a google cloud bucket.
This happens at 12pm daily, scheduled by google cloud scheduler.

#### Frontend
A react app that fetches the generated code from the google cloud bucket and renders it.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.


## Credits
One of the examples in the prompt is based on [this codepen example](https://codepen.io/balazs_sziklai/pen/vYZBWR)
