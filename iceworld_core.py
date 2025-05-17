import tkinter as tk
import time
import threading

# Parámetros del grid
GRID_ROWS = 6
GRID_COLS = 6
START = (0, 0)
GOAL = (5, 5)
WALLS = [(1,1), (1,2), (2,2), (3,4), (4,1), (4,2), (4,3)]
HOLES = [(2, 4), (3, 1)]

class IceWorld:
    def __init__(self, rows, cols, start, goal, walls, holes):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.goal = goal
        self.walls = set(walls)
        self.holes = set(holes)

    def neighbors(self, pos):
        r, c = pos
        moves = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
        valid = [p for p in moves if 0 <= p[0] < self.rows and 0 <= p[1] < self.cols and p not in self.walls and p not in self.holes]
        return valid

# Visualización del grid y recorrido
class GridVisualizer(tk.Toplevel):
    def __init__(self, master, world, path, visited, title, frontier_steps=None):
        super().__init__(master)
        self.title(title)
        self.world = world
        self.path = path
        self.visited = visited
        self.frontier_steps = frontier_steps or []
        self.cell_size = 60
        self.canvas = tk.Canvas(self, width=world.cols*self.cell_size, height=world.rows*self.cell_size)
        self.canvas.pack()
        self.info_label = tk.Label(self, text="", font=("Arial", 14))
        self.info_label.pack(pady=5)
        self.draw_grid()
        self.step = 0
        self.agent = None
        self.after(500, self.animate)

    def draw_grid(self, highlight=None, frontier=None):
        for r in range(self.world.rows):
            for c in range(self.world.cols):
                x0, y0 = c*self.cell_size, r*self.cell_size
                x1, y1 = x0+self.cell_size, y0+self.cell_size
                color = "#e0f7fa"  # celeste claro
                if (r, c) in self.world.walls:
                    color = "#616161"  # gris oscuro
                elif (r, c) in self.world.holes:
                    color = "#212121"  # casi negro
                elif (r, c) == self.world.goal:
                    color = "#ffe082"  # amarillo meta
                if frontier and (r, c) in frontier:
                    color = "#b2ff59"  # verde claro para frontera
                if highlight and (r, c) == highlight:
                    color = "#ff5252"  # rojo para nodo actual
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray", width=2)
                # Dibuja iconos
                if (r, c) in self.world.holes:
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="💀", font=("Arial", 28))
                elif (r, c) == self.world.goal:
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="⭐", font=("Arial", 28))
                elif (r, c) == self.world.start:
                    self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="🚩", font=("Arial", 24))

    def animate(self):
        if self.step < len(self.visited):
            r, c = self.visited[self.step]
            frontier = self.frontier_steps[self.step] if self.frontier_steps and self.step < len(self.frontier_steps) else []
            self.canvas.delete("all")
            self.draw_grid(highlight=(r, c), frontier=frontier)
            # Dibuja el agente
            x0, y0 = c*self.cell_size, r*self.cell_size
            x1, y1 = x0+self.cell_size, y0+self.cell_size
            self.canvas.create_oval(x0+10, y0+10, x1-10, y1-10, fill="#1976d2", tags="agent")
            self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="🤖", font=("Arial", 24), tags="agent")
            self.info_label.config(text=f"Paso {self.step+1}/{len(self.visited)} | Nodo actual: {(r, c)} | Frontera: {frontier}")
            self.step += 1
            self.after(500, self.animate)
        else:
            # Dibuja el camino final
            for (r, c) in self.path:
                x0, y0 = c*self.cell_size, r*self.cell_size
                x1, y1 = x0+self.cell_size, y0+self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, fill="#ffd966", outline="gray", width=2)
            # Redibuja inicio, meta y pozos
            for r in range(self.world.rows):
                for c in range(self.world.cols):
                    x0, y0 = c*self.cell_size, r*self.cell_size
                    x1, y1 = x0+self.cell_size, y0+self.cell_size
                    if (r, c) in self.world.holes:
                        self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="💀", font=("Arial", 28))
                    elif (r, c) == self.world.goal:
                        self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="⭐", font=("Arial", 28))
                    elif (r, c) == self.world.start:
                        self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="🚩", font=("Arial", 24))
            # Dibuja el agente en la meta
            gr, gc = self.world.goal
            x0, y0 = gc*self.cell_size, gr*self.cell_size
            x1, y1 = x0+self.cell_size, y0+self.cell_size
            self.canvas.create_oval(x0+10, y0+10, x1-10, y1-10, fill="#1976d2", tags="agent")
            self.canvas.create_text((x0+x1)//2, (y0+y1)//2, text="🤖", font=("Arial", 24), tags="agent")
            self.info_label.config(text="¡Recorrido terminado!")

# Algoritmos de búsqueda
def bfs(world):
    from collections import deque
    queue = deque([world.start])
    visited = set([world.start])
    parent = {world.start: None}
    order = []
    frontier_steps = []
    while queue:
        node = queue.popleft()
        order.append(node)
        frontier_steps.append(list(queue))
        if node == world.goal:
            break
        for neighbor in world.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
    # Reconstruir camino
    path = []
    node = world.goal
    while node:
        path.append(node)
        node = parent.get(node)
    path.reverse()
    return path, order, frontier_steps, parent

def dfs(world):
    stack = [world.start]
    visited = set([world.start])
    parent = {world.start: None}
    order = []
    frontier_steps = []
    while stack:
        node = stack.pop()
        order.append(node)
        frontier_steps.append(list(stack))
        if node == world.goal:
            break
        for neighbor in world.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                stack.append(neighbor)
    # Reconstruir camino
    path = []
    node = world.goal
    while node:
        path.append(node)
        node = parent.get(node)
    path.reverse()
    return path, order, frontier_steps, parent

class TreeVisualizer(tk.Toplevel):
    def __init__(self, master, parent, path, visited, title):
        super().__init__(master)
        self.title(title)
        self.parent = parent
        self.path = set(path)
        self.visited = visited
        self.node_positions = {}
        self.radius = 18
        self.level_gap = 80
        self.node_gap = 60
        self.margin_x = 40
        self.margin_y = 40
        self.canvas_width = 1000
        self.canvas_height = 700
        self.canvas = tk.Canvas(self, width=self.canvas_width, height=self.canvas_height, bg="white", scrollregion=(0,0,self.canvas_width,self.canvas_height))
        self.hbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.hbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.vbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.vbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.build_tree()
        self.draw_tree()

    def build_tree(self):
        # Construye niveles del árbol
        levels = {}
        max_depth = 0
        for node in self.visited:
            depth = 0
            p = self.parent.get(node)
            while p is not None:
                depth += 1
                p = self.parent.get(p)
            if depth not in levels:
                levels[depth] = []
            levels[depth].append(node)
            if depth > max_depth:
                max_depth = depth
        self.levels = levels
        # Calcula posiciones
        for depth, nodes in levels.items():
            n = len(nodes)
            for i, node in enumerate(nodes):
                # Espaciado horizontal dinámico
                x = self.margin_x + (self.canvas_width - 2*self.margin_x) * (i+1)/(n+1)
                # Espaciado vertical proporcional a la profundidad real
                y = self.margin_y + (self.canvas_height - 2*self.margin_y) * (depth)/(max_depth if max_depth > 0 else 1)
                self.node_positions[node] = (x, y)

    def draw_tree(self):
        # Dibuja aristas
        for node, p in self.parent.items():
            if p is not None and node in self.node_positions and p in self.node_positions:
                x0, y0 = self.node_positions[p]
                x1, y1 = self.node_positions[node]
                color = "#ffd966" if node in self.path and p in self.path else "#bdbdbd"
                self.canvas.create_line(x0, y0, x1, y1, fill=color, width=3 if color=="#ffd966" else 1)
        # Dibuja nodos
        for node, (x, y) in self.node_positions.items():
            fill = "#ffd966" if node in self.path else ("#1976d2" if node == self.visited[0] else "#b2dfdb")
            outline = "#ff5252" if node == self.visited[-1] else "#616161"
            self.canvas.create_oval(x-self.radius, y-self.radius, x+self.radius, y+self.radius, fill=fill, outline=outline, width=3)
            self.canvas.create_text(x, y, text=str(node), font=("Arial", 12, "bold"))
