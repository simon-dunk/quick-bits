import tkinter as tk
from tkinter import ttk, messagebox
import math

# --- Triangle Solver Functions ---
def solve_triangle(values):
    results = values.copy()
    steps = {"angles": [], "sides": [], "trig": [], "summary": []}

    A, B, C = values["A"], values["B"], values["C"]
    a, b, c = values["a"], values["b"], values["c"]

    # --- Find missing angle if two are known ---
    known_angles = [x for x in [A, B, C] if x is not None]
    if len(known_angles) == 2:
        missing = 180 - sum(known_angles)
        if missing <= 0:
            raise ValueError("Invalid angle values: sum exceeds 180°")
        if A is None:
            results["A"] = missing
            steps["angles"].append(f"A = 180° - B - C = {results['A']:.2f}°")
        elif B is None:
            results["B"] = missing
            steps["angles"].append(f"B = 180° - A - C = {results['B']:.2f}°")
        elif C is None:
            results["C"] = missing
            steps["angles"].append(f"C = 180° - A - B = {results['C']:.2f}°")

    # --- Use Law of Sines ---
    for side, angle in [("a", "A"), ("b", "B"), ("c", "C")]:
        if results[side] and results[angle]:
            num = results[side]
            denom = math.sin(math.radians(results[angle]))
            ratio = num / denom
            results["ratio"] = ratio
            steps["sides"].append(
                f"{side} / sin({angle}) = {num:.2f} / sin({results[angle]:.2f}°) "
                f"= {num:.2f} / {denom:.4f} = {ratio:.4f}"
            )
            break

    if "ratio" in results:
        ratio = results["ratio"]
        for side, angle in [("a", "A"), ("b", "B"), ("c", "C")]:
            if results[side] is None and results[angle]:
                results[side] = ratio * math.sin(math.radians(results[angle]))
                steps["sides"].append(f"{side} = ratio × sin({angle}) = {results[side]:.2f}")
            if results[angle] is None and results[side]:
                val = math.degrees(math.asin(results[side] / ratio))
                results[angle] = val
                steps["angles"].append(f"{angle} = arcsin({side}/ratio) = {results[angle]:.2f}°")

    # --- Trig Functions ---
    if results.get("A") and results.get("a") and results.get("b") and results.get("c"):
        steps["trig"].append(f"sin(A) = a/c = {results['a']:.2f}/{results['c']:.2f} = {results['a']/results['c']:.4f}")
        steps["trig"].append(f"cos(A) = b/c = {results['b']:.2f}/{results['c']:.2f} = {results['b']/results['c']:.4f}")
        steps["trig"].append(f"tan(A) = a/b = {results['a']:.2f}/{results['b']:.2f} = {results['a']/results['b']:.4f}")

    # --- Classification ---
    if all(results[x] for x in ["A", "B", "C"]):
        if any(abs(results[x] - 90) < 0.5 for x in ["A", "B", "C"]):
            tri_type = "Right"
        elif all(results[x] < 90 for x in ["A", "B", "C"]):
            tri_type = "Acute"
        else:
            tri_type = "Obtuse"

        if abs(results["a"]-results["b"])<1e-6 and abs(results["b"]-results["c"])<1e-6:
            tri_type += " Equilateral"
        elif abs(results["a"]-results["b"])<1e-6 or abs(results["b"]-results["c"])<1e-6 or abs(results["a"]-results["c"])<1e-6:
            tri_type += " Isosceles"
        else:
            tri_type += " Scalene"

        steps["summary"].append(f"Triangle Type: {tri_type}")

    # --- Perimeter & Area ---
    if all(results[x] for x in ["a", "b", "c"]):
        P = results["a"] + results["b"] + results["c"]
        s = P/2
        try:
            area = math.sqrt(s*(s-results["a"])*(s-results["b"])*(s-results["c"]))
            steps["summary"].append(f"Perimeter = {P:.2f}")
            steps["summary"].append(f"Area (Heron’s formula) = {area:.2f}")
        except ValueError:
            steps["summary"].append("Area could not be computed (invalid side lengths).")

    return results, steps


