#Visiting each element in an array starting form the last to first element
# Time Complexity: O(n)
# Space Complexity: O(1)


arr = [1,2,3,4,5]
print("Reversal Traversal:",end=" ")
for i in range(len(arr) - 1, -1, -1):
    print(arr[i],end=" ")
print()
