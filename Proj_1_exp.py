#Ben Moreau

import numpy as np
from math import *
from matplotlib import pyplot as plt
import os

##
#
## DONT RUN THIS IN SHELL, IT WONT WORK. RUN IT IN PYTHON 3 FROM TEH CMB or TERMIANAL
#
#
res_f0=open("Dice_Roll_Res0.txt","w+")
res_f1=open("Dice_Roll_Res1.txt","w+")
log0=open("log_like0.txt","w+")
log1=open("log_like1.txt","w+")
param=open("param.txt","w+")

Num_exp=10000
Num_rolls=100
Num_sides=20
Side_number=11

Dice_power=1.3
print("Input custom values? Y/N")
y=input()

while(y!="Y" and y!="N"):
    print("Input custom values? Y/N")
    y=input()


if(y=="Y"):
    print("input the number of exp:")
    Num_exp=float(input())
    print("input the number of rolls/exp:")
    Num_rolls=float(input())
    print("input the number of side on the die:")
    Num_sides=float(input())
    print("input the number of the side you want to test for:")
    Side_number=float(input())
    print("input the power of the dices weight (it may cause errors for values above 2 or so):")
    Dice_power=float(input())

Num_exp=int(Num_exp)
Num_rolls=int(Num_rolls)
Num_sides=int(Num_sides)
Side_number=int(Side_number)

print("A")
for i in range(100):
    param.write("Num_exp Num_rolls Num_sides Side_number Dice_power"+"\n") #need this or else it wont work for some reason

#print(Num_sides,Side_number,Num_sides)
p0=(1)/Num_sides #we believe the dice is fair
#p1=Side_number/Num_sides*0.05 #if the dice is loaded for a low roll



p1=[100000000]
for i in range(Num_sides-1):
    p1.append(p1[0]/Dice_power**(i+1)) #For a dice cube weighted so that the probability of a side is lowered by a factor of Dice_power for each side greater than 1
    
    #print(sum(p1))
Sp1=sum(p1)
#print(p1[0])
for i in range(Num_sides):
    #print(p1[i])
    #print()
    p1[i]=p1[i]/Sp1
    #print("N",p1[i])
    #print()
#print(p1[0])
#print(p1)
#print(sum(p1))
#print(len(p1))
#print(p1)
#print(sum(p1)) #Those probabilities for the loaded die sum to 1


if(Side_number>Num_sides):
    print("Number of sides updated to ",Side_number+1)

for i in range(100):
    param.write(str(Num_exp)+" "+str(Num_rolls)+" "+str(Num_sides)+" "+str(Side_number)+" "+str(Dice_power)+"\n")


avg_result=0


Exp_res=[]
Exp_successes=[]

Npass0=[]
LogLikeRatio0=[]


for i in range(Num_exp):
###
    Roll_res=[]
    LLR = 0
    Npass=0
    for l in range(Num_rolls):

        
        a=np.random.randint(1,Num_sides+1)
        #print(a)
        
        #print(a)
        if(a>=Side_number):

            
            Roll_res.append(1) #If the random number is higher than the side number specified, the roll was a success
            Npass += float(1)
            #print(p1[int(a):len(p1)-1])
            #print(sum(p1[int(a)-1:]))
            #print(p1[int(a)-1:])
            #print(int(a)-1)
            
            LLR += log( sum(p1[Side_number-1:])/(p0*(Num_sides-Side_number)))
        else:
            #print(p1[int(a):len(p1)-1])
            #print(sum(p1[int(a)-1:]))
            #print(p1[int(a)-1:])
            #print(int(a)-1)
            Roll_res.append(0) #Conversely, it fails
            LLR += log( (1- sum(p1[Side_number-1:]))/(1-p0*(Num_sides-Side_number)) )########################FIIXIX MEE
        res_f0.write(str(a)+"\n")

    log0.write(str(LLR)+"\n")


    '''
    if Npass < Npass_min:
        Npass_min = Npass
    if Npass > Npass_max:
        Npass_max = Npass
    if LLR < LLR_min:
        LLR_min = LLR
    if LLR > LLR_max:
        LLR_max = LLR
    '''
    Npass0.append(Npass)
    LogLikeRatio0.append(LLR)
###

            
    total_success=sum(Roll_res)

    exp_prob=(total_success/Num_rolls)


    Exp_res.append(exp_prob)

    Exp_successes.append(total_success)
    
    #print(Roll_res,exp_prob)

avg_result=sum(Exp_res)/Num_exp


Exp_res1=[]
Exp_successes1=[]

Npass1=[]
LogLikeRatio1=[]


for i in range(Num_exp):
###
    Roll_res=[]
    LLR = 0
    Npass=0
    for l in range(Num_rolls):

        
        a=np.random.randint(1,10**18+1)/10**18*Dice_power**Num_sides
        
        #print(a)
        lmno=1
        while(1==1):

            if(a>Dice_power**(Num_sides-lmno)):
                a=lmno#Choose the side number in a way that reflects the exponent, for a factor of two, 1 has a 50% chance, 2 has a 25% chance, etc.
                break;

            #if a is too small, it is the least probable side
            if(lmno>len(p1)-2):
                a=lmno
                break;
            lmno+=1
        res_f1.write(str(a)+"\n")

        #print(a)
        if(a>=Side_number):

            
            Roll_res.append(1) #If the random number is higher than the side number specified, the roll was a success
            Npass += float(1)
            LLR += log( sum(p1[Side_number-1:])/(p0*(Num_sides-Side_number)))
        else:

            Roll_res.append(0) #Conversely, it fails
            LLR += log( (1- sum(p1[Side_number-1:]))/(1-p0*(Num_sides-Side_number)) )
    '''
    if Npass < Npass_min:
        Npass_min = Npass
    if Npass > Npass_max:
        Npass_max = Npass
    if LLR < LLR_min:
        LLR_min = LLR
    if LLR > LLR_max:
        LLR_max = LLR
    '''
    Npass1.append(Npass)
    LogLikeRatio1.append(LLR)
    log1.write(str(LLR)+"\n")
