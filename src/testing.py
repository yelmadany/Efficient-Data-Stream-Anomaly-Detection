import random
index = 23
if( 0 <= index < 8 or 17 <= index < 24):
  print((random.uniform(0,10)))



index = (index + 1) % 24

print('index = ', index)