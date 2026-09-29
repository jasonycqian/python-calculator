
from graphics import *
import random
import math
from time import sleep

WIDTH, HEIGHT = 800, 800
X_MIN, X_MAX = -10, 10
Y_MIN, Y_MAX = -10, 10


def draw_button(a,b,c,d):
    button=Circle(Point(a,b), c)
    button.setWidth(0)
    button.setFill(color_rgb(220,210,195))
    button.draw(d)

def label_button(a,b,c,d,e):
    buttondisplaysgrid=[
        ["\u221a", "ANS", "\u232B", "AC"],
        ["7", "8", "9", "\u00f7"],
        ["4", "5", "6", "\u00d7"],
        ["1", "2", "3", "-"],
        ["0", ".", "=", "+"]
    ]
    label=Text(Point(a,b),buttondisplaysgrid[c][d])
    label.setSize(30)
    label.draw(e)
    return buttondisplaysgrid[c][d]

def math_to_screen(x, y):
    """Converts Cartesian (x, y) coordinates to pixel Point(px, py)."""
    px = (x - X_MIN) / (X_MAX - X_MIN) * WIDTH
    py = HEIGHT - ((y - Y_MIN) / (Y_MAX - Y_MIN) * HEIGHT)
    return Point(px, py)

def draw_axes_and_labels(win):
    """Draws X/Y axes, tick marks, and coordinate numbers."""
    origin = math_to_screen(0, 0)

    # Main X-Axis
    x_axis = Line(Point(0, origin.getY()), Point(WIDTH, origin.getY()))
    x_axis.setFill("gray")
    x_axis.draw(win)

    # Main Y-Axis
    y_axis = Line(Point(origin.getX(), 0), Point(origin.getX(), HEIGHT))
    y_axis.setFill("gray")
    y_axis.draw(win)

    # X-Axis Ticks & Labels
    for x in range(X_MIN, X_MAX + 1):
        if x == 0:
            continue  # Skip origin to avoid overlap
        pt = math_to_screen(x, 0)

        # Tick mark
        tick = Line(Point(pt.getX(), pt.getY() - 4), Point(pt.getX(), pt.getY() + 4))
        tick.draw(win)

        # Label text
        lbl = Text(Point(pt.getX(), pt.getY() + 15), str(x))
        lbl.setSize(8)
        lbl.setFill("darkgray")
        lbl.draw(win)

    # Y-Axis Ticks & Labels
    for y in range(Y_MIN, Y_MAX + 1):
        if y == 0:
            continue
        pt = math_to_screen(0, y)

        # Tick mark
        tick = Line(Point(pt.getX() - 4, pt.getY()), Point(pt.getX() + 4, pt.getY()))
        tick.draw(win)

        # Label text
        lbl = Text(Point(pt.getX() - 15, pt.getY()), str(y))
        lbl.setSize(8)
        lbl.setFill("darkgray")
        lbl.draw(win)

def safe_eval(expr, x_val):
    """Evaluates the string equation safely with Python's math module."""
    # Context dictionary exposes math functions (sin, cos, sqrt, etc.) and 'x'
    allowed_context = {
        "x": x_val,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "abs": abs,
        "pi": math.pi,
        "e": math.e,
    }
    return eval(expr, {"__builtins__": None}, allowed_context)

