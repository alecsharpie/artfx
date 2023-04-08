import React, { useEffect, useRef, useState } from "react";
import "./CanvasGrid.css";

function CanvasGrid() {
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

      console.log(data);
    };

    fetchCanvasArt();
  }, []);

  useEffect(() => {
    canvasRefs.current.forEach(({ ref }, index) => {
      const canvas = ref.current;

      if (canvas) {
        // raw on the canvas here
        eval(data[index].code);
        console.log(`Canvas ${index} is ready`);
      }
    });
  }, [data]);

  const redrawCanvas = (index) => {
    const canvas = canvasRefs.current[index].ref.current;
    const context = canvas.getContext("2d");

    // clear the canvas
    context.clearRect(0, 0, canvas.width, canvas.height);
    // redraw on the canvas
    eval(data[index].code);
    console.log(`Canvas ${index} has been redrawn`);
  };

  if (isLoading) {
    return <div> Loading... </div>;
  }

  return (
    <div className="canvas-grid">
      {" "}
      {canvasRefs.current.map(({ ref }, index) => (
        <div key={index} className="canvas-wrapper">
          <canvas className="single-canvas" ref={ref} width={500} height={500} />{" "}
          <div className="quote"> {data[index].quote} </div>{" "}
          <div className="date"> {data[index].date} </div>{" "}
          <button
            className="refresh-button"
            onClick={() => redrawCanvas(index)}
          >
            {" "}
            Regenerate{" "}
          </button>{" "}
        </div>
      ))}{" "}
    </div>
  );
}

export default CanvasGrid;
