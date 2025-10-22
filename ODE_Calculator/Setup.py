import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton
)
from sympy import symbols, Function, Eq, diff, Derivative, latex, sin, cos, tan, sinh, cosh, exp, sec, csc, cot
from CalculateODE import solving_ode
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class ODESolverApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ODE Calculator")
        self.resize(800, 600)

        # safe eval namespace
        x = symbols('x')
        y = Function('y')(x)
        self._safe = {
            'x': x,
            'y': y,
            'Eq': Eq,
            'diff': diff,
            'Derivative': Derivative,
            'sin': sin, 'csc': csc,
            'cos': cos, 'sec': sec,
            'tan': tan, 'cot': cot,
            'sinh': sinh,
            'cosh': cosh,
            'e': exp
        }

        # overall layout
        main = QVBoxLayout(self)

        # — top: input line —
        self.input = QLineEdit()
        self.input.setPlaceholderText(
            "Enter ODE, e.g. (x + sin(y)*diff(x) + (y**2 + x * cos(y))*diff(y)) = 0"
        )
        self.input.returnPressed.connect(self.on_enter)
        main.addWidget(self.input)

        # — slim LaTeX preview under the input —
        # create a very short figure
        self.in_fig, self.in_ax = plt.subplots(figsize=(6, 0.3))
        self.in_ax.axis('off')
        self.input_canvas = FigureCanvas(self.in_fig)
        # fix its height so it's just one line tall
        self.input_canvas.setFixedHeight(40)
        main.addWidget(self.input_canvas)

        # — bottom: split 1/3 buttons | 2/3 solution —
        body = QHBoxLayout()
        main.addLayout(body)

        # left: method buttons
        self.method_buttons = {}
        btn_layout = QVBoxLayout()
        body.addLayout(btn_layout, 1)

        self.methods = [
            ("Separable",    "separable"),
            ("Homogeneous",  "homogeneous"),
            ("Exact",        "exact"),
            ("Linear",       "linear"),
            ("Bernoulli",    "Bernoulli"),
            ("n-th Homog",    "homogeneous"),
            ("n-th Non‑homog","non-homogeneous"),
            ("Var of Params","variation of parameters"),
        ]
        for lbl, key in self.methods:
            btn = QPushButton(lbl)
            btn.setEnabled(False)
            btn_layout.addWidget(btn)
            self.method_buttons[key] = btn

        # right: solution canvas
        self.sol_fig, self.sol_ax = plt.subplots(figsize=(6, 3))
        self.sol_ax.axis('off')
        self.sol_canvas = FigureCanvas(self.sol_fig)
        body.addWidget(self.sol_canvas, 2)

        self._eq = None

    def on_enter(self):
        txt = self.input.text().strip()
        txt = self.replace_quoted_derivatives(txt)
        txt = self.replace_equal_sign(txt)
        txt = txt.replace('dx', 'diff(x)').replace('dy', 'diff(y)')
        try:
            eq = eval(txt, {"__builtins__": {}}, self._safe)
        except Exception as e:
            self._show_input_message(f"Parse error: {e}")
            self._show_solution_message("❌ Parse error — no solution")
            self._enable_buttons([])
            return

        # preview input as LaTeX
        try:
            latex_in = latex(eq)
            self._show_input_latex(latex_in)
        except Exception:
            self._show_input_message(txt)

        # solve and classify
        sol, classes = solving_ode(eq)
        self._enable_buttons(classes)

        if sol is None:
            self._show_solution_message("❌ Could not solve.")
        else:
            self._show_solution_latex(sol)

        self._eq = eq

    def _enable_buttons(self, keys):
        for key, btn in self.method_buttons.items():
            btn.setEnabled(key in keys)

    def _show_input_latex(self, latex_str):
        self.in_ax.clear()
        # smaller font to fit one line
        self.in_ax.text(0.5, 0.5, f'${latex_str}$',
                        ha='center', va='center', fontsize=12)
        self.in_ax.axis('off')
        self.input_canvas.draw()

    def _show_input_message(self, msg):
        self.in_ax.clear()
        self.in_ax.text(0.5, 0.5, msg,
                        ha='center', va='center', fontsize=10)
        self.in_ax.axis('off')
        self.input_canvas.draw()

    def _show_solution_latex(self, sol):
        sol_latex = latex(sol)
        self.sol_ax.clear()
        self.sol_ax.text(0.5, 0.5, f'${sol_latex}$',
                         ha='center', va='center', fontsize=18)
        self.sol_ax.axis('off')
        self.sol_canvas.draw()

    def _show_solution_message(self, msg):
        self.sol_ax.clear()
        self.sol_ax.text(0.5, 0.5, msg,
                         ha='center', va='center', fontsize=14)
        self.sol_ax.axis('off')
        self.sol_canvas.draw()

    def replace_quoted_derivatives(self, expr_str):
        pattern = r"y(['′]+)"

        def replacer(match):
            num_quotes = len(match.group(1))
            return f"y.diff(x, {num_quotes})"

        return re.sub(pattern, replacer, expr_str)

    def replace_equal_sign(self, expr_str):
        idx = expr_str.find("=")
        return "Eq(" + expr_str[:idx] + ", " + expr_str[idx+1:] + ")"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ODESolverApp()
    win.show()
    sys.exit(app.exec_())
