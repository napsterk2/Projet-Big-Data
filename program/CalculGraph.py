
class GraphCalculation:

    def __init__(self, road_net_adjancy_matrix: [[int]]):
        self.matrix = road_net_adjancy_matrix

        self.result_graph_weight = self.calculation_graph_weight()
        self.result_graph_degree = self.calculation_graph_degree()
        self.result_nbr_edge = self.calculation_nbr_edge()

        print()
        print("=============== GRAPH ===============")
        print("The graph weight : " + str(self.result_graph_weight))
        print("The graph degree : " + str(self.result_graph_degree))
        print("The graph has " + str(self.result_nbr_edge) + " edges")
        print()

    def calculation_graph_weight(self):
        weight_graph = 0

        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if i != j:
                    weight_graph = self.matrix[i][j] + weight_graph

        weight_graph = weight_graph / 2
        return weight_graph

    def calculation_graph_degree(self):
        vertex_list = []

        for i in range(len(self.matrix)):
            vertex_degree = 0
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] != 0:
                    vertex_degree = vertex_degree + 1
            vertex_list.append(vertex_degree)

        vertex_list.sort()
        return vertex_list[0]

    def calculation_nbr_edge(self):
        nbr_edge = ((len(self.matrix) * (len(self.matrix) - 1)) / 2)
        return nbr_edge


