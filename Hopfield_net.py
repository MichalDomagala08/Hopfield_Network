
import sys
import time
import os
import numpy as np
import random
import math

trys = 'Y'


def inputs():
	print('\n \n')
	print('                              ==== Sieć Hopfelda ====')
	print()
	print('Program służy do odzyskiwania wyuczonych w sieci Hopfelda wzorców prezentujących liczby,')
	print('Jednocześnie obrazuje procesu uczenia sieci. Sieć ma zapisane w pamięci następujące liczby: ')
	print()
	print('             '+ '  * * *  ' +'     ' + '* * *    '  +'     ' + '    *    ')
	print('             '+ '*       *' +'     ' + '      *  '  +'     ' + '  * *    ')
	print('             '+ '*       *' +'     ' + '      *  '  +'     ' + '*   *    ')
	print('             '+ '*       *' +'     ' + '  * *    '  +'     ' + '    *    ')
	print('             '+ '*       *' +'     ' + '*        '  +'     ' + '    *    ')
	print('             '+ '  * * *  ' +'     ' + '* * * * *'  +'     ' + '    *    ')
	print('             '+ '         ' +'     ' + '         '  +'     ' + '         ')
	print('             '+ '  zero   ' +'     ' + '  dwa    '  +'     ' + '  jeden  ')
	print()
	print('Program jest w stanie odzyskać wyżej podane liczby przy pomocy niżej wypisanych częściowych danych')
	print()
	print('             '+ '  * * *  ' +'     ' + '* * *    '  +'     ' + '    *    ')
	print('             '+ '*       *' +'     ' + '      *  '  +'     ' + '  * *    ')
	print('             '+ '*       *' +'     ' + '      *  '  +'     ' + '*   *    ')
	print('             '+ '         ' +'     ' + '         '  +'     ' + '         ')
	print('             '+ '         ' +'     ' + '         '  +'     ' + '         ')
	print('             '+ '         ' +'     ' + '         '  +'     ' + '         ')
	print()

	global part
	global trys

	ins = input('Wpisz jaki obrazek chcesz odzyskać: ')
	print()
	if ins =='zero':
		part = half_zero1
	elif ins =='jeden':
		part = half_one1
	elif ins =='dwa':
		part = half_two1
	else:
		trys ='N'
		print('Zła etykieta. Program Kończy działanie')
		
	print()
	input('        ==Nacisnij dowolny klawisz aby zacząć==')



###      ===Narzędzia===

## =Zmiana Reprezentacji=

#Zamienia reprezentacje 0,1 na -1,1
def dychotomy(wektor):
    op = np.zeros(wektor.shape[0])

    for i in range(wektor.shape[0]):
        if wektor[i] ==0:
            op[i] = -1
        else:
            op[i] = 1
    
    return op

#Dla synchronicznego uczenia --> zmienia output mnożeniwa wektora n -1 lub 1
def signum(sums):
    sumss = np.array(sums)


    sums_eq = np.zeros(sums.shape[1])

    for i in range(len(sumss[0])):
        #print(sums_eq)

        if sumss[0][i] >= 0:
            sums_eq[i] = 1
        else:
            sums_eq[i] = -1
        
    return sums_eq

#Dekoduje  z zapisu -1,1 na zapis 0,1, by możbna było wyświetlać
def decode(rray):
    eq = np.zeros((rray.shape[0]),dtype='int')
    for i in range(len(rray)):
        if rray[i] == 1:
            eq[i] = 1
    return np.matrix(eq,dtype='int')

## =Funkcje limitujące=    

#Funkcja sprawdzająca warubnki zapisu danych, czyo pozwolą stworzyć dobrą sieć Hopfielda
def memory_limit_function(data):
    return data.shape[0] <= math.floor(data.shape[1]/(2*math.log(data.shape[1])))
    

#Funkcja Energii, obliczająca dla każdej iteacji
def energy(weights,x):
    E = -(1/2)*x.T.dot(weights).dot(x)
    return np.array(E)


## =Funkcje Rysujące=

#Rysuje zachowaną w wektorze cyfrę
def draw_bin_image(image_matrix):
    for row in image_matrix.tolist():
        print('| ' + ' '.join(' *'[val] for val in row))


#Pozwala na rysowanie opóźnione w czasie
def periodic_draw(image_matrix):
    import sys
    import time
    import os

    print()
    print('Szukana Liczba:')
    print()
    draw_bin_image(decode(image_matrix).reshape((6,5)))
    print()
    print('Energia: {}'.format(En))
    print('Iteracje: {}'.format(count))

    time.sleep(0.05)
    os.system('cls')


