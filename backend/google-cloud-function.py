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
The canvas element has already been created and selected for you with `const canvas = ref.current;`. You just need to get the context and then draw on it.
Write the contents of a `canvas-art.js` file. Include only the code in your output: no external comments, no chat messages, no summarization.
The code will be re-run to regenerate new artwork, so some randomness needs to be included eg. `Math.random()`
Use shapes and lines wherever possible, only use text as a last resort.
If the inspiration to too long or complex, just use 1 or 2 key ideas.

Here is an example of how the input will be provided and the expected format of the output.

Inspiration:
We are all part of some cosmic pattern, and this pattern works toward good and not evil.

Output:
// Get the canvas element context, width, and height
const ctx = canvas.getContext("2d");
const displayWidth = canvas.width;
const displayHeight = canvas.height;

// Generate a pattern of circles on the canvas
for (let i = 0; i < 200; i++) {

    // Set the position and size of the circle randomly
    const x = Math.random() * displayWidth;
    const y = Math.random() * displayHeight;
    const radius = Math.random() * 50;

    // Set the color of the circle based on its position and size
    const hue = x / displayWidth * 360;
    const saturation = Math.max(0, (radius / 50) - (y / displayHeight)) * 100;
    const lightness = Math.max(0, (1 - (y / displayHeight)) * 50);

    // Draw the circle on the canvas
    ctx.fillStyle = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    ctx.beginPath();
    ctx.arc(x, y, radius, 0, Math.PI * 2);
    ctx.fill();
}

Now it's your turn to complete the output:

Inspiration
""" + inspo + """

Output:"""

    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
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


if __name__ == "__main__":

    quote = "Historical sense and poetic sense should not, in the end, be contradictory, for if poetry is the little myth we make, history is the big myth we live, and in our living, constantly remake."
    # Generate the code

    data = {
        "code": generate_code(quote),
        "quote": quote + " - Robert Penn Warren",
        "date": "2023-04-24"
    }

    with open('backend/single_result.json', 'w') as fp:
        json.dump(data, fp)