# --- Tkinter UI ---
class TriangleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Triangle Solver")

        self.entries = {}
        frm = ttk.Frame(root, padding=10)
        frm.pack(side="left", fill="y")

        # Input groups
        ttk.Label(frm, text="Enter Known Values", font=("Arial", 12, "bold")).pack(pady=5)
        angle_frame = ttk.LabelFrame(frm, text="Angles (°)")
        angle_frame.pack(pady=5, fill="x")
        for label, key in [("A", "A"), ("B", "B"), ("C", "C")]:
            ttk.Label(angle_frame, text=label).pack(side="left", padx=2)
            e = ttk.Entry(angle_frame, width=6)
            e.pack(side="left", padx=2)
            self.entries[key] = e

        side_frame = ttk.LabelFrame(frm, text="Sides")
        side_frame.pack(pady=5, fill="x")
        for label, key in [("a", "a"), ("b", "b"), ("c", "c")]:
            ttk.Label(side_frame, text=label).pack(side="left", padx=2)
            e = ttk.Entry(side_frame, width=6)
            e.pack(side="left", padx=2)
            self.entries[key] = e

        btn_frame = ttk.Frame(frm)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Calculate", command=self.calculate).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Clear", command=self.clear).pack(side="left", padx=5)

        # Output tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(side="right", expand=True, fill="both")

        self.text_output = tk.Text(self.notebook, wrap="word", font=("Consolas", 11))
        self.notebook.add(self.text_output, text="Steps")

        self.table_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.table_frame, text="Summary")

        self.tree = ttk.Treeview(self.table_frame, columns=("value",), show="headings")
        self.tree.heading("value", text="Value")
        self.tree.pack(expand=True, fill="both")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="darkgray")
        self.canvas.pack(side="bottom", pady=10)

    def draw_triangle(self, vals):
        self.canvas.delete("all")
        if not (vals["a"] and vals["b"] and vals["c"]):
            self.canvas.create_text(200, 200, text="Triangle will display here", fill="black")
            return

        # Simplified scaling
        a, b, c = vals["a"], vals["b"], vals["c"]
        scale = 250 / max(a, b, c)
        a, b, c = a*scale, b*scale, c*scale

        # Place points
        Ax, Ay = 50, 350
        Bx, By = 350, 350
        d = c
        x = (b**2 - a**2 + d**2) / (2*d)
        y = math.sqrt(abs(b**2 - x**2))
        Cx, Cy = Ax + x, Ay - y

        # Draw triangle outline
        self.canvas.create_polygon(Ax, Ay, Bx, By, Cx, Cy, outline="black", fill="", width=2)

        # --- Labels ---
        # Side lengths in blue
        self.canvas.create_text((Ax+Bx)/2, Ay+15, text=f"c={vals['c']:.2f}", fill="blue", font=("Arial", 10, "bold"))
        self.canvas.create_text((Ax+Cx)/2-10, (Ay+Cy)/2, text=f"b={vals['b']:.2f}", fill="blue", font=("Arial", 10, "bold"))
        self.canvas.create_text((Bx+Cx)/2+10, (By+Cy)/2, text=f"a={vals['a']:.2f}", fill="blue", font=("Arial", 10, "bold"))

        # Angles in red
        self.canvas.create_text(Ax-25, Ay, text="A", fill="red", font=("Arial", 12, "bold"))
        self.canvas.create_text(Bx+25, By, text="B", fill="red", font=("Arial", 12, "bold"))
        self.canvas.create_text(Cx, Cy-25, text="C", fill="red", font=("Arial", 12, "bold"))

        if vals["A"]:
            self.canvas.create_text(Ax-15, Ay+15, text=f"{vals['A']:.1f}°", fill="red", font=("Arial", 10))
        if vals["B"]:
            self.canvas.create_text(Bx+15, By+15, text=f"{vals['B']:.1f}°", fill="red", font=("Arial", 10))
        if vals["C"]:
            self.canvas.create_text(Cx, Cy-40, text=f"{vals['C']:.1f}°", fill="red", font=("Arial", 10))


    def calculate(self):
        try:
            values = {k: (float(v.get()) if v.get() else None) for k, v in self.entries.items()}
            if sum(1 for v in values.values() if v is not None) < 3:
                messagebox.showerror("Error", "Enter at least 3 values!")
                return
            results, steps = solve_triangle(values)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Steps output
        self.text_output.delete("1.0", tk.END)
        for cat, label in [("angles", "ANGLES"), ("sides", "SIDES"), ("trig", "TRIG FUNCTIONS"), ("summary", "SUMMARY")]:
            self.text_output.insert(tk.END, f"\n=== {label} ===\n\n")
            for s in steps[cat]:
                self.text_output.insert(tk.END, "• " + s + "\n")

        # Table summary
        for i in self.tree.get_children():
            self.tree.delete(i)
        for k in ["A", "B", "C", "a", "b", "c"]:
            if results[k]:
                self.tree.insert("", "end", values=(f"{k} = {results[k]:.2f}"))

        self.draw_triangle(results)

    def clear(self):
        for e in self.entries.values():
            e.delete(0, tk.END)
        self.text_output.delete("1.0", tk.END)
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.canvas.delete("all")
        self.canvas.create_text(200, 200, text="Triangle will display here", fill="black")


if __name__ == "__main__":
    root = tk.Tk()
    app = TriangleApp(root)
    root.mainloop()
