import functions_framework

import openai
from google.cloud import storage
import wikiquote
import json

import os
import pytz
import datetime

# schedule cloud function: https://cloud.google.com/community/tutorials/using-scheduler-invoke-private-functions-oidc

openai.api_key = os.getenv("OPENAI_API_KEY")
bucket_name = "website-assets-alecsharpie"


def generate_code(inspo):

    prompt = """
Please write the JS code to create a piece of generative art based on the given inspiration.
The canvas element has already been created and selected for you with `const canvas = ref.current;`. You just need to get the context and then draw on it.
Write the contents of a `canvas-art.js` file. Include only the code in your output: no external comments, no chat messages, no summarization.
The code will be re-run to regenerate new artwork, so some randomness needs to be included eg. `Math.random()`
Use shapes and lines wherever possible, only use text as a last resort.
If the inspiration to too complex, just use 1 or 2 key ideas.

Here is a simple example of what is expected:

Inspiration:
colored circles

Output:
// Get the canvas element context, width, and height
const ctx = canvas.getContext("2d");
var displayWidth = canvas.width;
var displayHeight = canvas.height;

// Generate a pattern of circles on the canvas
for (let i = 0; i < 20; i++) {
    // Set the color of the circle randomly
    const red = Math.floor(Math.random() * 256);
    const green = Math.floor(Math.random() * 256);
    const blue = Math.floor(Math.random() * 256);
    ctx.fillStyle = `rgb(${red}, ${green}, ${blue})`;

    // Set the position and size of the circle randomly
    const x = Math.random() * displayWidth;
    const y = Math.random() * displayHeight;
    const radius = Math.random() * 50;

    // Draw the circle on the canvas
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
}

Here is a more complex example of what is expected:

Inspiration:
sowing seeds in neon waves leads to food for all

Output:
// Get the canvas element context, width, and height
const ctx = canvas.getContext("2d");
var displayWidth = canvas.width;
var displayHeight = canvas.height;

var numCircles;
var maxMaxRad;
var minMaxRad;
var minRadFactor;
var circles;
var iterations;
var timer;
var drawsPerFrame;
var drawCount;
var bgColor,urlColor;
var TWO_PI = 2*Math.PI;
var lineWidth;

init();

function init() {
    /*
    Modify the next three variables to vary the number and radius of fractal curves ("circles").
    */
    numCircles = 1;
    maxMaxRad = 900;
    minMaxRad = 300;

    /*
    We draw closed curves with varying radius. The factor below should be set between 0 and 1,
    representing the size of the smallest radius with respect to the largest possible.
    */
    minRadFactor = 0;

    /*
    The number of subdividing steps to take when creating a single fractal curve.
    Can use more, but anything over 10 (thus 1024 points) is overkill for a moderately sized canvas.
    */
    iterations = 3;

    //number of curves to draw on every tick of the timer
    drawsPerFrame = 12;

    bgColor = "#000";
    urlColor = "#EEEEEE";

    lineWidth = 1.01;

    startGenerate();
}

function startGenerate() {
    drawCount = 0;
    ctx.setTransform(1,0,0,1,0,0);

    ctx.clearRect(0,0,displayWidth,displayHeight);

    setCircles();

    if(timer) {clearInterval(timer);}
    timer = setInterval(onTimer,1000/50);
}

function setCircles() {
    var i;
    var r,g,b,a;
    var maxR, minR;
    var grad;

    circles = [];

    for (i = 0; i < numCircles; i++) {
        maxR = minMaxRad+Math.random()*(maxMaxRad-minMaxRad);
        minR = minRadFactor*maxR;

        //define gradient
        grad = ctx.createRadialGradient(0,0,minR,0,0,maxR);
        grad.addColorStop(1,"rgba(0,170,200,0.2)");
        grad.addColorStop(0,"rgba(0,20,170,0.2)");

        var newCircle = {
            centerX: -maxR,
            centerY: displayHeight/2-50,
            maxRad : maxR,
            minRad : minR,
            color: grad, //can set a gradient or solid color here.
            //fillColor: "rgba(0,0,0,1)",
            param : 0,
            changeSpeed : 1/250,
            phase : Math.random()*TWO_PI, //the phase to use for a single fractal curve.
            globalPhase: Math.random()*TWO_PI //the curve as a whole will rise and fall by a sinusoid.
            };
        circles.push(newCircle);
        newCircle.pointList1 = setLinePoints(iterations);
        newCircle.pointList2 = setLinePoints(iterations);
    }
}

function onTimer() {
    var i,j;
    var c;
    var rad;
    var point1,point2;
    var x0,y0;
    var cosParam;

    var xSqueeze = 0.75; //cheap 3D effect by shortening in x direction.

    var yOffset;

    //draw circles
    for (j = 0; j < drawsPerFrame; j++) {

        drawCount++;

        for (i = 0; i < numCircles; i++) {
            c = circles[i];
            c.param += c.changeSpeed;
            if (c.param >= 1) {
                c.param = 0;

                c.pointList1 = c.pointList2;
                c.pointList2 = setLinePoints(iterations);
            }
            cosParam = 0.5-0.5*Math.cos(Math.PI*c.param);

            ctx.strokeStyle = c.color;
            ctx.lineWidth = lineWidth;
            //ctx.fillStyle = c.fillColor;
            ctx.beginPath();
            point1 = c.pointList1.first;
            point2 = c.pointList2.first;

            //slowly rotate
            c.phase += 0.0002;

            theta = c.phase;
            rad = c.minRad + (point1.y + cosParam*(point2.y-point1.y))*(c.maxRad - c.minRad);

            //move center
            c.centerX += 0.5;
            c.centerY += 0.04;
            yOffset = 40*Math.sin(c.globalPhase + drawCount/1000*TWO_PI);
            //stop when off screen
            if (c.centerX > displayWidth + maxMaxRad) {
                clearInterval(timer);
                timer = null;
            }

            //we are drawing in new position by applying a transform. We are doing this so the gradient will move with the drawing.
            ctx.setTransform(xSqueeze,0,0,1,c.centerX,c.centerY+yOffset)

            //Drawing the curve involves stepping through a linked list of points defined by a fractal subdivision process.
            //It is like drawing a circle, except with varying radius.
            x0 = xSqueeze*rad*Math.cos(theta);
            y0 = rad*Math.sin(theta);
            ctx.lineTo(x0, y0);
            while (point1.next != null) {
                point1 = point1.next;
                point2 = point2.next;
                theta = TWO_PI*(point1.x + cosParam*(point2.x-point1.x)) + c.phase;
                rad = c.minRad + (point1.y + cosParam*(point2.y-point1.y))*(c.maxRad - c.minRad);
                x0 = xSqueeze*rad*Math.cos(theta);
                y0 = rad*Math.sin(theta);
                ctx.lineTo(x0, y0);
            }
            ctx.closePath();
            ctx.stroke();
            //ctx.fill();

        }
    }
}

//Here is the function that defines a noisy (but not wildly varying) data set which we will use to draw the curves.
function setLinePoints(iterations) {
    var pointList = {};
    pointList.first = {x:0, y:1};
    var lastPoint = {x:1, y:1}
    var minY = 1;
    var maxY = 1;
    var point;
    var nextPoint;
    var dx, newX, newY;
    var ratio;

    var minRatio = 0.5;

    pointList.first.next = lastPoint;
    for (var i = 0; i < iterations; i++) {
        point = pointList.first;
        while (point.next != null) {
            nextPoint = point.next;

            dx = nextPoint.x - point.x;
            newX = 0.5*(point.x + nextPoint.x);
            newY = 0.5*(point.y + nextPoint.y);
            newY += dx*(Math.random()*2 - 1);

            var newPoint = {x:newX, y:newY};

            //min, max
            if (newY < minY) {
                minY = newY;
            }
            else if (newY > maxY) {
                maxY = newY;
            }

            //put between points
            newPoint.next = nextPoint;
            point.next = newPoint;

            point = nextPoint;
        }
    }

    //normalize to values between 0 and 1
    if (maxY != minY) {
        var normalizeRate = 1/(maxY - minY);
        point = pointList.first;
        while (point != null) {
            point.y = normalizeRate*(point.y - minY);
            point = point.next;
        }
    }
    //unlikely that max = min, but could happen if using zero iterations. In this case, set all points equal to 1.
    else {
        point = pointList.first;
        while (point != null) {
            point.y = 1;
            point = point.next;
        }
    }

    return pointList;
}

Now it's your turn:

Inspiration:
""" + inspo + """

Output:
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role":
            "system",
            "content":
            "You are an expert software engineer and creative generative artist who works primarily in javascript on an HTML canvas."
        }, {
            "role": "user",
            "content": prompt
        }])

    # Extract the generated code from the OpenAI response
    generated_code = response['choices'][0]['message']['content']

    # Return the generated code
    return generated_code


@functions_framework.http
def upload_generation(request):

    # returns a tuple of (quote, author)
    quote, author = wikiquote.quote_of_the_day()

    # Generate the code
    code = generate_code(quote)

    date = datetime.datetime.now(
        pytz.timezone('Australia/Melbourne')).strftime("%Y-%m-%d")

    art_data = {"code": code, "quote": quote + " - " + author, "date": date}

    # Store the code and quote in a Cloud Storage bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    db_filename = "artfx/DB.json"

    # Read in current JSON file
    blob = bucket.get_blob(db_filename)
    downloaded_file = blob.download_as_text(encoding="utf-8")
    json_data = json.loads(downloaded_file)

    limit = None
    if limit:
        if len(json_data) <= limit:
            json_data.insert(0, art_data)
        else:
            json_data.pop(-1)
            json_data.append(0, art_data)
    else:
        json_data.insert(0, art_data)

    # upload updated JSON file
    json_string = json.dumps(json_data)
    print(json_string)
    blob = bucket.blob(db_filename)
    blob.upload_from_string(json_string)

    # Return a success message
    return "Code stored successfully."
