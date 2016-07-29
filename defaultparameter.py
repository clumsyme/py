# in memoize.py we see how to store calculated value to dic for later use.
# now we see another feature----action of default-parameters.
# and we will use this for a memoize.  
def foo(a=[]):
    a.append(5)
    return a
# >>> foo()
# [5]
# >>> foo()
# [5, 5]
# >>> foo()
# [5, 5, 5]
# >>> foo()
# [5, 5, 5, 5]
# >>> foo()
"""
    Actually, this is not a design flaw, and it is not because of internals, or performance.
    It comes simply from the fact that functions in Python are first-class objects, and not only a piece of code.

    As soon as you get to think into this way, then it completely makes sense: a function is an object 
    being evaluated on its definition; default parameters are kind of "member data" 
    and therefore their state may change from one call to the other - exactly as in any other object.

    In any case, Effbot has a very nice explanation of the reasons for this behavior in Default Parameter Values in Python.
    I found it very clear, and I really suggest reading it for a better knowledge of how function objects work.
"""
    
    """Default parameter values are evaluated when the function definition is executed. """

# OR:
#     When we define a function, at the momente it is defined, the default parameters is a ref to a certain
#     position of memory(we call it the init memory).
#     so 
#         def f(i=5)
#     or
#         def g(li=[])
#     the i ref to a certain memory, so does the li.
#     Everytime the function is called, it looks for that memory(the init memory).

#     But as we see, when we operate a int object or something unmutable, as i = i+1,
#     we are creating a new i ref to a new memory,so the origin memory value is unchanged.
#     The next time we call the function, it looks for the init memory and the value is still unchange.

#     The other way, unlike int, we all know that when we operate list, it DOES NOT creat a new object in memory
#     to link the ref, it just modify the value in init memory.So, as long as we do li.append(1), the init memory
#     vaule will change, the next time the function is called, the default value is nolonger the init value.

#     It may lead us to mistake when we do not relize it, but we can take advantage of it also.
#     The fib function below use recursion has a large cost, as there's lot's of repeat calculations.
        def fib(n):
            if n<2:
                return n
            else:
                return fib(n-1) + fib(n-2)
#     This can be potimized by store calculated value in a dict, so repeat calculations will be replaced as 
#     dict lookups.As below:

#     ##### HERE IS THE MEMOIZE VERSION OF FIB: #####
        def fib(n, values = {}):
            if n<2:
                return n
            try:
                result = values[n]
            except:
                values[n] = fib(n-1) + fib(n-2)
                result = values[n]
            return result

#     # THIS efficiently reduce recursion repeat calculations, but still has a dict stored in memory.
#     # SO, it's still not as good as the iter one which is:
          def fib(n):
              a,b = 0,1
              for i in range(n):
                  a,b = b,a+b
              return a

# Here's the evidence:
# --------------------------------
    def mutable(var=[]):
	    print(id(var))      # present the id before modify it.
	    var.append(1)       # modify it.
	    print(id(var))      # present the id after modify it.

#     >>> mutable()
#     58295048
#     58295048    # use default value, after modify it, the id does't change.BUT var.value changed.
#     >>> mutable([2])
#     58296904    # no-use default value, id of var is not the init one.
#     58296904    # still, after modified, it's id remain the begining of the call.
#     >>> mutable()
#     58295048    # we use default value to call it again, it does use the init id and remain unchanged.
#     58295048    #

# ----------------------------------
    def unmutable(var=1):
	    print(id(var))
	    var += 1
	    print(id(var))

#     >>> unmutable()
#     1515979216
#     1515979248  # changed
#     >>> unmatable(2)
#     1515979248  # not init one.
#     1515979280  still changed.
#     >>> unmutable()
#     1515979216  # init one.
#     1515979248  # changed.
#     -----------------------------------
#     BUT another side, we know after
#         list = list+b
#     id(list) is changed,so the following is different from mutable():

    def mutorno(var=[]):
	    print(id(var))
	    var = var+[1]
	    print(id(var))
#     >>> mutorno()
#     58963016
#     58963208    # id DOES CHANGED.
#     >>> mutorno([2])
#     58353800
#     58963144
#     >>> mutorno()
#     58963016
#     58360008
#     this function will return [1] every time insteed [1]\[1,1]\[1,1,1]... in the mutable().
#     WHY?Because every call does not change the value of init memory, so every call with d-value get same value.
#     While mutable() does change the value of init memory, so every call with d-value get non-same value.

# In fact， if we can find out the value in memory, we would know it better.
# Luckly, the ctype module provide a function for us to know the value in 
# memory with a id of ID.
import ctypes
def mem_value(ID):
    """return the value in memory with id:ID."""
	return ctypes.cast(ID, ctypes.py_object).value

def i(var=1):
    init_id = id(var)
	print("Before var+=1, var.id and value in init memory:")
	print(id(var))
	print(mem_value(init_id))
	var += 1
	print("After i+=1, var.id and value in init memory:")
	print(id(var))
	print(mem_value(init_id))
# >>> i()
# Before var+=1, var.id and value in init memory:
# 1537409488
# 1
# After i+=1, var.id and value in init memory:
# 1537409520                                       # so, id changed, which means the pointer of var changed to another memory. 
# 1                                                # but value in init memory DOES NOT change.


def li(var=[1]):
	init_id = id(var)
	print("Before var+=[1], var.id and value in init memory:")
	print(id(var))
	print(mem_value(init_id))
	var += [1]
	print("After i+=1, var.id and value in init memory:")
	print(id(var))
	print(mem_value(init_id))	
# >>> li()
# Before var+=[1], var.id and value in init memory:
# 59061512
# [1]
# After i+=1, var.id and value in init memory:
# 59061512                                        # so, id Does Not change,  which means the pointer of var still point to init memory.
# [1, 1]                                          # but value in init memory DID change.