### ===DEKLARACJA SIECI===



# Uczy sieć na podstawie dostrczonej Macierzy wektorów
def weights(wektory):
    #print( wektory.T.dot( wektory))
    xx = wektory.T.dot( wektory)
    np.fill_diagonal(xx,0)
    return xx


#Synchroniczne odzyskiwanie
def recovery_synchronus(weights,inp):
    sums  =np.matmul(inp,weights)
    sums_eq = signum(sums)
        
    return sums_eq

#Asynchroniczne odzyskiwanie
def recovery_asynchronus(weights,inp, it = 10000):
    weights = np.array(weights)
    inp = np.array(inp)
    global En
    En = 0
    global count
    count =0
    wh = True
    while wh == True and count < 10000:
        count +=1
        column = random.randint(0,inp.shape[0] -1)
        Value = np.sign(weights[:][column].dot(inp.T))
        
        #Checking
        '''
        print('Picked vector: {}'.format(column))
        print('Calculated value: {}'.format(Value))
        print('Updated vector:\n {}'.format(inp))
        '''

        inp[column] = Value
        En = energy(weights,inp)

        periodic_draw(inp) 

        if En <= -400 :

        	#Energu check:
            '''
            print('Energy: {}'.format(En))
            print('Count: {}'.format(count))
            '''
            return inp
            break
    return inp



###   ==Dostępne Wektory Liczb==
    
## =Całe=

#Zero
zero = np.array([
 0, 1, 1, 1, 0,
1, 0, 0, 0, 1,
1, 0, 0, 0, 1,
 1, 0, 0, 0, 1,
1, 0, 0, 0, 1,
0, 1, 1, 1, 0
])

zero1 = dychotomy(zero)

#Jeden
one11 = np.array([
0, 0, 1, 0, 0,
0, 1, 1, 0, 0,
1, 0, 1, 0, 0,
0, 0, 1, 0, 0,
0, 0, 1, 0, 0,
0, 0, 1, 0, 0
])

one1 = dychotomy(one11)

#Dwa
two = np.array([
1, 1, 1, 0, 0,
0, 0, 0, 1, 0,
0, 0, 0, 1, 0,
0, 1, 1, 0, 0,
1, 0, 0, 0, 0,
1, 1, 1, 1, 1,
])

two1 = dychotomy(two)

#Uszkodzone Jeden
one = np.array([
0, 1, 1, 0, 0,
0, 0, 1, 0, 0,
0, 0, 1, 0, 0,
0, 0, 1, 0, 0,
0, 0, 1, 0, 0,
0, 0, 1, 0, 0
])

one111 = dychotomy(one)

##  =Połówki=

#Pół- Zero
half_zero = np.array([
0, 1, 1, 1, 0,
0, 0, 0, 0, 0,
0, 0, 0, 0, 0,
0, 0, 0, 0, 0,
0, 0, 0, 0, 0,
0, 0, 0, 0, 0,
])

half_zero1 = dychotomy(half_zero)

#Pół- Jeden
half_one = np.array([
0, 0, 1, 0, 0,
0, 1, 1, 0, 0,
1, 0, 1, 0, 0,
0, 0, 0, 0, 0,
0, 0, 0, 0, 0,
0, 0, 0, 0, 0
])

half_one1 = dychotomy(half_one)

#Pół - Dwa
half_two = np.array([
1, 1, 1, 0, 0,
0, 0, 0, 1, 0,
0, 0, 0, 1, 0,
0, 0, 0, 0, 0,
0, 0, 0, 0, 0,
0, 0, 0, 0, 0,
])

half_two1 = dychotomy(half_two)




####               ====WŁAŚCIWY PROGRAM====

data = np.concatenate([ np.matrix(zero1), np.matrix(one1), np.matrix(two1)], axis=0)
x = (weights(data))
while trys != 'N':
	inputs()
	if trys == 'N':
		break

	if memory_limit_function(data) == True:
	    base = recovery_asynchronus(x,part)
	    xx = decode(base)
	    print()
	    print('Szukana Liczba:')
	    print()
	    draw_bin_image(xx.reshape((6,5)))
	    print()
	    print('Energia: {}'.format(En))
	    print('Iteracje: {}'.format(count))
	    print()
	    trys = input('Czy chcesz obliczyć jeszcze raz? (Y/N): ')
	    os.system('cls')
print()
print('Dziękuję za uwagę! C: ')
print()
input('Naciśnij dowolny klawisz aby zakończyć działanie programu')
os.system('cls')



