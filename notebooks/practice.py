"""
Print out all of the strings in the following array in alphabetical order, each on a separate line.
['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot', 'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']
The expected output is:
'Cha Cha'
'Foxtrot'
'Jive'
'Paso Doble'
'Rumba'
'Samba'
'Tango'
'Viennese Waltz'
'Waltz'
You may use whatever programming language you'd like.
Verbalize your thought process as much as possible before writing any code. Run through the UPER problem solving framework while going through your thought process.

"""


line = ['Waltz', 'Tango', 'Viennese Waltz', 'Foxtrot',
        'Cha Cha', 'Samba', 'Rumba', 'Paso Doble', 'Jive']

line.sort()  # (n log(n))
# Python timsort
# use the built in function
# always (n log(n))
# Bubble Sort 0(n^2)
# Mergesort
# 2-3 challenges.
for i in line:
    print(i)
