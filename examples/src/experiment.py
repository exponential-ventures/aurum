#!/usr/bin/env python3

# import aurum as au
try:
    import aurum as au
except ImportError:
    import sys

    sys.path.append("../aurum")
    import aurum as au

au.parameters(a=0.01, b=1000, c=46, epochs=100, batch_size=200)

print(f"Parameter a = {au.a}")
print(f"Parameter b = {au.b}")
print(f"Parameter epochs = {au.epochs}")
print(f"Parameter batch_size = {au.batch_size}")
