# SUN Circuits

This repository benchmarks various parameterizations of quantum circuits, specifically within the context of SU(N) matrices. The project explores different circuit designs, their decompositions, and applications like the Ising model.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Introduction

This repository aims to benchmark different parametrizations of these circuits, comparing their efficiency and accuracy in various contexts.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/MSRudolph/SUN-circuits.git
    cd SUN-circuits
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

- **Notebooks**: The Jupyter notebooks demonstrate various circuit designs and their applications. To run them, use:

    ```bash
    jupyter notebook
    ```

- **Core Functions**: Functions for quantum gate decomposition, benchmarking, and other utilities are located in the `Parameter-Mapping/` directory. These can be imported and used in your own scripts or notebooks.

## Project Structure

