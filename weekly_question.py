dict_for_sum = {
                "cat": "bob",
                "dog": 23,
                19: 18,
                90: "fish"
                }

list_sum = []
# execute each one 
for i in dict_for_sum:
    # value is a number
    act_value = dict_for_sum[value]
    if type(act_value) == int:
        list_sum.append(value)
        print(list_sum)
result = sum(list_sum)
print(result)

