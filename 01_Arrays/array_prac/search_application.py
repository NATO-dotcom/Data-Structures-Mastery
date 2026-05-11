# Time Complexity: O(n)
# Space Complexity: O(1)

arr = [1,2,3,4,5]
target = 30
found = False

#Linear search using traversal
for i in range(len(arr)):
    if arr[i] == target:
        found = True
        break
if found:
    print("Element Found!")
else:
    print("Element not Found!")