# Problems for each of the days of build week.

# Find which contains dupes and if so, return True, else, return False

## Working solution for duplicates
def containsDuplicate(nums):
    if len(nums) == len(set(nums)):
        return(False)
    else:
        return(True)


if __name__ == "__main__":
    print(containsDuplicate([1,2,3,4,5]))
    print(containsDuplicate([1,2,3,4,5,5]))
    print(containsDuplicate([1,2,3,4,5,6,7,8,9]))
    print(containsDuplicate([1,2,3,4,5,5,5,5,5,5,5,5]))
    print(containsDuplicate([1,2,3,4,5,9,10,11,11,23]))
    print(containsDuplicate([1,2,3,4,5,6,10]))