def test_solution(solution):
    class ListNode:
        def __init__(self, value=0, next=None):
            self.value = value
            self.next = next

    def linked_list_to_list(node):
        result = []
        while node:
            result.append(node.value)
            node = node.next
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

    passed = []
    not_passed = []

    # Test case 1: Merging two non-empty linked lists
    list1 = list_to_linked_list([1, 3, 5])
    list2 = list_to_linked_list([2, 4, 6])
    expected_result = [1, 2, 3, 4, 5, 6]
    if linked_list_to_list(solution(list1, list2)) == expected_result:
        passed.append("Solution has passed test case 1 with parameters [1, 3, 5] and [2, 4, 6]")
    else:
        not_passed.append("Solution has not passed test case 1 with inputs [1, 3, 5] and [2, 4, 6]")

    # Test case 2: Merging one empty linked list with a non-empty linked list
    list1 = list_to_linked_list([])
    list2 = list_to_linked_list([1, 2, 3])
    expected_result = [1, 2, 3]
    if linked_list_to_list(solution(list1, list2)) == expected_result:
        passed.append("Solution has passed test case 2 with parameters [] and [1, 2, 3]")
    else:
        not_passed.append("Solution has not passed test case 2 with inputs [] and [1, 2, 3]")

    # Test case 3: Merging two empty linked lists
    list1 = list_to_linked_list([])
    list2 = list_to_linked_list([])
    expected_result = []
    if linked_list_to_list(solution(list1, list2)) == expected_result:
        passed.append("Solution has passed test case 3 with parameters [] and []")
    else:
        not_passed.append("Solution has not passed test case 3 with inputs [] and []")

    # Test case 4: Merging linked lists of different lengths
    list1 = list_to_linked_list([1, 3])
    list2 = list_to_linked_list([2, 4, 5, 6])
    expected_result = [1, 2, 3, 4, 5, 6]
    if linked_list_to_list(solution(list1, list2)) == expected_result:
        passed.append("Solution has passed test case 4 with parameters [1, 3] and [2, 4, 5, 6]")
    else:
        not_passed.append("Solution has not passed test case 4 with inputs [1, 3] and [2, 4, 5, 6]")

    return passed, not_passed