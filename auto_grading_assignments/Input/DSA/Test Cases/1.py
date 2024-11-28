def add_edge(self, u, v):
            if u not in self.graph:
                self.graph[u] = []
            if v not in self.graph:
                self.graph[v] = []
            self.graph[u].append(v)
            self.graph[v].append(u)  # For undirected graph

    # Test case 1: Basic BFS on a simple graph
    g1 = Graph()
    g1.add_edge(0, 1)
    g1.add_edge(0, 2)
    g1.add_edge(1, 3)
    g1.add_edge(1, 4)
    g1.add_edge(2, 5)
    expected_result1 = [0, 1, 2, 3, 4, 5]
    if solution(g1.graph, 0) == expected_result1:
        passed.append("Solution has passed test case 1 with expected result: " + str(expected_result1))
    else:
        not_passed.append("Solution has not passed test case 1 with expected result: " + str(expected_result1))

    # Test case 2: BFS on a disconnected graph
    g2 = Graph()
    g2.add_edge(0, 1)
    g2.add_edge(0, 2)
    g2.add_edge(3, 4)
    expected_result2 = [3, 4]  # Starting BFS from node 3
    if solution(g2.graph, 3) == expected_result2:
        passed.append("Solution has passed test case 2 with expected result: " + str(expected_result2))
    else:
        not_passed.append("Solution has not passed test case 2 with expected result: " + str(expected_result2))

    # Test case 3: BFS on a single node graph
    g3 = Graph()
    g3.add_edge(0, 0)  # Self-loop
    expected_result3 = [0]
    if solution(g3.graph, 0) == expected_result3:
        passed.append("Solution has passed test case 3 with expected result: " + str(expected_result3))
    else:
        not_passed.append("Solution has not passed test case 3 with expected result: " + str(expected_result3))

    # Test case 4: BFS on an empty graph
    g4 = Graph()
    expected_result4 = []  # No nodes to traverse
    if solution(g4.graph, 0) == expected_result4:
        passed.append("Solution has passed test case 4 with expected result: " + str(expected_result4))
    else:
        not_passed.append("Solution has not passed test case 4 with expected result: " + str(expected_result4))

    return passed, not_passed