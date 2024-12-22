class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def solution(head1, head2):
    """
    Merges two sorted linked lists and returns the head of the merged sorted list.

    Parameters:
        head1 (ListNode): Head node of the first sorted linked list.
        head2 (ListNode): Head node of the second sorted linked list.

    Returns:
        ListNode: Head node of the merged sorted linked list.
    """
    # Dummy node to simplify merging process
    dummy = ListNode(-1)
    current = dummy
    
    # Traverse both lists and merge them in sorted order
    while head1 and head2:
        if head1.value < head2.value:
            current.next = head1
            head1 = head1.next
        else:
            current.next = head2
            head2 = head2.next
        current = current.next
    
    # Append any remaining nodes
    if head1:
        current.next = head1
    if head2:
        current.next = head2
    
    return dummy.next

# Helper function to create a linked list from a list of values
def create_linked_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for value in values[1:]:
        current.next = ListNode(value)
        current = current.next
    return head

# Helper function to print a linked list
def print_linked_list(head):
    while head:
        print(head.value, end=" -> ")
        head = head.next
    print("None")

# Example usage
if __name__ == "__main__":
    # Example linked lists
    list1 = create_linked_list([1, 3, 5])
    list2 = create_linked_list([2, 4, 6])
    
    # Merge lists
    merged_head = solution(list1, list2)
    
    # Print merged list
    print("Merged Linked List:")
    print_linked_list(merged_head)

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

    # Test Case 1: Merging two non-empty linked lists
    list1 = list_to_linked_list([1, 3, 5])
    list2 = list_to_linked_list([2, 4, 6])
    expected_result = [1, 2, 3, 4, 5, 6]
    if linked_list_to_list(solution(list1, list2)) == expected_result:
        passed.append("Solution has passed test case 1 with inputs [1, 3, 5] and [2, 4, 6]")
    else:
        not_passed.append("Solution has not passed test case 1 with inputs [1, 3, 5] and [2, 4, 6]")

    # Test Case 2: Merging one empty linked list with a non-empty linked list
    list1 = list_to_linked_list([])
    list2 = list_to_linked_list([1, 2, 3])
    expected_result = [1, 2, 3]
    if linked_list_to_list(solution(list1, list2)) == expected_result:
        passed.append("Solution has passed test case 2 with inputs [] and [1, 2, 3]")
    else:
        not_passed.append("Solution has not passed test case 2 with inputs [] and [1, 2, 3]")

    # Test Case 3: Merging two empty linked lists
    list1 = list_to_linked_list([])
    list2 = list_to_linked_list([])
    expected_result = []
    if linked_list_to_list(solution(list1, list2)) == expected_result:
        passed.append("Solution has passed test case 3 with inputs [] and []")
    else:
        not_passed.append("Solution has not passed test case 3 with inputs [] and []")

    # Test Case 4: Merging linked lists of different lengths
    list1 = list_to_linked_list([1, 3])
    list2 = list_to_linked_list([2, 4, 5, 6])
    expected_result = [1, 2, 3, 4, 5, 6]
    if linked_list_to_list(solution(list1, list2)) == expected_result:
        passed.append("Solution has passed test case 4 with inputs [1, 3] and [2, 4, 5, 6]")
    else:
        not_passed.append("Solution has not passed test case 4 with inputs [1, 3] and [2, 4, 5, 6]")

    return passed, not_passed