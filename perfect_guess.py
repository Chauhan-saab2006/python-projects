import random
n = random.randint(1, 100 )
a = -1
gausses = 0       # start with 0 attempts
while(a != n):
    a = int(input("guess the number: "))
    gausses += 1  # increment attempts only once per guess
    if(a >n ):
        print("lower number please")
        
    elif(a<n):
        print("higher number please")   
        
print(f"you guessed the number {n} correctly in {gausses} attempts")