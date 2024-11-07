def test_solution(solution):
    passed = []
    not_passed = []

    # Test case 1: Solve for 1 queen
    expected_answer_1 = [[0]]
    if solution(1) == expected_answer_1:
        passed.append("Solution has passed test case with parameters (1) and expected result [[0]]")
    else:
        not_passed.append("Solution has not passed test case with inputs (1) result " + str(solution(1)) + " expected " + str(expected_answer_1))

    # Test case 2: Solve for 4 queens
    expected_answer_2 = [[1, 3, 0, 2], [2, 0, 3, 1]]  # Two valid solutions for 4 queens
    result_2 = solution(4)
    if sorted(result_2) == sorted(expected_answer_2):
        passed.append("Solution has passed test case with parameters (4) and expected result [[1, 3, 0, 2], [2, 0, 3, 1]]")
    else:
        not_passed.append("Solution has not passed test case with inputs (4) result " + str(result_2) + " expected " + str(expected_answer_2))

    # Test case 3: Solve for 8 queens
    result_3 = solution(8)
    if len(result_3) > 0:  # Expecting at least one solution
        passed.append("Solution has passed test case with parameters (8) and returned a non-empty result")
    else:
        not_passed.append("Solution has not passed test case with inputs (8) result " + str(result_3) + " expected non-empty result")

    # Test case 4: Solve for 0 queens
    expected_answer_4 = [[]]  # One way to place 0 queens
    if solution(0) == expected_answer_4:
        passed.append("Solution has passed test case with parameters (0) and expected result [[]]")
    else:
        not_passed.append("Solution has not passed test case with inputs (0) result " + str(solution(0)) + " expected " + str(expected_answer_4))

    return passed, not_passed