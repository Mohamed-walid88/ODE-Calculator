# ODE Calculator

A simple desktop application for solving and classifying Ordinary Differential Equations (ODEs). This tool uses **SymPy** for the symbolic mathematics and **PyQt5** with **Matplotlib** for the graphical user interface.

It provides a clean, user-friendly way to input differential equations, see them rendered in LaTeX, and get the symbolic solution.



## Features

* **Symbolic Solver:** Solves a variety of first-order and n-th order linear ODEs.
* **Equation Classifier:** Automatically classifies the ODE and highlights the method(s) that can be used to solve it (e.g., Separable, Homogeneous, Exact, Linear, Bernoulli).
* **Live LaTeX Preview:** Renders your input equation in a clean mathematical format as you type.
* **Beautiful Solution Display:** The final solution is displayed in a large, easy-to-read LaTeX format.
* **Flexible Input:** Supports multiple ways to write derivatives and equations.

## Requirements

To run this project, you will need Python 3 and the following libraries:

* **`sympy`**: For all symbolic mathematics and ODE solving.
* **`PyQt5`**: For the application framework and all GUI components.
* **`matplotlib`**: For rendering LaTeX strings into the GUI.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-project-name.git](https://github.com/your-username/your-project-name.git)
    cd your-project-name
    ```

2.  **Install the required libraries:**
    The easiest way is to use `pip`.

    ```bash
    pip install sympy PyQt5 matplotlib
    ```
    Or, you can create a `requirements.txt` file with the following content:
    ```
    sympy
    PyQt5
    matplotlib
    ```
    And then install from it:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

### 1. Running the Application

Run the `Setup.py` file to start the calculator:

```bash
python Setup.py
```

### 2. Entering Equations
Enter your differential equation into the top input field and press Enter. The application uses SymPy's `eval` function with a safe namespace.

**Key Syntax Rules:**
* The independent variable is `x`.
* The dependent function is `y` (which is treated as `y(x)`).
* Your equation must be an equality, written in one of two ways:
    1.  `LHS = RHS` (e.g., `y' = y * x`)
    2.  `Eq(LHS, RHS)` (e.g., `Eq(y.diff(x), y * x)`)

**Writing Derivatives:**
You can write derivatives in several ways:
* **Prime notation:** `y'`, `y''`, `y'''`
* **`diff` function:** `diff(y)` (for $y'$), `diff(y, x, 2)` (for $y''$)
* **Method call:** `y.diff(x)` (for $y'$), `y.diff(x, 2)` (for $y''$)

**Differential Form Shortcut (M + Ny' = 0):**
The app provides a convenient shortcut for equations in the form $M(x,y) + N(x,y)y' = 0$.
You can write this as `M*dx + N*dy = 0`.
* `dx` is interpreted as `1`.
* `dy` is interpreted as `y'` (or `Derivative(y, x)`).

For example, `(x+y)*dx + (x-y)*dy = 0` is interpreted as the equation `(x+y) + (x-y)*y' = 0`.

**Available Functions:**
You can use standard mathematical functions and constants:
* **Trigonometric:** `sin`, `cos`, `tan`, `csc`, `sec`, `cot`
* **Hyperbolic:** `sinh`, `cosh`
* **Exponential:** `e` (for `exp`), e.g., `e(x)` for $e^x$.

### 3. Getting the Solution
After you press **Enter**:
1.  A LaTeX preview of your *input* equation will appear just below the text box.
2.  The main window will display the symbolic *solution* to the ODE.
3.  On the left, buttons corresponding to the equation's classification (e.g., "Separable", "Linear") will become enabled.

---
### Example Inputs
Here are some valid equations you can try:

| Equation | Valid Input |
| :--- | :--- |
| $y' = y \cdot x$ | `y' = y * x` |
| $y' + y = \sin(x)$ | `y.diff(x) + y = sin(x)` |
| $(x+y) + (x-y)y' = 0$ | `(x+y)*dx + (x-y)*dy = 0` |
| $y'' + y = 0$ | `y'' + y = 0` |
| $e^x + y y' = 0$ | `Eq(e(x) + y*diff(y), 0)` |
| $\frac{dy}{dx} = \frac{y}{x}$ | `y' = y/x` |

## Project Structure
* **`Setup.py`**: This is the main file to run. It contains all the `PyQt5` GUI code, input parsing, and `matplotlib` canvas setup.
* **`CalculateODE.py`**: This is the backend solver engine. It imports `sympy` to classify and solve the equation object passed from the GUI.
