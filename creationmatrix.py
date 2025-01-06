import networkx as nx
import matplotlib.pyplot as plt

class matrix:
    def __init__(self):
        self.matrix = []



    def CreateMat(self,p, t):
        # Create a matrix with p rows and t columns
        self.matrix = []
        for i in range(p):
            row = []
            for j in range(t):
                value = int(input(f"Enter element for row {i+1}, column {j+1}: "))
                row.append(value)
            self.matrix.append(row)
    
    
    def ShowMat(self):
        if not self.matrix:
            print("Matrix is empty. Please create a matrix first.")
        else:
            for row in self.matrix:
                print(' '.join(map(str, row)))
    
    def RdpSim(matrix1,matrix2):
        #creation of matrix C 
        row1,col1 = len(matrix1),len(matrix1[0])
        row2,col2 = len(matrix2),len(matrix2[0])
        if row1 != row2 or col1 != col2:
            print("Matrices must have the same dimensions for subtraction.")
        else:
            matrixC = []
            connections = []
            for i in range(row1):
                row = []
                for j in range(col1):
                    if matrix1[i][j] >= 0 and matrix2[i][j] >= 0 or matrix1[i][j]==matrix2[i][j]:
                        value=matrix1[i][j] - matrix2[i][j]
                        row.append(value)
                matrixC.append(row)
        return matrixC            

    def show_graph(connections):
        """Display the graph connections."""
        if not connections:
            print("No connections to display.")
        else:
            print("Graph Connections:")
            for conn in connections:
                print(f"{conn[0]} {('<->' if conn[2] == 'bidirectional' else '->')} {conn[1]}")

    def generate_graph(post_matrix, pre_matrix):
        """Generate graph connections based on post_matrix and pre_matrix."""
        rows = len(post_matrix)
        cols = len(post_matrix[0])
        connections = []

        for i in range(rows):
            for j in range(cols):
                result = post_matrix[i][j] - pre_matrix[i][j]
                if result == 0 and post_matrix[i][j] > 0 and pre_matrix[i][j] > 0:
                    # Bidirectional connection
                    connections.append(("p" + str(i+1), "t" + str(j+1), "bidirectional"))
                elif result == -1:
                    # Connection from p[i] to t[j]
                    connections.append(("p" + str(i+1), "t" + str(j+1), "forward"))
                elif result == 1:
                    # Connection from t[j] to p[i]
                    connections.append(("t" + str(j+1), "p" + str(i+1), "backward"))

        return connections
    

    def visualize_graph(connections):
        """Visualize the graph using networkx and matplotlib."""
        if not connections:
            print("No connections to visualize.")
            return

        # Create a directed graph
        graph = nx.DiGraph()

        # Add edges based on connections
        for conn in connections:
            if conn[2] == "bidirectional":
                graph.add_edge(conn[0], conn[1])
                graph.add_edge(conn[1], conn[0])
            else:
                graph.add_edge(conn[0], conn[1])

        # Draw the graph
        pos = nx.spring_layout(graph)  # Positioning of nodes
        nx.draw(graph, pos, with_labels=True, node_size=1500, node_color="lightblue", font_size=10, font_weight="bold")
        edge_labels = {(u, v): "->" for u, v in graph.edges}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
        plt.title("Graph Visualization")
        plt.show()


    def is_fireable(marking, pre_matrix, transition_index):
        """Check if a transition is fireable."""
        for place_index, tokens in enumerate(marking):
            if tokens < pre_matrix[place_index][transition_index]:
                return False
        return True

    @staticmethod
    def fire_transition(marking, pre_matrix, post_matrix, transition_index):
        """Fire a transition and update the marking."""
        print(f"Firing transition t{transition_index + 1}")
        new_marking = marking[:]
        for place_index in range(len(marking)):
            new_marking[place_index] -= pre_matrix[place_index][transition_index]
            new_marking[place_index] += post_matrix[place_index][transition_index]
        print(f"New marking: {new_marking}")
        return new_marking

    
    def RspSim(pre_matrix, post_matrix, initial_marking):
        """Simulate the evolution of the marking in a Petri net."""
        marking = initial_marking[:]
        marking_history = [marking[:]]  # Track all markings
        transitions = len(pre_matrix[0])  # Number of transitions

        print(f"Initial marking: {marking}")
    
        while True:
            fireable = False
            for t in range(transitions):
                if matrix.is_fireable(marking, pre_matrix, t):
                    print(f"Transition t{t + 1} is fireable")
                    marking = matrix.fire_transition(marking, pre_matrix, post_matrix, t)
                    marking_history.append(marking[:])
                    fireable = True
                    break  # Fire only one transition per iteration

            if not fireable:
                print("No more transitions can fire. Simulation ends.")
            break  # No transitions can fire, end simulation

        return marking_history

    
    def visualize_marking_evolution(marking_history):
        """Visualize the marking evolution."""
        print("\nMarking Evolution:")
        for step, marking in enumerate(marking_history):
            print(f"Step {step}: {marking}")


    def visualize_marking_graph(pre_matrix, post_matrix, marking_history):
        """
        Visualize the marking evolution as a directed graph.
        
        Nodes: Represent markings.
        Edges: Represent transitions between markings.
        """
        G = nx.DiGraph()  # Create a directed graph
        
        # Add nodes for each marking
        for step, marking in enumerate(marking_history):
            G.add_node(step, label=f"M{step}: {marking}")

        # Add edges between markings based on the simulation
        for i in range(len(marking_history) - 1):
            G.add_edge(i, i + 1, label=f"t{i + 1}")

        # Draw the graph
        pos = nx.spring_layout(G)  # Position the nodes
        labels = nx.get_node_attributes(G, 'label')

        # Draw nodes and labels
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color="lightgreen")
        nx.draw_networkx_labels(G, pos, labels)

        # Draw edges
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=15)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        # Display the graph
        plt.title("le graphe marquage : ")
        plt.axis('off')
        plt.show()