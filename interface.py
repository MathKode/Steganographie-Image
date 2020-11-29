from tkinter import *
from tkinter import filedialog
from PIL import Image
from numpy import asarray
import numpy as np
import os
import pdfstegano as h_pdf

window = Tk()
window.title('Steganagraphie')
window.geometry('500x500')
window.minsize(500,500)
window.maxsize(500,500)
window.config(background="#414C7B")

global data

def result_mms(final) :
    ereur = Tk()
    ereur.title('Déchiffrer')
    ereur.geometry("400x70")
    ereur.minsize(400,70)
    ereur.maxsize(800,70)
    ereur.config(background="white")
    Label(ereur,text="Le contenu de l'image est :").pack()
    A = Entry(ereur,font=('Arial',10),width=800)
    A.pack()
    A.insert(0,final)
    Entry_chemin_decrypt.delete(0,END)
    ereur.mainloop()
    
def seepdfok() :
    file = open('cheminpdf','r')
    ls = file.read().split('\n')
    file.close()
    Chemin = ls[0]
    clef = key_entry_pdf.get()
    if clef == "" : clef = "a"
    result = h_pdf.Show(Chemin,clef)
    result_mms(result)
    

def seepdf(Chemin) :
    file = open('cheminpdf','w')
    file.write(Chemin)
    file.close()
    ereur = Tk()
    ereur.title('Déchiffrer')
    ereur.geometry("400x70")
    ereur.minsize(400,70)
    ereur.maxsize(500,70)
    ereur.config(background="white")
    Label(ereur,text="Le contenu du document est obligatoirement chiffré, entrer la clef et appuyer sur ok").pack()
    global key_entry_pdf
    key_entry_pdf = Entry(ereur,font=("Arial",10),width=100)
    key_entry_pdf.pack()
    Button(ereur,text='ok',command=seepdfok).pack()
    ereur.mainloop()
        

def key_ok() :

    key = key_entry.get()
    file = open("pixel.txt",'r')
    pixel = int(file.read())
    file.close()
    file = open("data.txt","r")
    file_name = file.read()
    file.close()
    file = open("longueur.txt","r")
    longueur = int(file.read())
    file.close()
    file = open("nb_color.txt","r")
    nb_color = int(file.read())
    print(nb_color)
    os.remove('pixel.txt')
    os.remove('data.txt')
    os.remove('longueur.txt')
    os.remove('nb_color.txt')
    file.close()
    data = asarray(Image.open(str(file_name))).copy()

    pixel+=1
    #cherche la moyenne
    ligne, colonne = pixel_to_list_number(pixel,data)
    moyenne = data[ligne][colonne][2]
    last_ligne = ligne
    pixel += 1
    final = ""
    alternance = 0
    for i in range(longueur) :
        if int(alternance) == int(nb_color) :
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
    final = decrypt(final,key)
    print(final)
    result_mms(final)
def key_input() :
    ereur = Tk()
    ereur.title('Déchiffrer')
    ereur.geometry("400x70")
    ereur.minsize(400,70)
    ereur.maxsize(500,70)
    ereur.config(background="white")
    Label(ereur,text="Le contenu de l'image est chiffré, entrer la clef et appuyer sur ok").pack()
    global key_entry
    key_entry = Entry(ereur,font=("Arial",10),width=100)
    key_entry.pack()
    Button(ereur,text='ok',command=key_ok).pack()
    ereur.mainloop()

def result(way) :
    ereur = Tk()
    ereur.title('SUCCESFUL')
    ereur.geometry("300x70")
    ereur.minsize(300,70)
    ereur.maxsize(1000,70)
    ereur.config(background="white")
    Label(ereur,text=f"L'image/pdf vient d'etre stenographié : \n{way}").pack()
    Entry_chemin.delete(0,END)
    Message_entry.delete(0,END)
    Clef_entry.delete(0,END)
    Crypt_checkbutton.deselect()
    ereur.mainloop()
    

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


