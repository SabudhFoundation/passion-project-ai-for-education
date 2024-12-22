class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def solution(head):
    """
    Reverses a linked list and returns the head of the reversed list.

    Parameters:
        head (ListNode): Head node of the linked list.

    Returns:
        ListNode: Head node of the reversed linked list.
    """
    prev = None
    current = head
    
    # Traverse the linked list and reverse the pointers
    while current:
        next_node = current.next  # Save the next node
        current.next = prev       # Reverse the pointer
        prev = current            # Move prev forward
        current = next_node       # Move current forward
    
    # Prev will now be the head of the reversed list
    return prev

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
    # Example linked list
    values = [1, 2, 3, 4, 5]
    head = create_linked_list(values)
    
    print("Original Linked List:")
    print_linked_list(head)
    
    # Reverse the linked list
    reversed_head = reverse_linked_list(head)
    
    print("Reversed Linked List:")
    print_linked_list(reversed_head)
