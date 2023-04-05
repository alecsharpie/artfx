import React from "react";
import Canvas from "./Canvas.js";
import useFetchFileContent from "./useFetchFileContent.js";
import "./App.css";

function App() {

    const fileContent = useFetchFileContent(
      "https://storage.googleapis.com/website-assets-alecsharpie/artfx/quote.txt"
    );

  return (
    <div className="container">
      <div className="logo-and-title">
        <img src="logo_64.png" alt="Logo" />
        <h1>WikiQuote to Canvas</h1>
      </div>
      <h3>
        Everyone gets to make at least one silly little GPT website, right?
      </h3>
      <p>
        This is a daily new artwork created by GPT based on WIkiQuote of the
        day.
      </p>
      <p>{fileContent}</p>
      <Canvas width={400} height={400} />
      <h3>How is it made?</h3>
      <ol>
        <li>Get WikiQuote of the day</li>
        <li>
          Feed GPT the quote as inspiration for a JS based HTML canvas artwork
        </li>
        <li>Voilà</li>
      </ol>
      <h3>Can I see the code?</h3>
      <p>Yes,</p>
      <a href="https://github.com/alecsharpie/artfx">
        github.com/alecsharpie/artfx
      </a>
    </div>
  );
}

export default App;
