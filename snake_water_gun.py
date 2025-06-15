import random

# its a game
#where you have choes b/w s , w and g "s = snake , w = water, g = gun"

computer = random.choice([-1, 1, 0])
youstr = input("enter your choice: ")
youduct={"s":1, "w":-1, "g":0}
reversdict={1:"snake", -1:"water", 0:"gun"}
you= youduct[youstr]

print(f"you chose: {reversdict[you]}\ncomputer choice: {reversdict[computer]}")

if(computer==you):  # if both chose same than match is draw
    print("its a draw")

else:    
    if(computer==-1 and you == 1):
        print("you win")
    elif(computer==-1 and you ==0):
        print("you lose")                
    elif(computer==1 and you ==-1):
        print("you lose") 
    elif(computer==1 and you ==0):
        print("you win") 
    elif(computer==0 and you ==-1):
        print("you win")         
    elif(computer==0 and you ==1):
        print("you lose") 
    else:
        print("something went erong!")