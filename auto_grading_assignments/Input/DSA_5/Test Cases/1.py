def test_solution():
    cache = LRUCache(2)

    # Test case 1: Adding elements to the cache
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1  # returns 1
    assert cache.get(2) == 2  # returns 2

    # Test case 2: Cache eviction
    cache.put(3, 3)  # evicts key 2
    assert cache.get(2) == -1  # returns -1 (not found)

    # Test case 3: Updating existing key
    cache.put(1, 10)  # updates key 1
    assert cache.get(1) == 10  # returns 10

    # Test case 4: Adding more elements than capacity
    cache.put(4, 4)  # evicts key 3
    assert cache.get(3) == -1  # returns -1 (not found)
    assert cache.get(4) == 4  # returns 4

    # Test case 5: Order of elements
    cache.put(5, 5)  # evicts key 1
    assert cache.get(1) == -1  # returns -1 (not found)
    assert cache.get(5) == 5  # returns 5

    print("All test cases passed!")

test_solution()