def pixel_to_list_number(pixel,data) :
    lon, Lag, nul = data.shape
    p = 0
    while pixel > (Lag-1) :
        p+=1
        pixel = pixel-Lag
    return p, pixel #ligne colonne
      
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

def see(file_name) :
    data = asarray(Image.open(str(file_name))).copy()
    nb_color = data[0][0]
    pixel = 0
    longueur = 0
    i = True
    while i :
        ligne, colonne = pixel_to_list_number(pixel,data)
        valeur = data[ligne][colonne][2]
        if valeur == 255 :
            i = False
        else :
            longueur += valeur
        pixel += 1
    ligne, colonne = pixel_to_list_number(pixel,data)
    Feature = valeur = data[ligne][colonne][2]
    if Feature == 1 :
        print('The Message is encrypted : enter the key')
        file = open('pixel.txt','w')
        file.write(str(pixel))
        file.close()
        file = open('data.txt','w')
        file.write(str(file_name))
        file.close()
        file = open('longueur.txt','w')
        file.write(str(longueur))
        file.close()
        file = open('nb_color.txt','w')
        file.write(str(len(nb_color)))
        file.close()
        key_input()
    else :
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
        result_mms(final)

def hide(file_name,sentence,Feature) :
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
            data[ligne][colonne][2] = 254
        else :
            data[ligne][colonne][2] = total
            i = False
        total -= 254
        pixel+=1 
    #dis que c'est la fin de la longueur :
    ligne, colonne = pixel_to_list_number(pixel,data)
    data[ligne][colonne][2] = 255
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
    print("Le fichier a été sauvegardé")
    result(str("".join(file_list)+"M.png"))

def erreur() :
    ereur = Tk()
    ereur.title('ATTENTION')
    ereur.geometry("300x70")
    ereur.minsize(300,70)
    ereur.maxsize(300,70)
    ereur.config(background="white")
    Label(ereur,text="Attention, tu dois remplir toutes les cases. \nMerci").pack()
    ereur.mainloop()

def browse_file() :
    filename = filedialog.askopenfilename(initialdir="/",title="Select_picture",filetypes = (("Image", "*.*"),("all files", "*.*")))
    Entry_chemin.delete(0,END)
    Entry_chemin.insert(0,filename)

def browse_file2() :
    filename = filedialog.askopenfilename(initialdir="/",title="Select_picture",filetypes = (("Image", "*.*"),("all files", "*.*")))
    Entry_chemin_decrypt.delete(0,END)
    Entry_chemin_decrypt.insert(0,filename)

def hidetkinter() :
    print('hide')
    #test si tous est remplis
    Message = Message_entry.get()
    Choix = choix.get()
    Feature = choix.get()
    print(Feature)
    Chemin = Entry_chemin.get()
    ls = Chemin.split('.')
    extension = str(ls[-1]).lower()
    if Choix == 1 :
        Clef = Clef_entry.get()
        if Message == "" or Clef == "" or Chemin == "" :   
            erreur()
        else :
            sentence = crypt(Message,Clef)
            if extension == 'pdf' :
                h_pdf.Hide(Chemin,Message,Clef)
                result(Chemin)
            else :
                hide(Chemin,sentence,Feature)
    else :
        Clef = ""
        if Message == "" or Chemin == "":
            erreur()
        else :
            if extension == 'pdf' :
                h_pdf.Hide(Chemin,Message,"a")
                result(Chemin)
            else :
                hide(Chemin,sentence,Feature)

def showtkinter() :
    Chemin = Entry_chemin_decrypt.get()
    ls = Chemin.split('.')
    extension = str(ls[-1]).lower()
    if Chemin == "" :
        erreur()
    else :
        if extension == "pdf" :
            seepdf(Chemin)
        else :
            see(Chemin)

Frame(window,bg="#414C7B",height=10).pack()