def plot_equation(win, expr_str, line_objects, ungraph, ungraph_txt):
    ungraph_txt.undraw()
    ungraph.undraw()
    """Erase old function lines and plot the new equation string."""
    # Undraw previous graph lines
    for line in line_objects:
        line.undraw()
    line_objects.clear()

    sample_count = 320
    points = []

    for step in range(sample_count + 1):
        x = X_MIN + (step / sample_count) * (X_MAX - X_MIN)

        try:
            y = safe_eval(expr_str, x)

            if y < Y_MIN or y > Y_MAX or type(y) is complex:
                continue

            curr_pt = math_to_screen(x, y)
            points.append(curr_pt)

        except (ValueError, ZeroDivisionError, TypeError, SyntaxError):
            pass

    if not points:
        ungraph.draw(win)
        ungraph_txt.draw(win)
        return

    refined_points = [points[0]]

    def add_segment(start, end, depth=0):
        if depth >= 3:
            refined_points.append(end)
            return

        dy = abs(end.getY() - start.getY())
        if dy > 24:
            mid = Point((start.getX() + end.getX()) / 2,
                       (start.getY() + end.getY()) / 2)
            add_segment(start, mid, depth + 1)
            add_segment(mid, end, depth + 1)
        else:
            refined_points.append(end)

    for i in range(len(points) - 1):
        add_segment(points[i], points[i + 1])

    for i in range(1, len(refined_points)):
        segment = Line(refined_points[i - 1], refined_points[i])
        segment.setFill("blue")
        segment.setWidth(2)
        segment.draw(win)
        line_objects.append(segment)

    ungraph.draw(win)
    ungraph_txt.draw(win)
    update()

def draw():
    # --- Window & Grid Setup ---
    win = GraphWin("Graphing Calculator", WIDTH, HEIGHT, autoflush=False)
    win.setBackground("white")

    draw_axes_and_labels(win)

    # --- UI Controls Header ---
    # Equation Entry Box
    lbl_eq = Text(Point(135, 30), "f(x) =")
    lbl_eq.setStyle("bold")
    lbl_eq.draw(win)

    entry_box = Entry(Point(250, 30), 25)
    entry_box.setText("")
    entry_box.draw(win)

    # Plot Button Visual
    btn_box = Rectangle(Point(360, 15), Point(420, 45))
    btn_box.setFill("lightgray")
    btn_box.draw(win)

    btn_text = Text(Point(390, 30), "Plot")
    btn_text.setStyle("bold")
    btn_text.draw(win)

    
    ungraph = Rectangle (Point(562,0),Point(800,50))
    ungraph.setFill("black")
    ungraph.draw(win)

    ungraph_txt = Text(Point(681,25), "Normal Calculator")
    ungraph_txt.setSize(25)
    ungraph_txt.setTextColor("white")
    ungraph_txt.draw(win)


    drawn_lines = []

    # Initial plot
    plot_equation(win, entry_box.getText(), drawn_lines, ungraph,ungraph_txt)

    # Event Loop: Wait for mouse clicks on the Plot button
    while True:
        click_pt = win.checkMouse()
        
        if click_pt:
            # Check if click landed inside the 'Plot' button boundary
            if 360 <= click_pt.getX() <= 420 and 15 <= click_pt.getY() <= 45:
                user_expr = entry_box.getText()
                plot_equation(win, user_expr, drawn_lines, ungraph,ungraph_txt)
            if (600 < click_pt.getX() < 800) and (0 < click_pt.getY() < 50):
                win.close()
                return "calc"

        # Check for keyboard Enter key press
        key = win.checkKey()
        if key == "Escape":
            win.close()
            return None
        if key == "Return":
            user_expr = entry_box.getText()
            plot_equation(win, user_expr, drawn_lines, ungraph,ungraph_txt)

    win.close()

