from flask import Flask, Response, request
import random
import io
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__)

# List of Quotes with Authors
quotes = [
    (" Putting a new feature into a program is important, but refactoring so new features can be added in the future is equally important. ", " Ward Cunningham "),
    (" Without data, you're just another person with an opinion. ", " W. Edwards Deming "),
    (" Data is the new oil.", " Clive Humby "),
    (" The goal is to turn data into information and information into insight. ", " Carly Fiorina "),
    (" Numbers have an important story to tell. They rely on you to give them a voice.", " Stephen Few" ),
    (" Torture the data, and it will confess to anything. ", " Ronald Coase "),
    (" An approximate answer to the right problem is worth more than an exact answer to an approximate problem. ", " John Tukey ")
]

# Theme Colors
BG_COLOR = (15, 12, 45)  # Deep Midnight Blue
TEXT_COLOR = (190, 220, 255)  # Light Blue for readability
QUOTE_COLOR = (255, 165, 0)  # Orange for opening/closing quotes
AUTHOR_COLOR = (255, 105, 180)  # Soft Pink for author name

FONT_PATH = "Montserrat-Bold.ttf"  # Use a bold font for better readability

def wrap_text(text, font, max_width):
    """Wrap text so it fits within the given width."""
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and font.getbbox(line + words[0])[2] < max_width:
            line += (words.pop(0) + " ")
        lines.append(line.strip())
    return lines

def generate_quote_image(screen_width=800):
    """Generates a responsive quote image with curved corners and no border."""
    quote, author = random.choice(quotes)

    # Load fonts
    try:
        quote_font = ImageFont.truetype(FONT_PATH, 32)  # Larger, bold font
        author_font = ImageFont.truetype(FONT_PATH, 24)  # Slightly larger author text
    except IOError:
        quote_font = ImageFont.load_default()
        author_font = ImageFont.load_default()

    # Responsive width
    base_width = min(max(500, screen_width - 100), 900)  # Between 500px and 900px
    padding = 50
    max_text_width = base_width - (padding * 2)
    border_radius = 20  # Smooth curved edges

    # Wrap quote text
    wrapped_quote = wrap_text(f"“{quote}”", quote_font, max_text_width)
    quote_line_height = quote_font.getbbox("hg")[3]
    total_quote_height = len(wrapped_quote) * quote_line_height

    # Author text
    wrapped_author = f"- {author}"
    author_line_height = author_font.getbbox("hg")[3]

    # Calculate total height
    total_text_height = total_quote_height + author_line_height + 50  # Extra spacing
    img_height = max(150, total_text_height + padding * 2)  # Minimum height

    # Create image with curved edges
    img = Image.new("RGB", (base_width, img_height), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw background with curved corners
    draw.rounded_rectangle(
        [(0, 0), (base_width, img_height)],
        radius=border_radius,
        fill=BG_COLOR
    )

    # Calculate Y position for centered text
    y = (img_height - total_text_height) // 2

    # Draw quote text
    for i, line in enumerate(wrapped_quote):
        text_width = quote_font.getbbox(line)[2]
        x = (base_width - text_width) // 2  # Center text

        # Add styled quotation marks
        if i == 0:
            line = f"“ {line}"  # Opening quote
        if i == len(wrapped_quote) - 1:
            line = f"{line} ”"  # Closing quote

        draw.text((x, y), line, fill=TEXT_COLOR, font=quote_font)
        y += quote_line_height + 8  # Extra spacing for readability

    # Add spacing before author name
    y += 15

    # Draw author name aligned to the right
    author_text_width = author_font.getbbox(wrapped_author)[2]
    author_x = base_width - padding - author_text_width  # Right-align
    draw.text((author_x, y), wrapped_author, fill=AUTHOR_COLOR, font=author_font)

    # Save image to memory
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return img_io

@app.route("/")
def home():
    return "Responsive Quote Generator API"

@app.route("/quote")
def quote():
    """Serve a responsive data science quote as an image."""
    screen_width = request.args.get("width", default=800, type=int)  # Get width from request
    img_io = generate_quote_image(screen_width)
    return Response(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)