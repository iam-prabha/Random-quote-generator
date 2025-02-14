from flask import Flask, Response
import random
import io
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# List of Data Science Quotes
quotes = [
    "Without data, you're just another person with an opinion. – W. Edwards Deming",
    "Data is the new oil. – Clive Humby",
    "The goal is to turn data into information and information into insight. – Carly Fiorina",
    "Numbers have an important story to tell. They rely on you to give them a voice. – Stephen Few",
    "Torture the data, and it will confess to anything. – Ronald Coase",
    "An approximate answer to the right problem is worth a good deal more than an exact answer to an approximate problem. – John Tukey"
]

# Tokyo Night theme colors
BACKGROUND_COLOR = (15, 20, 50)  # Deep navy blue
TEXT_COLOR = (139, 233, 253)  # Neon cyan
TEXT_SHADOW_COLOR = (68, 71, 90)  # Soft purple shadow

def generate_quote_image():
    """Generates an image with a random data science quote."""
    quote = random.choice(quotes)

    # Load font
    try:
        font = ImageFont.truetype("JetBrainsMono-Regular.ttf", 24)  # Load a specific font
    except IOError:
        font = ImageFont.load_default()  # Use default font if missing

    # Calculate text size using getbbox()
    text_bbox = font.getbbox(quote)
    text_width = text_bbox[2] - text_bbox[0]  # Width
    text_height = text_bbox[3] - text_bbox[1]  # Height

    # Create image dynamically based on text size
    img_width = max(text_width + 40, 800)  # Minimum width 800px
    img_height = max(text_height + 40, 250)  # Minimum height 250px
    img = Image.new("RGB", (img_width, img_height), color=BACKGROUND_COLOR)

    draw = ImageDraw.Draw(img)

    # Position text at the center
    x = 20
    y = (img_height - text_height) // 2  # Center vertically

    # Draw shadow for neon effect
    draw.text((x + 2, y + 2), quote, fill=TEXT_SHADOW_COLOR, font=font)
    draw.text((x, y), quote, fill=TEXT_COLOR, font=font)

    # Save image to memory
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return img_io

@app.route("/")
def home():
    return "Random Data Science Quote Generator"

@app.route("/quote")
def quote():
    """Serve a random data science quote as an image."""
    img_io = generate_quote_image()
    return Response(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
