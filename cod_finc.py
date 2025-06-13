import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify, diff
from sympy.utilities.lambdify import implemented_function

x = symbols('x')

# Ավելացնում ենք cot ֆունկցիա, որ numpy-ն ճանաչի
def cot(x):
    return 1 / np.tan(x)

custom_funcs = {"cot": cot, "sin": np.sin, "cos": np.cos, "tan": np.tan}

def solve_equation():
    try:
        expr = sympify(entry_func.get())
        f = lambdify(x, expr, modules=[custom_funcs, 'numpy'])
        df_expr = diff(expr, x)
        df = lambdify(x, df_expr, modules=[custom_funcs, 'numpy'])
        
        a = float(entry_a.get())
        b = float(entry_b.get())
        method = method_var.get()

        if method == "Լարերի մեթոդ":
            root = secant_method(f, a, b)
        elif method == "Շոշափողի մեթոդ":
            root = newton_raphson(f, df, a)
        elif method == "Համակցման մեթոդ":
            root = hybrid_bisection_secant(f, a, b)
        elif method == "Կրկնատեղադրման մեթոդ":
            root = fixed_point_iteration(expr, a)
        else:
            raise ValueError("Սխալ մեթոդ")

        result_label.config(text=f"Լուծում ≈ {root:.6f}")
        plot_graph(f, str(expr), root)

    except Exception as e:
        messagebox.showerror("Սխալ", str(e))

def secant_method(f, x0, x1, tol=1e-6, max_iter=100):
    for _ in range(max_iter):
        if abs(f(x1) - f(x0)) < 1e-12:
            raise ValueError("Զգուշացեք՝ բաժանում զրոյի վրա")
        x2 = x1 - f(x1)*(x1 - x0)/(f(x1) - f(x0))
        if abs(x2 - x1) < tol:
            return x2
        x0, x1 = x1, x2
    raise ValueError("Լարերի մեթոդը չհաջողվեց")

def newton_raphson(f, df, x0, tol=1e-6, max_iter=100):
    for _ in range(max_iter):
        dfx0 = df(x0)
        if abs(dfx0) < 1e-12:
            raise ValueError("Արտածյալը զրո է")
        x1 = x0 - f(x0)/dfx0
        if abs(x1 - x0) < tol:
            return x1
        x0 = x1
    raise ValueError("Շոշափողի մեթոդը չհաջողվեց")

def hybrid_bisection_secant(f, a, b, tol=1e-6, max_iter=100):
    if f(a)*f(b) > 0:
        raise ValueError("f(a) և f(b) ունեն նույն նշանը")
    for _ in range(max_iter):
        c = (a + b) / 2
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
        if abs(f(b) - f(a)) < 1e-12:
            continue
        s = b - f(b)*(b - a)/(f(b) - f(a))
        if abs(f(s)) < tol:
            return s
        if f(a) * f(s) < 0:
            b = s
        else:
            a = s
        if abs(b - a) < tol:
            return (a + b)/2
    raise ValueError("Համակցման մեթոդը չհաջողվեց")

def fixed_point_iteration(expr, x0, tol=1e-6, max_iter=100):
    f_expr = expr
    g_expr = x - 0.1 * f_expr
    g = lambdify(x, g_expr, modules=[custom_funcs, 'numpy'])
    for _ in range(max_iter):
        x1 = g(x0)
        if abs(x1 - x0) < tol:
            return x1
        x0 = x1
    raise ValueError("Կրկնատեղադրման մեթոդը չհաջողվեց")

def plot_graph(f, label, root):
    x_vals = np.linspace(root - 5, root + 5, 400)
    y_vals = f(x_vals)
    plt.figure()
    plt.plot(x_vals, y_vals, label=f"f(x) = {label}")
    plt.axhline(0, color='gray', linestyle='--')
    plt.axvline(root, color='red', linestyle='--', label=f'x ≈ {root:.6f}')
    plt.title('Ֆունկցիայի գրաֆիկ')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.legend()
    plt.grid(True)
    plt.show()

# === Գրաֆիկական միջերես ===
root = tk.Tk()
root.title("Ոչ գծային հավասարումների լուծում")

tk.Label(root, text="Մուտքագրեք հավասարումը (օր. sin(x) - x/2):").pack()
entry_func = tk.Entry(root, width=40)
entry_func.pack()

tk.Label(root, text="Մուտքագրեք միջակայքի առաջին արժեքը (a):").pack()
entry_a = tk.Entry(root, width=20)
entry_a.pack()

tk.Label(root, text="Մուտքագրեք երկրորդ արժեքը (b):").pack()
entry_b = tk.Entry(root, width=20)
entry_b.pack()

method_var = tk.StringVar(value="Լարերի մեթոդ")
tk.OptionMenu(root, method_var, "Լարերի մեթոդ", "Շոշափողի մեթոդ", "Համակցման մեթոդ", "Կրկնատեղադրման մեթոդ").pack()

tk.Button(root, text="Լուծել", command=solve_equation).pack(pady=10)
result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
