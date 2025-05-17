import tkinter as tk
import random

romania_map = {
    'Arad': [('Zerind', 75), ('Sibiu', 140), ('Timisoara', 118)],
    'Zerind': [('Arad', 75), ('Oradea', 71)],
    'Oradea': [('Zerind', 71), ('Sibiu', 151)],
    'Sibiu': [('Arad', 140), ('Oradea', 151), ('Fagaras', 99), ('Rimnicu Vilcea', 80)],
    'Fagaras': [('Sibiu', 99), ('Bucharest', 211)],
    'Rimnicu Vilcea': [('Sibiu', 80), ('Pitesti', 97), ('Craiova', 146)],
    'Pitesti': [('Rimnicu Vilcea', 97), ('Craiova', 138), ('Bucharest', 101)],
    'Timisoara': [('Arad', 118), ('Lugoj', 111)],
    'Lugoj': [('Timisoara', 111), ('Mehadia', 70)],
    'Mehadia': [('Lugoj', 70), ('Drobeta', 75)],
    'Drobeta': [('Mehadia', 75), ('Craiova', 120)],
    'Craiova': [('Drobeta', 120), ('Rimnicu Vilcea', 146), ('Pitesti', 138)],
    'Bucharest': [('Fagaras', 211), ('Pitesti', 101), ('Giurgiu', 90), ('Urziceni', 85)],
    'Giurgiu': [('Bucharest', 90)],
    'Urziceni': [('Bucharest', 85), ('Hirsova', 98), ('Vaslui', 142)],
    'Hirsova': [('Urziceni', 98), ('Eforie', 86)],
    'Eforie': [('Hirsova', 86)],
    'Vaslui': [('Urziceni', 142), ('Iasi', 92)],
    'Iasi': [('Vaslui', 92), ('Neamt', 87)],
    'Neamt': [('Iasi', 87)]
}

heuristics = {
    'Arad': 366, 'Bucharest': 0, 'Craiova': 160, 'Drobeta': 242, 'Eforie': 161, 'Fagaras': 176,
    'Giurgiu': 77, 'Hirsova': 151, 'Iasi': 226, 'Lugoj': 244, 'Mehadia': 241, 'Neamt': 234,
    'Oradea': 380, 'Pitesti': 100, 'Rimnicu Vilcea': 193, 'Sibiu': 253, 'Timisoara': 329,
    'Urziceni': 80, 'Vaslui': 199, 'Zerind': 374
}

class HillClimbingVisualizer(tk.Toplevel):
    def __init__(self, master, path, title, start, goal):
        super().__init__(master)
        self.title(title)
        self.geometry("800x600")
        self.canvas = tk.Canvas(self, width=800, height=520, bg="white")
        self.canvas.pack()
        self.label = tk.Label(self, text="", font=("Arial", 14))
        self.label.pack(pady=10)
        self.path = path
        self.start = start
        self.goal = goal
        self.positions = {
            'Arad': (60, 80), 'Zerind': (120, 40), 'Oradea': (180, 20), 'Sibiu': (200, 100),
            'Fagaras': (300, 80), 'Rimnicu Vilcea': (250, 160), 'Pitesti': (350, 160),
            'Timisoara': (40, 160), 'Lugoj': (80, 220), 'Mehadia': (120, 280), 'Drobeta': (80, 340),
            'Craiova': (220, 300), 'Bucharest': (500, 200), 'Giurgiu': (520, 260),
            'Urziceni': (520, 120), 'Hirsova': (600, 80), 'Eforie': (650, 60),
            'Vaslui': (600, 200), 'Iasi': (650, 240), 'Neamt': (700, 280)
        }
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
                # Fondo para el peso
                rect = self.canvas.create_rectangle(mx-15, my-10, mx+15, my+10, fill="#fff", outline="#1976d2", width=1)
                self.canvas.create_text(mx, my, text=str(weight), font=("Arial", 10, "bold"), fill="#1976d2")

    def draw_all_nodes(self):
        for city, (x, y) in self.positions.items():
            color = "#ffd966" if city in self.path else "#bdbdbd"
            outline = "#1976d2" if city == self.start else ("#ff5252" if city == self.goal else "#616161")
            self.canvas.create_oval(x-18, y-18, x+18, y+18, fill=color, outline=outline, width=3)
            self.canvas.create_text(x, y+25, text=city, font=("Arial", 13, "bold"), fill="#222")

    def animate_path(self, step):
        self.canvas.delete("path_arrow")
        self.canvas.delete("weight_anim")
        if step < len(self.path)-1:
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
            self.label.config(text=f"Recorrido final: {' → '.join(self.path)}")

def hill_climbing(start, goal):
    current = start
    path = [current]
    while current != goal:
        neighbors = romania_map[current]
        # Elige el vecino con menor heurística
        next_city = min(neighbors, key=lambda x: heuristics[x[0]])[0]
        if heuristics[next_city] >= heuristics[current]:
            break  # No hay mejora, se estanca
        current = next_city
        path.append(current)
    return path
