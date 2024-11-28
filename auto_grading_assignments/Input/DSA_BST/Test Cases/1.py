def __init__(self, value):
            self.value = value
            self.left = None
            self.right = None

    root = Node(10)
    if solution(root) == 1:
        passed.append("Solution has passed test case with a single node tree")
    else:
        not_passed.append("Solution has not passed test case with a single node tree, expected result 1")

    # Test case 3: Balanced tree
    root.left = Node(5)
    root.right = Node(15)
    if solution(root) == 2:
        passed.append("Solution has passed test case with a balanced tree")
    else:
        not_passed.append("Solution has not passed test case with a balanced tree, expected result 2")

    # Test case 4: Unbalanced tree (left-heavy)
    root.left.left = Node(3)
    if solution(root) == 3:
        passed.append("Solution has passed test case with an unbalanced left-heavy tree")
    else:
        not_passed.append("Solution has not passed test case with an unbalanced left-heavy tree, expected result 3")

    # Test case 5: Unbalanced tree (right-heavy)
    root.right.right = Node(20)
    if solution(root) == 3:
        passed.append("Solution has passed test case with an unbalanced right-heavy tree")
    else:
        not_passed.append("Solution has not passed test case with an unbalanced right-heavy tree, expected result 3")

    # Test case 6: More complex tree
    root.left.right = Node(7)
    if solution(root) == 3:
        passed.append("Solution has passed test case with a more complex tree")
    else:
        not_passed.append("Solution has not passed test case with a more complex tree, expected result 3")

    return passed, not_passed