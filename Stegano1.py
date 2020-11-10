import os 
from PIL import Image
from numpy import asarray

global Feature #Permet de dire si le message est crypté ou non (0si non 1 si oui)

def crypt(phrase,clef) :
    f = ""
    p = 0
    for c in phrase :
        t = 0;n=0
        if p == len(clef) :
            p = 0
        for i in alphabet :
            if i == c : n+=t
            if clef[p] == i : n+=t
            t+=1
        if n > len(alphabet) :
            n -= len(alphabet)
        f+=alphabet[n]
        p+=1
    return f

def decrypt(phrase,clef) :
    f = ""
    p = 0
    for c in phrase :
        t=0;m=0;cl=0
        if p == len(clef) :
            p = 0
        for i in alphabet :
            if i == c : m=t
            if i == clef[p] : cl=t
            t+=1
        n = m-cl
        if n < 0 :
            n+=len(alphabet)
        f+=alphabet[n]
        p+=1
    return f

def color_regular(pixel,data) :
    ligne, colonne = pixel_to_list_number(pixel,data)
    ligne = data[ligne]
    nb = 0;total=0
    for pix in ligne :nb+=pix[2];total+=1
    l=str(nb/total).split('.')
    result = int(l[0])
    return result
    
global alphabet
alphabet=[]
for i in "apzoeirutyqm sldkfjghwnxbcvAMZLEçKRJTHYGFUDISOQPWNXBCV1907856432)è(@#:/=+/;,?.ù%$€*àé§&'" :
    alphabet.append(i)

def pixel_to_list_number(pixel,data) :
    lon, Lag, nul = data.shape
    p = 0
    while pixel > (Lag-1) :
        p+=1
        pixel = pixel-Lag
    return p, pixel #ligne colonne
        
def see(file_name) :
    data = asarray(Image.open(str(file_name))).copy()
    nb_color = data[0][0]
    pixel = 0
    longueur = 0
    i = True
    while i :
        ligne, colonne = pixel_to_list_number(pixel,data)
        valeur = data[ligne][colonne][0]
        if valeur == 255 :
            i = False
        else :
            longueur += valeur
        pixel += 1
    ligne, colonne = pixel_to_list_number(pixel,data)
    Feature = valeur = data[ligne][colonne][2]
    if Feature == 1 :
        print('The Message is encrypted : enter the key')
        key = input('-> ')
    pixel+=1
    #cherche la moyenne
    ligne, colonne = pixel_to_list_number(pixel,data)
    moyenne = data[ligne][colonne][2]
    last_ligne = ligne
    pixel += 1
    final = ""
    alternance = 0
    for i in range(longueur) :
        if int(alternance) == int(len(nb_color)) :
            alternance = 0
        ligne, colonne = pixel_to_list_number(pixel,data)
        if last_ligne != ligne :
            #print(data[ligne][colonne][2],'moyenne')
            ligne, colonne = pixel_to_list_number(pixel,data)
            moyenne = data[ligne][colonne][2]
            pixel += 1
            ligne, colonne = pixel_to_list_number(pixel,data)
            lettre_position = ((moyenne+alternance) - data[ligne][colonne][2]) * -1
            if lettre_position * -1 > len(alphabet) :
                lettre_position += 255 
            t = 0; d = 0
            for lt in alphabet :
                if t == lettre_position :
                    final += lt
                if d == 1 :
                    t = t * (-1)
                    d = 0
                else :
                    d = 1
                    t = t * (-1)
                    t += 1
            alternance += 1
            pixel += 1
        else :
            #print(data[ligne][colonne][2],'lettre',alternance)
            lettre_position = ((moyenne+alternance) - data[ligne][colonne][2]) * -1
            if lettre_position * -1 > len(alphabet) :
                lettre_position += 255 
            t = 0; d = 0
            for lt in alphabet :
                if t == lettre_position :
                    final += lt
                if d == 1 :
                    t = t * (-1)
                    d = 0
                else :
                    d = 1
                    t = t * (-1)
                    t += 1
            alternance += 1
            pixel += 1
    
        last_ligne = ligne
    print(final)
    if Feature == 1 : final = decrypt(final,key);print(final)

