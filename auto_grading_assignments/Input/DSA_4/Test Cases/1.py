def test_solution(solution):
    passed = []
    not_passed = []

    # Test case 1: Reverse a linked list with multiple elements
    linked_list_1 = [1, 2, 3, 4, 5]
    expected_result_1 = [5, 4, 3, 2, 1]
    if solution(linked_list_1) == expected_result_1:
        passed.append("Solution has passed test case with input [1, 2, 3, 4, 5] and expected result [5, 4, 3, 2, 1]")
    else:
        not_passed.append("Solution has not passed test case with input [1, 2, 3, 4, 5] result [5, 4, 3, 2, 1]")

    # Test case 2: Reverse a linked list with a single element
    linked_list_2 = [1]
    expected_result_2 = [1]
    if solution(linked_list_2) == expected_result_2:
        passed.append("Solution has passed test case with input [1] and expected result [1]")
    else:
        not_passed.append("Solution has not passed test case with input [1] result [1]")

    # Test case 3: Reverse an empty linked list
    linked_list_3 = []
    expected_result_3 = []
    if solution(linked_list_3) == expected_result_3:
        passed.append("Solution has passed test case with input [] and expected result []")
    else:
        not_passed.append("Solution has not passed test case with input [] result []")

    # Test case 4: Reverse a linked list with duplicate elements
    linked_list_4 = [1, 2, 2, 3, 3]
    expected_result_4 = [3, 3, 2, 2, 1]
    if solution(linked_list_4) == expected_result_4:
        passed.append("Solution has passed test case with input [1, 2, 2, 3, 3] and expected result [3, 3, 2, 2, 1]")
    else:
        not_passed.append("Solution has not passed test case with input [1, 2, 2, 3, 3] result [3, 3, 2, 2, 1]")

    return passed, not_passed