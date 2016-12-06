# Algorithm Performance Speed-Up more than 100 times!

## source comes from: [用python的交易员](https://zhuanlan.zhihu.com/p/24168485?refer=vn-py)

> This file introduces different kinds of methods that could promote Python running performance.

> Method includes: basic, numpy(wrong), numpy(right), numba, algorithm improvement, combination of numba and algorithm improvement, Cython(simple), Cython(static) and algorithm improvement.

Cython user guide:
> 1.Put the function that you wish to run by Cython into .pyx file such as helloworld.pyx

> 2.Set up a file called setup.py which is used to set compile contents

> 3.Open terminal and changes to the dictionary which contains helloworld.pyx and setup.py

> 4.Running "python setup.py build_ext --inplace"

> 5.If succeed, there will be a new file called helloworld.pyd

> 6.After that, you can import helloworld just like import other modules


