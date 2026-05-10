#Modifying elements of an array
arr = [10, 20, 30, 40, 50]

# Modifying elements using traversal (increasing each by 5)
for i in range(len(arr)):
    arr[i] += 5

# Print modified array
print("Modified array:", end=' ')
for num in arr:
    print(num, end=' ')
print()