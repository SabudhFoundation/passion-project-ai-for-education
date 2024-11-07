def test_solution(solution):
    passed = []
    not_passed = []

    # Test Case 1
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'D': 2, 'E': 5},
        'C': {'A': 4, 'D': 1},
        'D': {'B': 2, 'C': 1, 'E': 3},
        'E': {'B': 5, 'D': 3}
    }
    start = 'A'
    goal = 'E'
    expected_answer = ['A', 'B', 'D', 'E']
    if solution(graph, start, goal) == expected_answer:
        passed.append("Solution has passed test case with parameters graph, start='A', goal='E' and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph, start='A', goal='E' result " + str(expected_answer))

    # Test Case 2
    graph = {
        'A': {'B': 2, 'C': 1},
        'B': {'A': 2, 'D': 3},
        'C': {'A': 1, 'D': 4},
        'D': {'B': 3, 'C': 4}
    }
    start = 'A'
    goal = 'D'
    expected_answer = ['A', 'C', 'D']
    if solution(graph, start, goal) == expected_answer:
        passed.append("Solution has passed test case with parameters graph, start='A', goal='D' and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph, start='A', goal='D' result " + str(expected_answer))

    # Test Case 3
    graph = {
        'A': {'B': 1},
        'B': {'A': 1, 'C': 2},
        'C': {'B': 2}
    }
    start = 'A'
    goal = 'C'
    expected_answer = ['A', 'B', 'C']
    if solution(graph, start, goal) == expected_answer:
        passed.append("Solution has passed test case with parameters graph, start='A', goal='C' and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph, start='A', goal='C' result " + str(expected_answer))

    return passed, not_passed