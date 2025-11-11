# Practica-Final-Estructura-de-Datos


# Shortest Path Finder

## Team Members
- **Thomas Bedoya**
-  **Juan Esteban Jimenez**
-  **Juan Jose Garcia**
## Project Description
This project is part of the Algorithms and Data Structures course. The provided application visualizes graphs and computes shortest paths. The current code implements **Dijkstra's algorithm** for single-source shortest paths and includes UI.

The program allows users to:
- Visualize a graph interactively using a PyQt5 GUI.
- Generate a random adjacency matrix that is not always fully connected.
- Display and edit the adjacency matrix directly.
- Draw the graph visually from the matrix.
- Compute shortest paths using Dijkstra’s algorithm.
  

## Project Structure
Project Root  
│  
├── grafos.ui           # Qt Designer interface (UI layout)  
├── grafos.py           # Auto-generated UI code (from grafos.ui)  
├── grafos.pyw          # PyQt wrapper script (optional entry point)  
├── main.py             # Main application logic (graph drawing & algorithms; Dijkstra implementation)  
└── README.md           # Documentation file  

## Technologies Used
- Python 3.10+  
- PyQt5 — For GUI design and interaction.  
- Qt Designer — For interface creation.  
- QGraphicsScene and QGraphicsView — For dynamic graph visualization.

## How to Run
### 1. Clone the Repository
git clone https://github.com/<your-username>/<your-repo-name>.git  
cd <your-repo-name>

### 2. Install Dependencies
Make sure you have Python and pip installed. Then run:  
pip install PyQt5

### 3. Run the Application
python main.py

## How It Works
1. Matrix Input:  
   - The program displays a table (QTableWidget) representing the adjacency matrix.  
   - Clicking on the table header can auto-fill the matrix with random weights.

2. Graph Drawing:  
   - Each node is represented as a circle with a label.  
   - Edges are created based on nonzero entries in the adjacency matrix.  
   - The user can visualize and interact with the graph (move nodes, inspect edges).

3. Shortest Path Calculation:  
   - The user selects a start node.  
   - The program runs Dijkstra’s algorithm to compute the shortest distances to every other node.  
   - Results are displayed with distances and reconstructed paths.


## Example of Execution
1. Launch the program with:  
   python main.py

2. Click on the header of the table to generate a random matrix.

3. Press "Dibujar Grafo" to visualize the graph.

4. Enter a start node (for example, `1`) and click "Calcular Dijkstra" to display shortest paths and distances.

## Build and Release
To prepare the final deliverable:
1. Ensure your repository includes:  
   - `src/` (source code)  
   - `README.md`  
   - `build/` or compilation instructions

2. Create a tagged release:  
git tag -a v1.0 -m "Final version"  
git push origin v1.0


## Rules and Considerations
- Allowed languages: Python, C++, or Java only.  
- Plagiarism: Any uncredited code reuse will result in a grade of 0.0.  
- Personalize the project where possible (custom graph generator, UI improvements, visualization features).

## License
This project is for academic purposes and follows EAFIT University academic integrity guidelines.

## GUI Overview
The GUI includes:  
- A table for matrix editing.  
- A button to draw the graph (`Dibujar Grafo`).  
- Controls to run Dijkstra and show results.  
- A dynamic graph display area (`QGraphicsView`).

Repository: https://github.com/<your-username>/<your-repo-name>  
Version: v1.0  
Language: Python 3 + PyQt5  
Institution: EAFIT University — School of Applied Sciences and Engineering
