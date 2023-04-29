import React from "react";
import CanvasGrid from "./CanvasGrid.js";
import Countdown from "./Countdown.js";
import "./App.css";

function App() {
  return (
    <div className="container">
      <div className="logo-and-title">
        <img src="logo_128.png" alt="Logo" />
        <h1> Quote Canvas </h1>{" "}
      </div>{" "}
      <h3>
        Everyone gets to make at least one silly little GPT website, right ?
      </h3>{" "}
      <h2> Generated Generative Art </h2>{" "}
      <p> New artwork generated daily, inspired by quotes. </p>{" "}
      <p>
        GPT writes the code to create generative art using Javascript on a
        canvas.{" "}
      </p>{" "}
      <p className="instructions">
        Click the "Regenerate" button to render a new version of each artwork.{" "}
      </p>{" "}
      <Countdown />
      <CanvasGrid width="66%" height={300} /> <h3> How is it made ? </h3>{" "}
      <ol>
        <li> Ask Wikipedia for the quote of the day </li>{" "}
        <li>
          Feed an AI (large language model, gpt-4) the quote as
          inspiration along with an example of the expected output.{" "}
        </li>{" "}
        <li>
          The AI generates code for a Javascript based HTML canvas artwork.{" "}
        </li>{" "}
        <li> Store the generated pieces of code and render them here. </li>{" "}
      </ol>{" "}
      <h3> Who made this ? </h3>{" "}
      <a href="https://alecsharpie.me"> alecsharpie.me </a> <h3> Why ? </h3>{" "}
      <ul>
        <li> Fun! </li> <li> Experimenting with reliable code generation. </li>{" "}
      </ul>{" "}
      <h3> Can I see the code ? </h3>{" "}
      <p>
        Yes,{" "}
        <a href="https://github.com/alecsharpie/artfx">
          github.com / alecsharpie / artfx{" "}
        </a>
        .The prompt is{" "}
        <a href="https://github.com/alecsharpie/artfx/blob/main/google-cloud-function.py">
          here{" "}
        </a>{" "}
      </p>{" "}
    </div>
  );
}

export default App;
