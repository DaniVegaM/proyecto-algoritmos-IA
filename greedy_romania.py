import tkinter as tk
from hill_climbing_romania import romania_map, heuristics

def greedy_search(start, goal):
    current = start
    path = [current]
    total_cost = 0
    visited = set([current])
    while current != goal:
        neighbors = [(n, c) for n, c in romania_map[current] if n not in visited]
        if not neighbors:
            break
        # Elige el vecino con menor heurística (sin importar el costo real)
        next_city, cost = min(neighbors, key=lambda x: heuristics[x[0]])
        path.append(next_city)
        total_cost += cost
        visited.add(next_city)
        if heuristics[next_city] >= heuristics[current]:
            break  # No hay mejora
        current = next_city
    if current != goal:
        return None, None
    return path, total_cost

def greedy_search_backtracking(start, goal):
    path = []
    visited = set()
    steps = []  # Para animación: (ciudad, acción)
    found = [False]
    def dfs(current):
        if found[0]:
            return
        path.append(current)
        visited.add(current)
        steps.append((current, 'forward'))
        if current == goal:
            found[0] = True
            return
        # Ordena vecinos por heurística
        neighbors = [(n, c) for n, c in romania_map[current] if n not in visited]
        neighbors.sort(key=lambda x: heuristics[x[0]])
        for neighbor, _ in neighbors:
            dfs(neighbor)
            if found[0]:
                return
        # Retroceso
        path.pop()
        steps.append((current, 'backtrack'))
    dfs(start)
    if not found[0]:
        return None, None, steps
    # Calcular costo total
    total_cost = 0
    for i in range(len(path)-1):
        for n, c in romania_map[path[i]]:
            if n == path[i+1]:
                total_cost += c
                break
    return path, total_cost, steps

class GreedyVisualizer(tk.Toplevel):
    def __init__(self, master, path, cost, title, start, goal):
        super().__init__(master)
        self.title(title)
        self.geometry("800x600")
        self.offset_x, self.offset_y = 30, 20
        self.positions = {
            'Arad': (60, 80), 'Zerind': (120, 40), 'Oradea': (180, 20), 'Sibiu': (200, 100),
            'Fagaras': (300, 80), 'Rimnicu Vilcea': (250, 160), 'Pitesti': (350, 160),
            'Timisoara': (40, 160), 'Lugoj': (80, 220), 'Mehadia': (120, 280), 'Drobeta': (80, 340),
            'Craiova': (220, 300), 'Bucharest': (500, 200), 'Giurgiu': (520, 260),
            'Urziceni': (520, 120), 'Hirsova': (600, 80), 'Eforie': (650, 60),
            'Vaslui': (600, 200), 'Iasi': (650, 240), 'Neamt': (700, 280)
        }
        self.positions = {city: (x + self.offset_x, y + self.offset_y) for city, (x, y) in self.positions.items()}
        self.canvas = tk.Canvas(self, width=800, height=520, bg="white")
        self.canvas.pack()
        self.label = tk.Label(self, text="", font=("Arial", 14))
        self.label.pack(pady=10)
        self.path = path
        self.cost = cost
        self.start = start
        self.goal = goal
        self.draw_all_edges()
        self.draw_all_nodes()
        self.after(500, self.animate_path, 0)

    def draw_all_edges(self):
        drawn = set()
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
            color = "#ffd966" if self.path and city in self.path else "#bdbdbd"
            outline = "#1976d2" if city == self.start else ("#ff5252" if city == self.goal else "#616161")
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill=color, outline=outline, width=3)
            self.canvas.create_text(x, y+25, text=city, font=("Arial", 13, "bold"), fill="#222")

    def animate_path(self, step):
        self.canvas.delete("path_arrow")
        self.canvas.delete("weight_anim")
        if self.path and step < len(self.path)-1:
            city1 = self.path[step]
            city2 = self.path[step+1]
            x0, y0 = self.positions[city1]
            x1, y1 = self.positions[city2]
            self.canvas.create_line(x0, y0, x1, y1, fill="#1976d2", width=5, arrow=tk.LAST, tags="path_arrow")
            # Dibuja el peso de la arista animada con fondo
            for neighbor, weight in romania_map[city1]:
                if neighbor == city2:
                    mx, my = (x0 + x1) // 2, (y0 + y1) // 2
                    self.canvas.create_rectangle(mx-15, my-10, mx+15, my+10, fill="#ffd966", outline="#1976d2", width=2, tags="weight_anim")
                    self.canvas.create_text(mx, my, text=str(weight), font=("Arial", 12, "bold"), fill="#1976d2", tags="weight_anim")
                    break
            self.label.config(text=f"Paso {step+1}: {city1} → {city2}")
            self.after(900, self.animate_path, step+1)
        else:
            if self.path:
                self.label.config(text=f"Recorrido final: {' → '.join(self.path)} | Costo total: {self.cost}")
            else:
                self.label.config(text="No se encontró camino con Greedy")

