import math
import webbrowser
import tempfile
import os

def trig_from_coords(x, y):
    # Step 1: radius
    r_squared = x**2 + y**2
    r = math.sqrt(r_squared)

    # Step 2: quadrant info
    if x > 0 and y > 0:
        quadrant = "Quadrant I"
    elif x < 0 and y > 0:
        quadrant = "Quadrant II"
    elif x < 0 and y < 0:
        quadrant = "Quadrant III"
    elif x > 0 and y < 0:
        quadrant = "Quadrant IV"
    else:
        quadrant = "On axis"

    # Step 3 & 4: trig functions with rationalized denominators
    sin_theta = f"{y}&radic;{r_squared}/{r_squared} &asymp; {y/r:.5f}"
    cos_theta = f"{x}&radic;{r_squared}/{r_squared} &asymp; {x/r:.5f}"
    tan_theta = f"{y}/{x} = {y/x:.5f}" if x != 0 else "undefined"
    csc_theta = f"{r_squared}/{y}&radic;{r_squared} &asymp; {r/y:.5f}" if y != 0 else "undefined"
    sec_theta = f"{r_squared}/{x}&radic;{r_squared} &asymp; {r/x:.5f}" if x != 0 else "undefined"
    cot_theta = f"{x}/{y} = {x/y:.5f}" if y != 0 else "undefined"

    # HTML template with separate sections for each trig function
    html_content = f"""
    <html>
    <head>
        <title>Trig Functions from Coordinates</title>
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f5f5;
                color: #333;
                margin: 20px;
            }}
            h1 {{
                color: #2c3e50;
            }}
            section {{
                background-color: #ffffff;
                border-radius: 10px;
                padding: 15px 20px;
                margin-bottom: 15px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }}
            pre {{
                font-family: 'Courier New', monospace;
                background-color: #ecf0f1;
                padding: 10px;
                border-radius: 5px;
                overflow-x: auto;
            }}
        </style>
    </head>
    <body>
        <h1>Trig Functions from Coordinates</h1>
        <section>
            <h2>Input Coordinates</h2>
            <pre>x = {x}, y = {y}</pre>
        </section>
        <section>
            <h2>Radius & Quadrant</h2>
            <pre>r&sup2; = {r_squared}
r = &radic;{r_squared} &asymp; {r:.5f}
Quadrant: {quadrant}</pre>
        </section>
        <section>
            <h2>sin &theta;</h2>
            <pre>{sin_theta}</pre>
        </section>
        <section>
            <h2>cos &theta;</h2>
            <pre>{cos_theta}</pre>
        </section>
        <section>
            <h2>tan &theta;</h2>
            <pre>{tan_theta}</pre>
        </section>
        <section>
            <h2>csc &theta;</h2>
            <pre>{csc_theta}</pre>
        </section>
        <section>
            <h2>sec &theta;</h2>
            <pre>{sec_theta}</pre>
        </section>
        <section>
            <h2>cot &theta;</h2>
            <pre>{cot_theta}</pre>
        </section>
    </body>
    </html>
    """

    # Write HTML to a temporary file and open in default browser (macOS-safe)
    with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
        f.write(html_content)
        temp_filename = f.name

    os.system(f"open {temp_filename}")  # Works reliably on macOS

if __name__ == "__main__":
    try:
        x = float(input("Enter x coordinate: "))
        y = float(input("Enter y coordinate: "))
        trig_from_coords(x, y)
    except ValueError:
        print("Please enter valid numbers for x and y.")
