# Given an integer array nums, return true if any value appears more than once in the array, otherwise return false.

def hasDuplicate(nums):
    found=set()
    for i in nums:
        if i in found:
            return True
        found.add(i)
    return False
nums=[1,2,3,4]
print(hasDuplicate(nums))