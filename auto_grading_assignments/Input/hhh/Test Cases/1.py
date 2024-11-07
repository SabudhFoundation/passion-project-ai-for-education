def test_solution(solution):
    passed = []
    not_passed = []

    # Test case 1: Simple graph
    graph1 = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E']
    }
    expected1 = ['A', 'B', 'D', 'E', 'F', 'C']  # DFS starting from A
    if solution(graph1, 'A') == expected1:
        passed.append("Solution has passed test case with parameters graph1, 'A' and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph1, 'A' result " + str(expected1))

    # Test case 2: Graph with no edges
    graph2 = {
        'A': [],
        'B': [],
        'C': []
    }
    expected2 = ['A']  # DFS starting from A
    if solution(graph2, 'A') == expected2:
        passed.append("Solution has passed test case with parameters graph2, 'A' and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph2, 'A' result " + str(expected2))

    # Test case 3: Graph with cycles
    graph3 = {
        'A': ['B'],
        'B': ['C', 'A'],
        'C': ['D'],
        'D': ['B']
    }
    expected3 = ['A', 'B', 'C', 'D']  # DFS starting from A
    if solution(graph3, 'A') == expected3:
        passed.append("Solution has passed test case with parameters graph3, 'A' and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph3, 'A' result " + str(expected3))

    # Test case 4: Empty graph
    graph4 = {}
    expected4 = []  # DFS starting from any node in an empty graph
    if solution(graph4, 'A') == expected4:
        passed.append("Solution has passed test case with parameters graph4, 'A' and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph4, 'A' result " + str(expected4))

    return passed, not_passed