def linked_list_to_list(head):
        result = []
        current = head
        while current:
            result.append(current.value)
            current = current.next
        return result

    # Test case 1: Normal case
    input_list = [1, 2, 3, 4, 5]
    expected_output = [5, 4, 3, 2, 1]
    head = create_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " expected " + str(expected_output))

    # Test case 2: Empty list
    input_list = []
    expected_output = []
    head = create_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " expected " + str(expected_output))

    # Test case 3: Single element list
    input_list = [1]
    expected_output = [1]
    head = create_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " expected " + str(expected_output))

    # Test case 4: Two elements list
    input_list = [1, 2]
    expected_output = [2, 1]
    head = create_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " expected " + str(expected_output))

    # Test case 5: List with duplicate values
    input_list = [1, 2, 2, 1]
    expected_output = [1, 2, 2, 1]
    head = create_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " expected " + str(expected_output))

    return passed, not_passed