paragraphe_frame = Frame(window,bg='#798AD4',width=450)

Titre_label = Label(paragraphe_frame,text='Stéganographie',font=('Arial',20),bg='#798AD4',fg='black')
Titre_label.grid(row=0,column=1)

Auteur_label = Label(paragraphe_frame,text="by BIMATHAX",font=("Arial",13),bg="#798AD4",fg="black")
Auteur_label.grid(row=1,column=0)

Space = Frame(paragraphe_frame,bg="#798AD4",width=100)
Space.grid(row=1,column=2)

Frame(paragraphe_frame,bg='#798AD4',height=3).grid(row=2,column=0)
paragraphe_frame.pack()

Frame(window,bg="#414C7B",height=10).pack()
Frame(window,bg="#FFFFFF",width=500,height=4).pack()


Message_paragraphe = Frame(window,bg="#414C7B")

Info_text = Label(Message_paragraphe,bg="#414C7B",fg='black',font=('Arial',15),text="Message :")
Info_text.grid(row=0,column=0)

global Message_entry
Message_entry = Entry(Message_paragraphe,bg='white',fg='black',font=('Arial',12),width=55)
Message_entry.grid(row=1,column=2)

Frame(Message_paragraphe,bg='#414C7B',height=10).grid(row=2,column=1)

Info_text = Label(Message_paragraphe,bg="#414C7B",fg='black',font=('Arial',15),text="Clef :       ")
Info_text.grid(row=3,column=0)

global choix
choix = IntVar()
Crypt_checkbutton = Checkbutton(Message_paragraphe,text='Chiffrer',bg="#414C7B",variable=choix)
Crypt_checkbutton.grid(row=4,column=0)

Label(Message_paragraphe,bg="#414C7B",width=3).grid(row=4,column=1)

global Clef_entry
Clef_entry = Entry(Message_paragraphe,bg='white',fg='black',font=("Arial",12),width=55)
Clef_entry.grid(row=4,column=2)

Frame(Message_paragraphe,bg='#414C7B',height=20).grid(row=5,column=1)

button_explore = Button(Message_paragraphe, text="Select A Picture/Pdf",width=16, command=browse_file)
button_explore.grid(row=6,column=2)

global Entry_chemin
Entry_chemin = Entry(Message_paragraphe, bg="white",fg="black", highlightthickness=1 ,font=("Arial",12),width=20)
Entry_chemin.grid(row=7,column=2)

Frame(Message_paragraphe,bg='#414C7B',height=20).grid(row=8,column=1)

Button(Message_paragraphe,text="Hide",bg='white',fg='black',command=hidetkinter,width=5).grid(row=9,column=2)

Message_paragraphe.pack()

Frame(window,bg="#414C7B",height=13).pack()
Frame(window,bg="#FFFFFF",width=500,height=4).pack()

Dercypt_frame = Frame(window,bg="#414C7B") 

Frame(Dercypt_frame,bg="#414C7B",width=30,height=3).grid(row=0,column=0)
Frame(Dercypt_frame,bg="#414C7B",width=300,height=3).grid(row=0,column=3)
Label(Dercypt_frame,bg="#414C7B",text="Image Modify :    ",font=("Arial",15)).grid(row=1,column=0)
Frame(Dercypt_frame,bg="#414C7B",width=300,height=5).grid(row=2,column=3)
button_explore = Button(Dercypt_frame, text="Select A Picture/Pdf",width=16, command=browse_file2)
button_explore.grid(row=3,column=1)

global Entry_chemin_decrypt
Entry_chemin_decrypt = Entry(Dercypt_frame, bg="white",fg="black", highlightthickness=1 ,font=("Arial",12),width=20)
Entry_chemin_decrypt.grid(row=4,column=1)

Button(Dercypt_frame,text="Show",bg='white',fg='black',command=showtkinter,width=5).grid(row=5,column=3)

Dercypt_frame.pack()
window.mainloop()