def hide(file_name) :
    #test convertir une image en tableau
    data = asarray(Image.open(str(file_name))).copy()
    """
    Que contient data ?
    Data contient des tableaux qui représente une ligne et qui contienne chacun
    un nombre de "liste" equivalent a la Lageur.
        Par exemple, sur une image de dimendion 10*2 (Largeur * Hauteur), on au
    ra comme donné, dans data, 2 tableau qui comporte chacun 10 liste (une list
    e equivaut a 1 pixel : il y a, normalement 3 nb RGB mais il peut aussi y en
    avoir 4).
    """
    #savoir si l'image est en RGB ou en RGBA
    nb_color = data[0][0] #on se refaire au premier pixel [190 220 248 255]
    """
    Modification de notre code :
    premier pixel jusqu'au signal pour donner la longueur du message
    le signal est 255 car la longueurdu message ne dépasse pas 254
    puis on inscrit le message en alternant les pixels
    """
    total = len(sentence)
    pixel = 0
    i = True
    while i :
        ligne, colonne = pixel_to_list_number(pixel,data)
        if total > 254 :
            data[ligne][colonne][0] = 254
        else :
            data[ligne][colonne][0] = total
            i = False
        total -= 254
        pixel+=1 
    #dis que c'est la fin de la longueur :
    ligne, colonne = pixel_to_list_number(pixel,data)
    data[ligne][colonne][0] = 255
    pixel+=1
    #dis le type de Message :
    ligne, colonne = pixel_to_list_number(pixel,data) 
    data[ligne][colonne][2] = int(Feature) #attention on entre la donné sur le pixel Blue
    pixel+=1

    ligne, colonne = pixel_to_list_number(pixel,data)
    last_ligne = ligne 
    moyenne = color_regular(pixel,data)
    data[ligne][colonne][2] = moyenne
    pixel+=1

    #ecrire le message en alternance R G et B :
    alternance = 0
    for charactere in sentence :
        if int(alternance) == int(len(nb_color)) :
            alternance = 0
        t = 0; d = 0
        for i in alphabet :
            if i == charactere :
                p = t
            if d == 1 :
                t = t * (-1)
                d = 0
            else :
                d = 1
                t = t * (-1)
                t += 1
        ligne, colonne = pixel_to_list_number(pixel,data)
        if last_ligne != ligne :
            data[ligne][colonne][2] = color_regular(pixel,data)
            moyenne = color_regular(pixel,data)
            pixel+=1
            last_ligne = ligne
            ligne, colonne = pixel_to_list_number(pixel,data)
            calcul = moyenne + p + alternance
            if calcul > 255 :
                calcul -= 255
            data[ligne][colonne][2] = calcul
            pixel += 1
            alternance += 1
            #print(data[ligne][colonne][2],'moyenne')
        else : 
            calcul = moyenne + p + alternance
            if calcul > 255 :
                calcul -= 255
            data[ligne][colonne][2] = calcul
            pixel += 1
            last_ligne = ligne
            #print(data[ligne][colonne][2],'lettre',alternance)
            alternance += 1 
            
        
    imagefinal = Image.fromarray(data)
    file_list = file_name.split('.')
    del file_list[-1]
    imagefinal = imagefinal.save(str("".join(file_list))+"M.png") 

while True : 
    if input('[H]ide or [S]ee the message : ').lower() == "h" :
        global sentence
        sentence = input('Sentence to hide : ')  
        if input('[E]ncrypt or [N]ormal : ').lower() == 'e' :
            sentence = crypt(sentence,input('Key -> '))
            Feature = 1
        else : Feature = 0
        print(sentence)
        p=1;print('')
        for i in os.listdir() :print(str(p)+". " + i);p+=1
        print('');choice = int(input('Number of the concerning file : '))
        file_name = os.listdir()[choice-1]
        hide(file_name)
    else :
        p=1;print('')
        for i in os.listdir() :print(str(p)+". " + i);p+=1
        print('');choice = int(input('Number of the concerning file : '))
        file_name = os.listdir()[choice-1]
        see(file_name)
    