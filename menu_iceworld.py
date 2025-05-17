import tkinter as tk
from tkinter import messagebox
from iceworld_core import IceWorld, bfs, dfs, GridVisualizer
from iceworld_core import TreeVisualizer

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

root = tk.Tk()
root.title("Menú Principal - Ice World")
root.geometry("400x300")

label = tk.Label(root, text="Elige una opción de juego:", font=("Arial", 16))
label.pack(pady=30)

btn_bfs = tk.Button(root, text="Jugar Ice World (BFS)", font=("Arial", 14), width=25, command=jugar_bfs)
btn_bfs.pack(pady=10)

btn_dfs = tk.Button(root, text="Jugar Ice World (DFS)", font=("Arial", 14), width=25, command=jugar_dfs)
btn_dfs.pack(pady=10)

root.mainloop()
