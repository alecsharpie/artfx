import React, { useEffect, useRef, useState } from "react";
import "./Canvas.css";

function Canvas() {
  const canvasRefs = useRef([]);
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchCanvasArt = async () => {
      const response = await fetch(
        "https://storage.googleapis.com/website-assets-alecsharpie/artfx/DB.json"
      );
      const data = await response.json();

      canvasRefs.current = data.map(() => ({
        ref: React.createRef(),
        width: 500,
        height: 500,
      }));

      setData(data);
      setIsLoading(false);

      console.log(data)
    };

    fetchCanvasArt();
  }, []);

  useEffect(() => {
    canvasRefs.current.forEach(({ ref }, index) => {
      const canvas = ref.current;

      if (canvas) {
        // Draw on the canvas here
        eval(data[index].code);
        console.log(`Canvas ${index} is ready`);
      }
    });
  }, [canvasRefs.current]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="canvas-grid">
      {canvasRefs.current.map(({ ref }, index) => (
        <div key={index} className="canvas-wrapper">
          <canvas ref={ref} width={500} height={500} />
          <div className="quote">{data[index].quote}</div>
          <div className="date">{data[index].date}</div>
        </div>
      ))}
    </div>
  );
}

export default Canvas;
