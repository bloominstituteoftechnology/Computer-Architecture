# Given a hashmap where the keys are integers, print out all of the values of the hashmap in reverse order, ordered by the keys.
# For example, given the following hashmap:

# The expected output is:
# widescreen
# views
# tissue
# coffee
# inbox
# vs code
# alloc
# bottle
# window
# since "widescreen" has the largest integer key, "views" has the second largest, etc.
# You may use whatever programming language you'd like.
# Verbalize your thought process as much as possible before writing any code. 
# Run through the UPER problem solving framework while going through your thought process.

numbers={
    14: "vs code",
    3: "window",
    9: "alloc",
    26: "views",
    4: "bottle",
    15: "inbox",
    79: "widescreen",
    16: "coffee",
    19: "tissue",
    }
# print(numbers)

reverse=sorted(numbers.items(),reverse=True)
print(reverse)

for value in reverse:
    print(value[1])