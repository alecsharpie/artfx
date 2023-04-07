import React from "react";
import Canvas from "./Canvas.js";
// import Countdown from "./Countdown.js";
import useFetchFileContent from "./useFetchFileContent.js";
import "./App.css";

function App() {

  return (
    <div className="container">
      <div className="logo-and-title">
        <img src="logo_128.png" alt="Logo" />
        <h1>Quote Canvas</h1>
      </div>
      <h3>
        Everyone gets to make at least one silly little GPT website, right?
      </h3>
      <p>
      New artwork created daily. GPT writes the code to create generative art using on JS on a canvas. Illustrations inspired by quotes. Refresh the page to re-generate the art.
      </p>
      {/* <Countdown /> */}
      <Canvas width={400} height={400} />
      <h3>How is it made?</h3>
      <ol>
        <li>Get WikiQuote of the day</li>
        <li>
          Feed GPT (gpt-3.5-turbo) the quote as inspiration for a Javascript
          based HTML canvas artwork. GPT is given 2 examples of the expected
          output.
        </li>
        <li>Display them here.</li>
      </ol>
      <h3>Who made this?</h3>
      <a href="https://alecsharpie.me">alecsharpie.me</a>
      <h3>Can I see the code?</h3>
      <p>
        Yes,{" "}
        <a href="https://github.com/alecsharpie/artfx">
          github.com/alecsharpie/artfx
        </a>
      </p>
    </div>
  );
}

export default App;
