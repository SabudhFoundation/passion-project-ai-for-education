def test_solution(solution):
    passed = []
    not_passed = []
    
    # Test Case 1: Simple graph with direct path
    graph1 = {
        'A': {'B': 1, 'C': 4},
        'B': {'D': 2},
        'C': {},
        'D': {}
    }
    start1 = 'A'
    goal1 = 'D'
    expected1 = ['A', 'B', 'D']
    
    if solution(graph1, start1, goal1) == expected1:
        passed.append("Solution has passed test case with parameters graph1, start1, goal1 and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph1, start1, goal1 result " + str(expected1))
    
    # Test Case 2: Graph with no path
    graph2 = {
        'A': {'B': 1},
        'B': {'C': 1},
        'C': {}
    }
    start2 = 'A'
    goal2 = 'D'
    expected2 = None
    
    if solution(graph2, start2, goal2) == expected2:
        passed.append("Solution has passed test case with parameters graph2, start2, goal2 and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph2, start2, goal2 result " + str(expected2))
    
    # Test Case 3: Graph with multiple paths
    graph3 = {
        'A': {'B': 1, 'C': 2},
        'B': {'D': 2},
        'C': {'D': 1},
        'D': {}
    }
    start3 = 'A'
    goal3 = 'D'
    expected3 = ['A', 'C', 'D']  # Best path
    
    if solution(graph3, start3, goal3) == expected3:
        passed.append("Solution has passed test case with parameters graph3, start3, goal3 and expected result")
    else:
        not_passed.append("Solution has not passed test case with inputs graph3, start3, goal3 result " + str(expected3))
    
    return passed, not_passed