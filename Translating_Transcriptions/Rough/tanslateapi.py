class Node:
    def __init__(self, val, next=None, prev=None):
        self.val = val
        self.next = next
        self.prev = prev

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = None
        self.hash = {}
        self.contains = 0
    
    def lru_add(self, key):
        new_node = Node(val=key)
        if not self.cache:
            self.cache = new_node
        else:
            temp = self.cache
            while temp.next:
                temp = temp.next
            temp.next = new_node
            new_node.prev = temp
        
    def lru_shift(self, key):
        temp = self.cache
        while temp.val != key:
            temp = temp.next
        if temp.next:
            if temp.prev is None:
                self.cache = self.cache.next
                self.cache.prev = None
            else:
                temp.prev.next = temp.next
            start = temp.next
            while start.next:
                start = start.next
            new_node = Node(val=key)
            start.next = new_node
            new_node.prev = start
        
    def get(self, key: int) -> int:
        if key in self.hash:
            self.lru_shift(key)
            return self.hash[key]
        else:
            return -1
    
    def print_cache(self):
        temp = self.cache
        result = []
        while temp:
            result.append(str(temp.val))
            temp = temp.next
        print(" --> ".join(result) + " --> None")

    def put(self, key: int, value: int) -> None:
        if key in self.hash:
            self.hash[key] = value
            self.lru_shift(key)
        elif self.contains < self.capacity:
            self.hash[key] = value
            self.contains += 1
            # Insert into LL Cache
            self.lru_add(key)
        else:
            lru = self.cache.val
            if lru in self.hash:
              del self.hash[lru]
            self.cache = self.cache.next
            if self.cache:
                self.cache.prev = None
            self.lru_add(key)                        
            self.hash[key] = value

# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)

def test_lru_cache():
    # Inputs
    operations = ["LRUCache","put","put","put","put","put","get","put","get","get","put","get","put","put","put","get","put","get","get","get","get","put","put","get","get","get","put","put","get","put","get","put","get","get","get","put","put","put","get","put","get","get","put","put","get","put","put","put","put","get","put","put","get","put","put","get","put","put","put","put","put","get","put","put","get","put","get","get","get","put","get","get","put","put","put","put","get","put","put","put","put","get","get","get","put","put","put","get","put","put","put","get","put","put","put","get","get","get","put","put","put","put","get","put","put","put","put","put","put","put"]
    arguments = [[10],[10,13],[3,17],[6,11],[10,5],[9,10],[13],[2,19],[2],[3],[5,25],[8],[9,22],[5,5],[1,30],[11],[9,12],[7],[5],[8],[9],[4,30],[9,3],[9],[10],[10],[6,14],[3,1],[3],[10,11],[8],[2,14],[1],[5],[4],[11,4],[12,24],[5,18],[13],[7,23],[8],[12],[3,27],[2,12],[5],[2,9],[13,4],[8,18],[1,7],[6],[9,29],[8,21],[5],[6,30],[1,12],[10],[4,15],[7,22],[11,26],[8,17],[9,29],[5],[3,4],[11,30],[12],[4,29],[3],[9],[6],[3,4],[1],[10],[3,29],[10,28],[1,20],[11,13],[3],[3,12],[3,8],[10,9],[3,26],[8],[7],[5],[13,17],[2,27],[11,15],[12],[9,19],[2,15],[3,16],[1],[12,17],[9,1],[6,19],[4],[5],[5],[8,1],[11,7],[5,2],[9,28],[1],[2,2],[7,4],[4,22],[7,24],[9,26],[13,28],[11,26]]
    
    # Initialize cache and results list
    results = []
    cache = None
    
    for operation, args in zip(operations, arguments):
        if operation == "LRUCache":
            cache = LRUCache(*args)
            results.append(None)  # Initialization doesn't return a value
        elif operation == "put":
            cache.put(*args)
            results.append(None)  # put operation doesn't return a value
        elif operation == "get":
            result = cache.get(*args)
            results.append(result)  # Collect the result for get operation
        print(f"Success: {operation}:{args} ")
        cache.print_cache()
    
    return results

# Run the test function and print the results
test_output = test_lru_cache()
print(test_output)