class GreedyBacktrackVisualizer(tk.Toplevel):
    def __init__(self, master, path, cost, steps, title, start, goal):
        super().__init__(master)
        self.title(title)
        self.geometry("800x600")
        self.offset_x, self.offset_y = 30, 20
        self.positions = {
            'Arad': (60, 80), 'Zerind': (120, 40), 'Oradea': (180, 20), 'Sibiu': (200, 100),
            'Fagaras': (300, 80), 'Rimnicu Vilcea': (250, 160), 'Pitesti': (350, 160),
            'Timisoara': (40, 160), 'Lugoj': (80, 220), 'Mehadia': (120, 280), 'Drobeta': (80, 340),
            'Craiova': (220, 300), 'Bucharest': (500, 200), 'Giurgiu': (520, 260),
            'Urziceni': (520, 120), 'Hirsova': (600, 80), 'Eforie': (650, 60),
            'Vaslui': (600, 200), 'Iasi': (650, 240), 'Neamt': (700, 280)
        }
        self.positions = {city: (x + self.offset_x, y + self.offset_y) for city, (x, y) in self.positions.items()}
        self.canvas = tk.Canvas(self, width=800, height=520, bg="white")
        self.canvas.pack()
        self.label = tk.Label(self, text="", font=("Arial", 14))
        self.label.pack(pady=10)
        self.path = path
        self.cost = cost
        self.steps = steps
        self.start = start
        self.goal = goal
        self.draw_all_edges()
        self.draw_all_nodes()
        self.after(500, self.animate_steps, 0, [])

    def draw_all_edges(self):
        drawn = set()
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

    def draw_all_nodes(self, highlight=None, backtrack=None):
        for city, (x, y) in self.positions.items():
            color = "#ffd966" if self.path and city in self.path else "#bdbdbd"
            outline = "#1976d2" if city == self.start else ("#ff5252" if city == self.goal else "#616161")
            if highlight == city:
                outline = "#00c853"  # verde para avance
            if backtrack == city:
                outline = "#ff1744"  # rojo para retroceso
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill=color, outline=outline, width=3)
            self.canvas.create_text(x, y+25, text=city, font=("Arial", 13, "bold"), fill="#222")

    def animate_steps(self, step, current_path):
        self.canvas.delete("path_arrow")
        self.canvas.delete("weight_anim")
        if step < len(self.steps):
            city, action = self.steps[step]
            self.draw_all_edges()
            # Dibuja flecha si hay avance
            if action == 'forward' and len(current_path) > 0:
                prev_city = current_path[-1]
                x0, y0 = self.positions[prev_city]
                x1, y1 = self.positions[city]
                self.canvas.create_line(x0, y0, x1, y1, fill="#1976d2", width=5, arrow=tk.LAST, tags="path_arrow")
                # Dibuja el peso de la arista animada con fondo
                for neighbor, weight in romania_map[prev_city]:
                    if neighbor == city:
                        mx, my = (x0 + x1) // 2, (y0 + y1) // 2
                        self.canvas.create_rectangle(mx-15, my-10, mx+15, my+10, fill="#ffd966", outline="#1976d2", width=2, tags="weight_anim")
                        self.canvas.create_text(mx, my, text=str(weight), font=("Arial", 12, "bold"), fill="#1976d2", tags="weight_anim")
                        break
            if action == 'forward':
                current_path.append(city)
                self.draw_all_nodes(highlight=city)
                self.label.config(text=f"Avanza a {city}")
            else:
                # Retroceso: quitamos el último nodo (que debe ser city)
                if current_path and current_path[-1] == city:
                    current_path.pop()
                self.draw_all_nodes(backtrack=city)
                self.label.config(text=f"Retrocede desde {city} (retroceso)")
            self.after(900, self.animate_steps, step+1, current_path)
        else:
            self.draw_all_edges()
            self.draw_all_nodes()
            if self.path:
                self.label.config(text=f"Recorrido final: {' → '.join(self.path)} | Costo total: {self.cost}")
            else:
                self.label.config(text="No se encontró camino con Greedy + retroceso")
