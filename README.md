# What is Preacher?

**Preacher** is a small program written in python, to natively interact with 3-D wireframe models.
The general idea is to **interact with your models with your hands**, instead of a silicone keyboard.
This makes interacting with 3D models much more instinctive, and can have production values in industrial manufacturing.
At this stage, Preacher is suitable for small wireframe models, with medium number of nodes, and edges, but I plan to soon add GPU support.
With one more camera for better depth estimation for hand positions, this program can be extended for scientific causes, instead of 
purely educational and visualization purposes.

## Demonstration

Note, that the image on screen is moved completely by hands, and not by keyboard, or mouse.

![demonstration video](https://github.com/user-attachments/assets/80e0edbf-7d27-41aa-b6ac-6c3a0116d9aa)


## Installation

1. **Download and Install Poetry**  
   **Poetry** is used for dependency management and packaging in this project. To install Poetry, follow these steps:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -

2. **Clone repository**
   
   To clone this repository, type:

    ```bash
    git clone git clone https://github.com/thisismars-x/Preacher.git
    cd Preacher

3. **Install dependencies**
   
   Type:

    ```bash
    poetry install
    poetry shell

4. **Run an example**
   
   Run:

    ```bash
    python3 main.py --no-shell

5. **Run your model**
   
   - Put your model under **src**.
   - Go to **declarations.py** and change **EXAMPLE** to your model name(ending with .obj)

## CONTROLS

Use your **left hand** for **rotation**, by pinching thumb and index fingers.
Use your **right hand** for **translation**.
It suffices to say, but do not block the camera, or do not record in very dim lighted corners.


## ADVANCED CONTROLS

Preacher supports a very minimal interface to interact with.
The only operations it supports are: **help instructions**, and **setting up global variables**.


To investigate everything you may do through this interface, type in **'help'**.
The details of this project can be read through **'info'**.
To get a summary of the global variables of the project, simply type **'return'**.
You may set rotation speed, camera index, and more through this interface directly.
Type, **SHOWCVWINDOW 1**, to show opencv window along with the main program.
This can be directly done, through the terminal by passing **--cv-open** while running main.py.

Run:

```bash
python3 main.py
