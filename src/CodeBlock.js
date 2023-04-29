import React, { useState } from "react";
import hljs from "highlight.js";

const CodeBlock = ({ code }) => {
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const highlightedCode = hljs.highlightAuto(code).value;

  return (
    <div>
      <button className="code-button" onClick={toggleVisibility}> Show code 👇</button>{" "}
      {isVisible && (
        <pre>
          <code style={{ display: "block", margin: "20px auto", border: "2px solid var(--secondary-color)" }} dangerouslySetInnerHTML={{ __html: highlightedCode }}></code>{" "}
        </pre>
      )}{" "}
    </div>
  );
};

export default CodeBlock;
