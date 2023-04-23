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
          <code dangerouslySetInnerHTML={{ __html: highlightedCode }}></code>{" "}
        </pre>
      )}{" "}
    </div>
  );
};

export default CodeBlock;
