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
