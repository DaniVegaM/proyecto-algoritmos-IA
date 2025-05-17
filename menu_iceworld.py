import tkinter as tk
from tkinter import messagebox
from iceworld_core import IceWorld, bfs, dfs, GridVisualizer
from iceworld_core import TreeVisualizer
from hill_climbing_romania import hill_climbing, HillClimbingVisualizer, romania_map

def jugar_bfs():
    holes = [(2,4), (3,1), (1,4), (4,4)]
    world = IceWorld(6, 6, (0, 0), (5, 5), [(1,1), (1,2), (2,2), (3,4), (4,1), (4,2), (4,3)], holes)
    path, visited, frontier_steps, parent = bfs(world)
    GridVisualizer(root, world, path, visited, "Recorrido en Anchura (BFS)", frontier_steps)
    TreeVisualizer(root, parent, path, visited, "Árbol de exploración BFS")

def jugar_dfs():
    holes = [(2,4), (3,1), (1,4), (4,4)]
    world = IceWorld(6, 6, (0, 0), (5, 5), [(1,1), (1,2), (2,2), (3,4), (4,1), (4,2), (4,3)], holes)
    path, visited, frontier_steps, parent = dfs(world)
    GridVisualizer(root, world, path, visited, "Recorrido en Profundidad (DFS)", frontier_steps)
    TreeVisualizer(root, parent, path, visited, "Árbol de exploración DFS")

def jugar_hill_climbing():
    # Permite al usuario seleccionar inicio y meta con dos clics
    selector = CitySelector(root)

class CitySelector(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Selecciona ciudades de inicio y meta")
        self.geometry("800x600")
        self.offset_x, self.offset_y = 30, 20
        self.base_positions = {
            'Arad': (60, 80), 'Zerind': (120, 40), 'Oradea': (180, 20), 'Sibiu': (200, 100),
            'Fagaras': (300, 80), 'Rimnicu Vilcea': (250, 160), 'Pitesti': (350, 160),
            'Timisoara': (40, 160), 'Lugoj': (80, 220), 'Mehadia': (120, 280), 'Drobeta': (80, 340),
            'Craiova': (220, 300), 'Bucharest': (500, 200), 'Giurgiu': (520, 260),
            'Urziceni': (520, 120), 'Hirsova': (600, 80), 'Eforie': (650, 60),
            'Vaslui': (600, 200), 'Iasi': (650, 240), 'Neamt': (700, 280)
        }
        # Aplica el offset a todas las posiciones desde el inicio
        self.positions = {city: (x + self.offset_x, y + self.offset_y) for city, (x, y) in self.base_positions.items()}
        self.canvas = tk.Canvas(self, width=800, height=520, bg="white")
        self.canvas.pack()
        self.label = tk.Label(self, text="Haz clic en la ciudad de inicio y luego en la ciudad meta", font=("Arial", 14))
        self.label.pack(pady=10)
        self.draw_all_edges()
        self.draw_all_nodes()
        self.selected = []
        self.canvas.bind("<Button-1>", self.on_click)

    def draw_all_edges(self):
        drawn = set()
        # Usa las posiciones ya desplazadas para dibujar las aristas
        for city, neighbors in romania_map.items():
            x0, y0 = self.positions[city]
            for neighbor, weight in neighbors:
                edge = tuple(sorted([city, neighbor]))
                if edge in drawn:
                    continue
                drawn.add(edge)
                x1, y1 = self.positions[neighbor]
                self.canvas.create_line(x0, y0, x1, y1, fill="#bdbdbd", width=2)
                mx, my = (x0 + x1) // 2, (y0 + y1) // 2
                self.canvas.create_rectangle(mx-15, my-10, mx+15, my+10, fill="#fff", outline="#1976d2", width=1)
                self.canvas.create_text(mx, my, text=str(weight), font=("Arial", 10, "bold"), fill="#1976d2")

    def draw_all_nodes(self):
        for city, (x, y) in self.positions.items():
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill="#ffd966", outline="#616161", width=3)
            self.canvas.create_text(x, y+25, text=city, font=("Arial", 13, "bold"), fill="#222")

    def on_click(self, event):
        for city, (x, y) in self.positions.items():
            if (x-18) <= event.x <= (x+18) and (y-18) <= event.y <= (y+18):
                self.selected.append(city)
                self.highlight_city(city, len(self.selected))
                if len(self.selected) == 2:
                    self.after(500, self.run_hill_climbing)
                break

    def highlight_city(self, city, order):
        x, y = self.positions[city]
        color = "#1976d2" if order == 1 else "#ff5252"
        self.canvas.create_oval(x-22, y-22, x+22, y+22, outline=color, width=5)

    def run_hill_climbing(self):
        start, goal = self.selected
        self.destroy()
        path = hill_climbing(start, goal)
        HillClimbingVisualizer(root, path, f"Hill Climbing: {start} → {goal}", start, goal)

root = tk.Tk()
root.title("Menú Principal - Ice World")
root.geometry("400x300")

label = tk.Label(root, text="Elige una opción de juego:", font=("Arial", 16))
label.pack(pady=30)

btn_bfs = tk.Button(root, text="Jugar Ice World (BFS)", font=("Arial", 14), width=25, command=jugar_bfs)
btn_bfs.pack(pady=10)

btn_dfs = tk.Button(root, text="Jugar Ice World (DFS)", font=("Arial", 14), width=25, command=jugar_dfs)
btn_dfs.pack(pady=10)

btn_hc = tk.Button(root, text="Hill Climbing (Mapa de Rumania)", font=("Arial", 14), width=25, command=jugar_hill_climbing)
btn_hc.pack(pady=10)

root.mainloop()
