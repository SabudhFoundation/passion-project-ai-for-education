def test_solution(solution):
    passed = []
    not_passed = []

    # Test case 1: Simple graph
    graph1 = {
        0: [1, 2],
        1: [0, 3],
        2: [0],
        3: [1]
    }
    expected_result1 = [0, 1, 3, 2]  # DFS starting from node 0
    if solution(graph1, 0) == expected_result1:
        passed.append("Solution has passed test case 1 with parameters graph1, 0 and expected result")
    else:
        not_passed.append("Solution has not passed test case 1 with inputs graph1, 0 result " + str(expected_result1))

    # Test case 2: Graph with a cycle
    graph2 = {
        0: [1],
        1: [2],
        2: [0, 3],
        3: []
    }
    expected_result2 = [0, 1, 2, 3]  # DFS starting from node 0
    if solution(graph2, 0) == expected_result2:
        passed.append("Solution has passed test case 2 with parameters graph2, 0 and expected result")
    else:
        not_passed.append("Solution has not passed test case 2 with inputs graph2, 0 result " + str(expected_result2))

    # Test case 3: Disconnected graph
    graph3 = {
        0: [1],
        1: [0],
        2: [3],
        3: [2]
    }
    expected_result3 = [0, 1]  # DFS starting from node 0
    if solution(graph3, 0) == expected_result3:
        passed.append("Solution has passed test case 3 with parameters graph3, 0 and expected result")
    else:
        not_passed.append("Solution has not passed test case 3 with inputs graph3, 0 result " + str(expected_result3))

    # Test case 4: Empty graph
    graph4 = {}
    expected_result4 = []  # DFS starting from any node should return empty
    if solution(graph4, 0) == expected_result4:
        passed.append("Solution has passed test case 4 with parameters graph4, 0 and expected result")
    else:
        not_passed.append("Solution has not passed test case 4 with inputs graph4, 0 result " + str(expected_result4))

    # Test case 5: Single node graph
    graph5 = {
        0: []
    }
    expected_result5 = [0]  # DFS starting from node 0
    if solution(graph5, 0) == expected_result5:
        passed.append("Solution has passed test case 5 with parameters graph5, 0 and expected result")
    else:
        not_passed.append("Solution has not passed test case 5 with inputs graph5, 0 result " + str(expected_result5))

    return passed, not_passed