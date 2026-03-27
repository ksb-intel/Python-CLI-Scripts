### lists

num1 = 65
print(num1)

nums = [45, 87, 21, 24, 99]
print(nums)

print(nums[-4])

### slicing - printing a specific section of a list
print(nums[2:4])

## Lists also work with strings
names = ['katie', 'parker', 'john']
print(names)

## Mix - can have different types of data in one list: integars, characters
mix = ['katie', 21, 3.21]
print(mix)

### you can combine two lists
mix = [ nums, names ]
print(mix)
len(mix)
print(len(mix))

print(mix[1][2])

### nums. to a list adds functions to the list
nums.append(33)
print(nums)

print(nums.count(33))

nums.remove(99)
print(nums)

### stack follows pop will remove last in first out
nums.pop(4)
print(nums)

del nums [2:4]
print(nums)

### insert values by using append and insert .extend adds multiple values
nums.extend([99, 43, 50, 11, 21])
print(nums)

## want to replace 99 and 43 with 54 and 76.
nums[2:4] = [54, 76]
print(nums)

### nums.reverse reverses a list
nums.reverse()
print(nums)

### we can sort the list by value
nums.sort()
print(nums)

## min and max
min(nums)
max(nums)
print(min(nums))
print(max(nums))

### avg
avg = sum(nums)/len(nums)
print(avg)

### task to guess the output

a = [33, 76, 24, 56]
b = ["james" , "tony" , "kieran"]

print((a[:2] + b[1:])[-3])

### guess: 76