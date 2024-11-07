def test_solution(solution):
    passed = []
    not_passed = []

    # Test Case 1: Simple pathfinding
    start = (0, 0)
    goal = (1, 1)
    grid = [
        [0, 0],
        [0, 0]
    ]
    expected_answer = [(0, 0), (0, 1), (1, 1)]
    if solution(start, goal, grid) == expected_answer:
        passed.append("Solution has passed test case with parameters (0, 0), (1, 1) and expected result [(0, 0), (0, 1), (1, 1)]")
    else:
        not_passed.append("Solution has not passed test case with inputs (0, 0), (1, 1) result [(0, 0), (0, 1), (1, 1)]")

    # Test Case 2: No path available
    start = (0, 0)
    goal = (1, 1)
    grid = [
        [0, 1],
        [1, 0]
    ]
    expected_answer = []
    if solution(start, goal, grid) == expected_answer:
        passed.append("Solution has passed test case with parameters (0, 0), (1, 1) and expected result []")
    else:
        not_passed.append("Solution has not passed test case with inputs (0, 0), (1, 1) result []")

    # Test Case 3: Larger grid with a clear path
    start = (0, 0)
    goal = (2, 2)
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    expected_answer = [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]
    if solution(start, goal, grid) == expected_answer:
        passed.append("Solution has passed test case with parameters (0, 0), (2, 2) and expected result [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]")
    else:
        not_passed.append("Solution has not passed test case with inputs (0, 0), (2, 2) result [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)]")

    return passed, not_passed