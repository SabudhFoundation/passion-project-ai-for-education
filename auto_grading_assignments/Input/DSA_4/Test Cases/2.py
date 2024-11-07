def test_solution(solution):
    passed = []
    not_passed = []

    # Test case 1: Basic functionality
    lru_cache = solution(2)  # Capacity of 2
    lru_cache.put(1, 1)
    lru_cache.put(2, 2)
    if lru_cache.get(1) == 1:
        passed.append("Solution has passed test case with parameters (2) and expected result 1")
    else:
        not_passed.append("Solution has not passed test case with inputs (2) result 1")

    # Test case 2: Eviction policy
    lru_cache.put(3, 3)  # Evicts key 2
    if lru_cache.get(2) == -1:
        passed.append("Solution has passed test case with parameters (3) and expected result -1")
    else:
        not_passed.append("Solution has not passed test case with inputs (3) result -1")

    # Test case 3: Update existing key
    lru_cache.put(1, 10)  # Update key 1
    if lru_cache.get(1) == 10:
        passed.append("Solution has passed test case with parameters (1, 10) and expected result 10")
    else:
        not_passed.append("Solution has not passed test case with inputs (1, 10) result 10")

    # Test case 4: Capacity limit
    lru_cache.put(4, 4)  # Evicts key 3
    if lru_cache.get(3) == -1:
        passed.append("Solution has passed test case with parameters (4) and expected result -1")
    else:
        not_passed.append("Solution has not passed test case with inputs (4) result -1")

    # Test case 5: Check order of eviction
    lru_cache.put(5, 5)  # Evicts key 1
    if lru_cache.get(1) == -1:
        passed.append("Solution has passed test case with parameters (5) and expected result -1")
    else:
        not_passed.append("Solution has not passed test case with inputs (5) result -1")

    return passed, not_passed