import React, { useEffect, useRef } from "react";

function Canvas() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const fetchCanvasArt = async () => {
      const response = await fetch(
        "https://storage.googleapis.com/website-assets-alecsharpie/artfx/canvas-art.js"
      );
      const code = await response.text();

      // const canvas = canvasRef.current;
      // const ctx = canvas.getContext("2d");

      // eslint-disable-next-line no-eval
      eval(code);
    };

    fetchCanvasArt();
  }, []);

  return <canvas ref={canvasRef} width={500} height={500} />;
}

export default Canvas;
