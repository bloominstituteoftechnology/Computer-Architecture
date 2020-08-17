obj = {
  "cat": "bob",
  "dog": 23,
  19: 18,
  90: "fish"
}

ans = 0
for keys, value in obj.items():
    if type(value) == int:
        ans += value

print(ans)