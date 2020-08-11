# chapter 13 exercise 7

# exercise 2
def cumsum(nums):
    summed = []
    for num in range(len(nums)):
        summed.append(sum(nums[:num+1]))    
    return summed

print(cumsum([1,2,3]))

# exercise 10
def in_bisect(sortedWords, target):
    topIndex = len(sortedWords)-1
    bottomIndex = 0
    currentIndex = 0
    while(True):
        currentIndex = int((topIndex+bottomIndex)/2)
        if target < sortedWords[currentIndex]:
            topIndex = currentIndex - 1
        elif target > sortedWords[currentIndex]:
            bottomIndex = currentIndex + 1
        elif target == sortedWords[currentIndex]:
            return True
        if bottomIndex == topIndex and target != sortedWords[int((topIndex+bottomIndex)/2)]:
            break
    return False 

print(in_bisect(['aa', 'alien', 'allen', 'zymurgy'], 'Okay'))