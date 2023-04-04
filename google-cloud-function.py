import functions_framework

import openai
from google.cloud import storage
import wikiquote

import os
# import pytz
# import datetime

openai.api_key = os.getenv("OPENAI_API_KEY")
bucket_name = "website-assets-alecsharpie"

def generate_code(inspo):

    prompt = """
    Please write the JS code to create a piece of generative art based on the given inspiration.
    The canvas element has already been created for you, you just need to select it and draw on it.
    Write the contents of a `canvas-art.js` file. Include only the code in your output: no external comments, no chat messages, no summarisation.

    Here is a simplified example of what is expected:

    Inspiration:
    colored circles

    Expected output:
    // Get the canvas element and its context
    const canvas = document.querySelector('canvas');
    const ctx = canvas.getContext('2d');

    // Generate a pattern of circles on the canvas
    for (let i = 0; i < 20; i++) {
    // Set the color of the circle randomly
    const red = Math.floor(Math.random() * 256);
    const green = Math.floor(Math.random() * 256);
    const blue = Math.floor(Math.random() * 256);
    ctx.fillStyle = `rgb(${red}, ${green}, ${blue})`;

    // Set the position and size of the circle randomly
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    const radius = Math.random() * 50;

    // Draw the circle on the canvas
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
    }

    Now it's your turn

    Inspiration:
    """ + inspo + """

    Output:
    """

    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are an expert software engineer and generative artist who works primarily in javascript on an HTML canvas."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the generated code from the OpenAI response
    generated_code = response['choices'][0]['message']['content']

    # Return the generated code
    return generated_code

# date = datetime.datetime.now(pytz.timezone('US/Pacific')).strftime("%Y/%m/%d")


@functions_framework.http
def upload_generation(request):

    # returns a tuple of (quote, author)
    inspiration = wikiquote.quote_of_the_day()

    # Generate the code
    code = generate_code(inspiration[0])

    # Store the code and quote in a Cloud Storage bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    code_filename = "artfx/canvas-art.js"
    blob = bucket.blob(code_filename)
    blob.upload_from_string(code)

    quote_filename = "artfx/quote.txt"
    blob = bucket.blob(quote_filename)
    blob.upload_from_string(inspiration[0] + " - " + inspiration[1])

    # Return a success message
    return "Code stored successfully."
