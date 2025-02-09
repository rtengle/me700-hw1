
# Overview

This repository contains code for Assignment 1 in ME 700, including functions for the Bisection Method and Newton's method for finding zeros. These are called from the ```src.zeros.py``` file.

# Bisection Method Algorithm

1. Starting with a function $f(x)$ with two guesses $A = f(a)$ and $B=f(b)$ where $\text{sign}(a) \neq \text{sign}(b)$.
2. Determine the current interval's midpoint $m = \frac{a+b}{2}$ and its function value $M=f(m)$.
3. If $M = 0$, return $m$. If $\text{sign}(m) = a$, repeat the method along the interval $x \in [m, b]$. Otherwise, repeat the method along the inverval $x \in [a, m]$.
4. Repeat this until either the tolerance is reached ($|M| \leq \text{tol}$) or until the stated maximum iterations is reached.

# Newton's Method Algorithm

1. Start with a fully differentiable function $\vec{f}(\vec{x}): \mathbb{R}^n\rightarrow \mathbb{R}^m$ and an initial guess $\vec{x}_0 \in \mathbb{R}^n.$
2. Compute the Jacobian $\mathbf{J}(\vec{f}, \vec{x}_n), $ of the matrix as defined by:
```math 
\mathbf{J}\left(\vec{f}, \vec{x}_n\right) = \left[
    \begin{matrix}
        \frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n} \\
        \vdots  & \ddots & \vdots \\
        \frac{\partial f_m}{\partial x_1} & \cdots & \frac{\partial f_m}{\partial x_n}
    \end{matrix} 
 \right] \Big |_{\vec{x} = \vec{x}_n}
```
3. Compute the next vector as:
```math
\vec{x}_{n+1} = \vec{x}_n - \mathbf{J}^{\mathbb{I}}\left(\vec{f}, \vec{x}_n \right) \vec{f}(\vec{x}_n)
```
where $\mathbf{A}^\mathbb{I}$ is the relevant generalized inverse function for the matrix $\mathbb{A} \in \mathbb{R}^{n \times m}$:
  - If $n = m$, then a standard inverse is used.
  - If $n > m$, then the right-handed inverse is used defined by $\mathbf{A}^\mathbb{I} = \mathbf{A}^T \left( \mathbf{A} \mathbf{A}^T\right)^{-1}$
  - If $n < m$, then the left-handed inverse is used defined by $\mathbf{A}^\mathbb{I} = \left(\mathbf{A}^T \mathbf{A} \right)^{-1} \mathbf{A}$
4. Iterate until either convergence is reached or the step limit is reached.
# Installation

To install this package, please begin by setting up a conda environment (mamba also works):
```bash
conda create --name me700-hw1-env python=3.12
```
Once the environment has been created, activate it:

```bash
conda activate me700-hw1-env
```
Double check that python is version 3.9.18 in the environment. It should still work on a later version, but it was made on this one.
```bash
python --version
```
Ensure that pip is using the most up to date version of setuptools:
```bash
pip install --upgrade pip setuptools wheel
```
Create an editable install of the bisection method code (note: you must be in the correct directory):
```bash
pip install -e .
```
Test that the code is working with pytest:
```bash
pytest -v --cov=. --cov-report=xml
```
Code coverage should be 100%. Now you are prepared to write your own code based on this method and/or run the tutorial.