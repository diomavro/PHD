import itertools
from itertools import product
import random
import tkinter as tk

def union(A,B):
    k = set(A)
    for i in B:
        k.add(i)
    return k
def intersection(A,B):
    k = set()
    for i in A:
        if i in B:
            k.add(i)
            print(k)
    return k

#checking if functions work
# A = {1,2,3}
# B = {1,2,4}
# print(A)
# assert( union(A,B)== {1,2,3,4} )
# print(A)
# assert( intersection(A,B) == {1,2} )

#takes in the whole space and a set in the space
#returns complement of the set
def complement(A,U):
    k = set()
    for i in U: 
        if i not in A:
            k.add(i)
     return k 


#Give three sets, A, B and U
#Second return all elements in U which are not in A and B
def complement_of_union(A, B, U):
    # inputs: A, B and U are of type 'set'
    # output: a tuple of the type (set, set)
    k = A
    for i in B:
        k.add(i)
    kc = set()
    for j in U:
        if j not in k:
            kc.add(j)
    return kc

#check if function works
# A = {1, 2, 3, 4, 5}
# B = {0, 2, -6, 5, 8, 9}
# U = A|B|{-3, 7, 10, -4}
# assert( complement_of_union(A, B, U) == {-4, -3, 7, 10}) 

#Give three sets, A, B and U
#Second return is intersection of complements of A and B
def intersection_of_complements(A, B, U):
    # inputs: A, B and U are of type 'set'
    # output: a tuple of the form (set, set)
    k = set()
    for i in U: 
        if i not in A:
            k.add(i)
    l = set()
    for i in U: 
        if i not in B:
            l.add(i)
    m = set()
    for i in k:
        if i in l:
            m.add(i)
    return m

#check if function works
# A = {1, 2, 3, 4, 5}
# B = {0, 2, -6, 5, 8, 9}
# U = A|B|{-3, 7, 10, -4}
# assert(  intersection_of_complements(A, B, U) ==  {-4, -3, 7, 10} )

def product(A,B):
	u = set()
	for i in A:
		for j in B:
			u.add((i,j))
	return u

#check function
# A = {1,2,3}
# B = {3,4}
# print(product(A,B))
# assert(product(A,B) == { (1, 3), (3, 3), (1, 4), (2, 3), (3, 4), (2, 4)} )

#Give four sets, A, B, S and T
#First return the union of A and B
#The return the cartesian product of the union of A and B and the Union of S and T
def product_of_unions(A, B, S, T):
    # inputs: A, B, S and T are sets
    # output: a tuple of the type (set, set)
    u = set(A)
    for i in B:
        u.add(i)
    print(u)
    o = set(S)
    for i in T:
        o.add(i)
    print(o)
    p = set()
    for i in o:
        for j in u:
            p.add((j,i))
    return p

#check if function works
# A = {5}
# B = {5, 6}
# S = {-1, 0, 1}
# T = {1, 2}
# assert( product_of_unions(A, B, S, T) == \{(6, -1), (6, 0), (6, 1), (6, 2)}  )

#Give four sets, A, B, S and T
#First return the cartesian product of A and S
#Then return cartesian product of cross combinations, A*S,A*T,B*S,B*T

def union_of_products(A, B, S, T):
    # inputs: A, B, S and T are sets
    # output: a tuple of the type (set, set)
    u = set()
    o = set()
    for i in A:
        for j in S:
            o.add((i,j))
            u.add((i,j))
        for j in T:
            o.add((i,j))
    for i in B:
        for j in S:
            o.add((i,j))
        for j in T:
            o.add((i,j))
    return o

#check if function works
# A = {5}
# B = {5, 6}
# S = {-1, 0, 1}
# T = {1, 2}
# assert( union_of_products(A, B, S, T) == {(5, -1), (5, 0), (5, 1), (5, 2), (6, -1), (6, 0), (6, 1), (6, 2)}  \
#       )

#Give two sets A, B
#Then return unique elements in each set
def union_of_differences(A, B): #or unique elements in both sets
    k = set()
    for i in A:
        if i not in B:
            k.add(i)
    for j in B:
        if j not in A:
            k.add(j)
    return k

#check if function works
# A = {5,10,20,6}
# B = {5,11, 230, 10, 33,66}
# assert( union_of_differences(A, B) == \
# 	{33,66,6,230,11,20} \
# 	)

#UI example
# class Example(tk.Frame):
#     def __init__(self, parent):
#         tk.Frame.__init__(self, parent)

#         # create a prompt, an input box, an output label,
#         # and a button to do the computation
#         self.prompt = tk.Label(self, text="Enter a number:", anchor="w")
#         self.entry = tk.Entry(self)
#         self.submit = tk.Button(self, text="Submit", command = self.calculate)
#         self.output = tk.Label(self, text="")

#         # lay the widgets out on the screen. 
#         self.prompt.pack(side="top", fill="x")
#         self.entry.pack(side="top", fill="x", padx=20)
#         self.output.pack(side="top", fill="x", expand=True)
#         self.submit.pack(side="right")

#     def calculate(self):
#         # get the value from the input widget, convert
#         # it to an int, and do a calculation
#         try:
#             i = int(self.entry.get())
#             result = "%s*2=%s" % (i, i*2)
#         except ValueError:
#             result = "Please enter digits only"

#         # set the output widget to have our result
#         self.output.configure(text=result)

# # if this is run as a program (versus being imported),
# # create a root window and an instance of our example,
# # then start the event loop

# if __name__ == "__main__":
#     root = tk.Tk()
#     Example(root).pack(fill="both", expand=True)
#     root.mainloop()

#How to make the computer ask you questions:
A = set()
B = set()
for x in range(3):
    i = random.randint(1,11)
    str(i)
    A.add(i)
    i = random.randint(1,11)
    str(i)
    B.add(i)
k = union_of_differences(A, B)
h = str(len(k))
answer = input("How many elements are there in the union of differences between set {} and {} ?" .format(A,B))
print(type(answer))
if answer == h:
    print("{} is correct".format(answer))
else:
    print("{} is wrong, try again".format(answer))
print(answer)
print(k)
print(h)