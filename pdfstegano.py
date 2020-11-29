import os; import time

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

global alphabet
alphabet=[]
for i in "apzoeirutyqm sldkfjghwnxbcvAMZLEçKRJTHYGFUDISOQPWNXBCV1907856432)è(@#:/=+/;,?.ù%$€*àé§&'" : alphabet.append(i)

def verif(doc,number_line) :
    total = 0
    for i in str(number_line) :
        total += len(doc[int(i)])
    print(total)
    return total

def Hide(name='.pdf',sentence='hello world',clef="azety") :
    if name == '.pdf' :
        return "MUST COMPLETED path or name"
    elif sentence == '' :
        return "MUST GIVE a sentence"
    if clef == '' :
        clef = "azerty"
    
    if True :
        final_name = str(name+'.txt')
        print(final_name)
        os.rename(name,final_name)
        number_line = 0
        doc = []
        for line in open(final_name, "rb") :
            doc.append(str(line[:-1])[2:-1])
            print(doc[-1])
            number_line += 1
        print(number_line)
        nb = str(number_line / 2).split('.')
        nb = int(nb[0]) - 2
        print(nb)
        print(doc[nb] ,".......")
        if str(doc[nb]) == '%' + str(verif(doc,number_line)) :
            print('doc deja codé')
            choix = input('Voulez vous détruitre l ancien message ? [Y/N] : ')
            choix = choix.lower()
        else :
            choix = 'y'
        if choix == 'y' :
            print('doc ok') 
            sentence = crypt(sentence,clef)
            message = '%' + str(sentence)
            os.system(f"echo '{message}' >> {final_name}")
            doc.append(message)
            number_line += 2
            nb = str(number_line / 2).split('.')
            nb = int(nb[0]) - 1
            doc.insert(nb, '%' + str(verif(doc,number_line)))
            print(doc[nb])
            nom = doc[nb]
            print(nom)
            final_name2 = str(final_name) + ".txt"
            os.system(f"sed $'{nb}i\\\n{nom}\n' {final_name} > {final_name2}")
            print(nb)
            print(nom)
            os.remove(final_name)
            os.rename(final_name2,name)
        else :
            os.rename(final_name,name)
        #os.system(f"echo '%{sentence}' >> {final_name} | cat {final_name}") #Ajoute la phrase à la fin
        
def Show(name='.pdf',clef="azety") :
    if name == '.pdf' :
        return "MUST COMPLETED path or name"
    if clef == '' :
        clef = "azerty"
  

    if True :
        final_name = str(name+'.txt')
        print(final_name)
        os.rename(name,final_name)
        number_line = 0
        doc = []
        for line in open(final_name, "rb") :
            doc.append(str(line[:-1])[2:-1])
            print(doc[-1])
            number_line += 1
        print(number_line)
        nb = str(number_line / 2).split('.')
        nb = int(nb[0]) - 2
        print(nb)
        print(doc[nb] ,".......")
        if str(doc[nb]) == '%' + str(verif(doc,number_line)) :
            print('doc ok')
            message = str(doc[-1])[1:]
            print(message)
            message = decrypt(message,clef)
            return message
        else :
            print('DOC NO ENCODED')
        os.rename(final_name,name)
if __name__ == "__main__":
    while True :
        t = 1
        ls_file = os.listdir()
        for i in ls_file  : print(t, i); t+=1
        n = input('name (number) :')
        name = ls_file[int(n)-1]
        print(name)
        sentence = input('sentence :')
        c = input('crypt :')
        Hide(name,sentence,c)
        Show(name,c)

        