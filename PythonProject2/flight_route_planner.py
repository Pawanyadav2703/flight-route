import heapq
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
from tkinter import messagebox, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Dijkstra's algorithm to calculate the shortest path
def dijkstra(graph, start):
    queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    return distances, previous_nodes


# Function to calculate the shortest path between two cities
def shortest_path(graph, start, end):
    distances, previous_nodes = dijkstra(graph, start)
    path = []
    step = end

    while step:
        path.append(step)
        step = previous_nodes[step]

    path.reverse()
    return path, distances[end]


# Function to handle the button click for the shortest path calculation
def calculate_shortest_path():
    if start_city.get() == "Select Start City" or end_city.get() == "Select End City":
        messagebox.showerror("Invalid Input", "Please select both start and end cities.")
        return

    start = start_city.get()
    end = end_city.get()

    path, cost = shortest_path(graph, start, end)
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Shortest path from {start} to {end}:\n")
    result_text.insert(tk.END, " → ".join(path) + "\n")
    result_text.insert(tk.END, f"Total cost: {cost}")
    result_text.config(state=tk.DISABLED)

    # Visualization
    visualize_path(start, end, path)


def visualize_path(start, end, path):
    # Clear previous visualization
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Create NetworkX graph
    G = nx.Graph()

    # Add edges with weights to the graph
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)

    # Create figure
    fig = plt.figure(figsize=(8, 6), dpi=100)
    ax = fig.add_subplot(111)

    # Position nodes using spring layout
    pos = nx.spring_layout(G, k=0.5, iterations=50)

    # Draw all nodes and edges
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=1, ax=ax)

    # Highlight the path
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', node_size=800, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3, ax=ax)

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

    # Add title
    ax.set_title(f"Shortest Path from {start} to {end}", fontsize=12)
    plt.tight_layout()

    # Embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add toolbar (optional)
    # toolbar = NavigationToolbar2Tk(canvas, graph_frame)
    # toolbar.update()
    # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


def clear_selections():
    start_city.set("Select Start City")
    end_city.set("Select End City")
    result_text.config(state=tk.NORMAL)
    result_text.delete(1.0, tk.END)
    result_text.config(state=tk.DISABLED)
    for widget in graph_frame.winfo_children():
        widget.destroy()


# Example graph representing cities and flight costs
graph = {
    'New York': {'Chicago': 719, 'Toronto': 470, 'Boston': 215, 'Washington': 227},
    'Chicago': {'New York': 719, 'Denver': 1003, 'Toronto': 525},
    'Toronto': {'New York': 470, 'Chicago': 525, 'Boston': 550},
    'Boston': {'New York': 215, 'Toronto': 550, 'Washington': 442},
    'Washington': {'New York': 227, 'Boston': 442, 'Miami': 923},
    'Denver': {'Chicago': 1003, 'Phoenix': 853, 'Dallas': 792},
    'Dallas': {'Denver': 792, 'Phoenix': 887, 'Houston': 239},
    'Houston': {'Dallas': 239, 'Miami': 1187},
    'Miami': {'Washington': 923, 'Houston': 1187, 'Atlanta': 661},
    'Atlanta': {'Miami': 661, 'Phoenix': 1589},
    'Phoenix': {'Denver': 853, 'Dallas': 887, 'Atlanta': 1589, 'Los Angeles': 373},
    'Los Angeles': {'Phoenix': 373, 'San Francisco': 382},
    'San Francisco': {'Los Angeles': 382, 'Seattle': 808},
    'Seattle': {'San Francisco': 808, 'Denver': 1306}
}

# Create the main window
root = tk.Tk()
root.title("Flight Route Planner")
root.geometry("1000x800")
root.configure(bg='#f0f0f0')

# Style configuration
style = ttk.Style()
style.configure('TFrame', background='#f0f0f0')
style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10), padding=5)
style.configure('TCombobox', font=('Arial', 10), padding=5)

# Main container
main_frame = ttk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Control panel
control_frame = ttk.Frame(main_frame)
control_frame.pack(fill=tk.X, pady=10)

# City selection
cities = sorted(graph.keys())

start_label = ttk.Label(control_frame, text="Departure City:")
start_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
start_city = tk.StringVar(value="Select Start City")
start_menu = ttk.Combobox(control_frame, textvariable=start_city, values=cities, state="readonly")
start_menu.grid(row=0, column=1, padx=5, pady=5)

end_label = ttk.Label(control_frame, text="Destination City:")
end_label.grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
end_city = tk.StringVar(value="Select End City")
end_menu = ttk.Combobox(control_frame, textvariable=end_city, values=cities, state="readonly")
end_menu.grid(row=0, column=3, padx=5, pady=5)

# Buttons
button_frame = ttk.Frame(control_frame)
button_frame.grid(row=0, column=4, padx=10)

calculate_btn = ttk.Button(button_frame, text="Find Route", command=calculate_shortest_path)
calculate_btn.pack(side=tk.LEFT, padx=5)

clear_btn = ttk.Button(button_frame, text="Clear", command=clear_selections)
clear_btn.pack(side=tk.LEFT, padx=5)

# Result display
result_frame = ttk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True, pady=10)

result_label = ttk.Label(result_frame, text="Route Information:", font=('Arial', 11, 'bold'))
result_label.pack(anchor=tk.W)

result_text = tk.Text(result_frame, height=4, width=80, wrap=tk.WORD, font=('Arial', 10))
result_text.pack(fill=tk.BOTH, expand=True, pady=5)
result_text.config(state=tk.DISABLED)

# Graph visualization
graph_frame = ttk.Frame(main_frame)
graph_frame.pack(fill=tk.BOTH, expand=True)
graph_label = ttk.Label(graph_frame, text="Route Visualization:", font=('Arial', 11, 'bold'))
graph_label.pack(anchor=tk.W)

# Initial empty plot
fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
ax.text(0.5, 0.5, "Select cities and click 'Find Route' to visualize the path",
        ha='center', va='center', fontsize=12, color='gray')
ax.axis('off')
plt.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Run the main loop
root.mainloop()