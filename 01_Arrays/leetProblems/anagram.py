# Given two strings s and t, return true if the two strings are anagrams of each other, 
# otherwise return false.

# An anagram is a string that contains the exact same characters as another string, 
# but the order of the characters can be different.

def anagram(s: str,t:str)-> bool:
    if len(s)!=len(t):    #must be of same length
        return False
    
    # countS, countT = {}, {} #create an empty dictionary s=care t=race
    
    # for i in range(len(t)):
    #     countS[s[i]]= 1+countS.get(s[i],0)
    #     countT[t[i]]= 1+countT.get(t[i],0)
    # return countS==countT
    return sorted(s)==sorted(t)
        
s="car"
t="rac"
print(anagram(s,t))
    
    
    