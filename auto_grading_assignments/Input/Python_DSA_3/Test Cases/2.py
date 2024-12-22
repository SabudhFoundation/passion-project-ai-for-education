def test_solution(solution):
    class ListNode:
        def __init__(self, value=0, next=None):
            self.value = value
            self.next = next

    def linked_list_to_list(head):
        result = []
        while head:
            result.append(head.value)
            head = head.next
        return result

    def list_to_linked_list(lst):
        if not lst:
            return None
        head = ListNode(lst[0])
        current = head
        for value in lst[1:]:
            current.next = ListNode(value)
            current = current.next
        return head

    # Test case 1: Normal case
    input_list = [1, 2, 3, 4, 5]
    expected_output = [5, 4, 3, 2, 1]
    head = list_to_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list) + " and expected result " + str(expected_output))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " result " + str(expected_output))

    # Test case 2: Single element
    input_list = [1]
    expected_output = [1]
    head = list_to_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list) + " and expected result " + str(expected_output))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " result " + str(expected_output))

    # Test case 3: Empty list
    input_list = []
    expected_output = []
    head = list_to_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list) + " and expected result " + str(expected_output))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " result " + str(expected_output))

    # Test case 4: Two elements
    input_list = [1, 2]
    expected_output = [2, 1]
    head = list_to_linked_list(input_list)
    if linked_list_to_list(solution(head)) == expected_output:
        passed.append("Solution has passed test case with input " + str(input_list) + " and expected result " + str(expected_output))
    else:
        not_passed.append("Solution has not passed test case with input " + str(input_list) + " result " + str(expected_output))

    return passed, not_passed