def calc():


    win=GraphWin("Calculator", 512, 768, autoflush=False)
    bg=Rectangle(Point(0,0), Point(512, 768))
    bg.setFill(color_rgb(0,0,0))
    bg.draw(win)
    display=Rectangle(Point(32,32), Point(480,256))
    display.setWidth(8)
    display.setOutline(color_rgb(255,0,0))
    display.setFill(color_rgb(220,210,195))
    display.draw(win)

    display_text = Text(Point(55, 70), "")
    display_text.setSize(36)
    display_text.setStyle("bold")
    display_text.draw(win)

    graph = Rectangle(Point(250,0), Point(512,50))
    graph.setFill("white")
    graph.draw(win)

    graph_txt = Text(Point(381,25), "Graphing Calculator")
    graph_txt.setSize(25)
    graph_txt.draw(win)


    result_text = Text(Point(300, 200), "")
    result_text.setSize(36)
    result_text.setStyle("bold")
    result_text.draw(win)

    buttons=[]
    button_radius=36
    for row in range(5):
        for col in range(4):
            x_buttongrid = 82 + (col * 116)
            y_buttongrid = 320 + (row * 96)
            draw_button(x_buttongrid,y_buttongrid, button_radius, win)
            button_symbol=label_button(x_buttongrid,y_buttongrid,row,col,win)
            buttons.append({
                "x": x_buttongrid,
                "y": y_buttongrid,
                "label": button_symbol
            })

    update()

    current_input=""
    current_output=""
    input_lock=False
    prev_ans=""
    while True:
        key = win.checkKey()
        if key == "Escape":
            win.close()
            return None

        click=win.checkMouse()
        if click is None:
            sleep(0.01)
            continue
    #Point(250,0), Point(512,50)
        if (250 < click.getX() < 512) and (0 < click.getY() < 50):
            win.close()
            return "draw"
        for btn in buttons:
            dx = click.getX() - btn["x"]
            dy = click.getY() - btn["y"]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance <= button_radius:
                key = btn["label"]
                if current_output=="Math ERROR" and key != "AC":  #only allows AC key if Math ERROR
                    pass
                
                elif input_lock==True and not (key in ["AC", "\u00d7", "\u00f7", "+", "-", "ANS"]): 
                    pass
                
                elif key == "AC":  #clears the input, clears the output
                    current_input = ""
                    current_output = ""
                    input_lock=False

                    
                elif key == "\u221a": #sqrt; locks input, gives an output
                    try:
                        expr = current_input.replace("\u00d7", "*").replace("\u00f7", "/").replace("ANS", prev_ans)
                        val = float(eval(expr))
                        if val < 0:
                            current_output="Math ERROR"
                        else:
                            res = math.sqrt(val)
                            if res.is_integer():
                                current_output = str(int(res))    # Turns √25 -> 5.0 -> "5"
                            else:
                                current_output = str(round(res, 6)) # Keeps √2 -> "1.414214"
                            current_input = "\u221a(" + current_input + ")"
                            input_lock = True
                            prev_ans = current_output
                    except Exception:
                        current_output="Math ERROR"


                        
                elif key == "ANS":  #adds ANS to the end of the input
                    if input_lock==True:
                        current_output=""
                        current_input="ANS"
                        input_lock=False
                    else:
                        current_input+="ANS"

                        
                elif key =="\u232B":
                    if current_input.endswith("ANS"):
                        current_input = current_input[:-3] 
                    else:
                        current_input = current_input[:-1]

                        
                elif key == "=":  
                    try:
                        expr = current_input.replace("\u00d7", "*").replace("\u00f7", "/").replace("ANS", prev_ans)
                        val = eval(expr)
                        if isinstance(val, float) and val.is_integer():
                            current_output = str(int(val)) 
                        else:
                            current_output = str(round(val, 6))   
                        prev_ans = current_output
                        input_lock = True
                    except Exception:
                        current_output = "Math ERROR"


                        
                elif key == "\u00d7" or key == "\u00f7" or key == "+" or key == "-":
                    if input_lock==True:
                        current_output=""
                        current_input="ANS"
                        input_lock=False
                    current_input+=key

                    
                else:  #must have clicked 1234567890. so add to the end of input
                    current_input+=key

                display_text.setText(current_input)
                result_text.setText(current_output)
                
                target_x_input = 55 + (len(current_input) * 20 / 2)
                current_x_input = display_text.getAnchor().getX()
                display_text.move(target_x_input - current_x_input, 0)

                target_x_output = 455 - (len(current_output) * 20 / 2)
                current_x_output = result_text.getAnchor().getX()
                result_text.move(target_x_output - current_x_output, 0)

                update()
                break
                
def main():
    screen = "calc"
    while screen is not None:
        if screen == "calc":
            screen = calc()
        else:
            screen = draw()

main()
        