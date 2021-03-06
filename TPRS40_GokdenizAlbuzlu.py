### Author : Albuzlu Gökdeniz
### https://github.com/GokdenizAlbuzlu?tab=repositories

import hashlib
import binascii

def home_mod_expnoent(x,y,n):                               #fonctionne !
     y=format(y, 'b')   #on transforme en binaire l'exposant 
     k=(len(y)) #longueur du bit
     R1=1       
     R2=x
     result=[]
     for i in range(0, len(y), 1):
        result.append(int(y[i : i + 1]))     #je stocke les bits de manière séparé dans un tableau
     for i in range(k-1,-1,-1):     #il faut faire attention ici on dit qu'on part de k-1 jusqu'a -1 car si on met 0, le 0 ne sera pas pris en compte, le troisième paramètre indique la décrementation de -1
         if result[i]==1:           #si le bit est égale à 1  
             R1=(R1*R2)%n           #alors voici ce qui se passe sinon on ne touche pas a R1
         R2=(R2*R2)%n               #R2 change tjrs de valeur
     return R1

def home_ext_euclide(y, b):  # algorithme d'euclide étendu pour la recherche de l'exposant secret
    (r,nouvr,t,nouvt)=(y,b,0,1)
    while nouvr>1:
        quotient=r//nouvr
        (r, nouvr) = (nouvr, r-quotient*nouvr)
        (t, nouvt) = (nouvt, t-quotient*nouvt)
    return nouvt%y

def home_pgcd(a,b): #recherche du pgcd
    if(b==0): 
        return a 
    else: 
        return home_pgcd(b,a%b)

def home_string_to_int(x): # pour transformer un string en int
    z=0
    for i in reversed(range(len(x))):
        z=int(ord(x[i]))*pow(2,(8*i))+z
    return(z)


def home_int_to_string(x): # pour transformer un int en string
    txt=''
    res1=x
    while res1>0:
        res=res1%(pow(2,8))
        res1=(res1-res)//(pow(2,8))
        txt=txt+chr(res)
    return txt

def home_crt(x, d, n, p, q):
    inverse_de_q = home_ext_euclide(q,1)
    dq = home_mod_expnoent(d,1,q-1)
    dp = home_mod_expnoent(d,1,p-1)
    mq = home_mod_expnoent(x,dq,q)
    mp = home_mod_expnoent(x,dp,p)
    h = home_mod_expnoent(((mp-mq)*inverse_de_q),1,p)
    return home_mod_expnoent(mq+ h*q,1,n)



def longueurMaximale(x1,x2): #entrer le secret
    i=1
    while(2**i<=(x1*x2)):
        i=i+1
    nbCaracteresMaxi= int (i/8)
    secret=input("donner un secret de "+str(nbCaracteresMaxi) + " caractères au maximum : ")
    while(len(secret)>i):
        secret=input("c'est beaucoup trop long,"+str(nbCaracteresMaxi)+" caractères S.V.P : ")
    return secret

#voici les éléments de la clé d'Alice

    
x1a=572893968095908224156641273272235974110556389295186601100659658050544231818716552181763155206915481714357753849464976409109410304421754286380610861629104805401835829261668319332494743147536185666695745506015380175593567985814392349536151282598299801700804090778691713892273202449021694122664123237181 #p
x2a=342873175679121135487538516693416555493179571558077832526185236543004155339492070905944209254461347692561795365046788161639057683708326774984141629822038482281581605457910453579769055768920760145228659260285668135381492321069743440808490662239348273714095702024298546562599200773677982328135008933283 #q
na=x1a*x2a  #n
phia=((x1a-1)*(x2a-1))//home_pgcd(x1a-1,x2a-1)
ea=65537 #exposant public
da=home_ext_euclide(phia,ea) #exposant privé
#voici les éléments de la clé de bob
x1b=117560218077710612362772614236489905395489287052882847954732348482373265562684303375006896359871436235281660015003552787359737427772942165944603531069962760743683373514194447824602851007726514980692851873726543795041436282559306478880981317979642020900732442323694760142864503869754189990698362594259 #p
x2b=693393881816451679586254034007530145024674089221890309739020889034015596615996084082867336194633311572478458098901764353237701865124154280749738811091023357776522423423060071317625481266128802008477796868284672647365335072622985125909717530124189840344811804757457109579277551827048878595263925152981 #q
nb=x1b*x2b # n
phib=((x1b-1)*(x2b-1))//home_pgcd(x1b-1,x2b-1)
eb=65537 # exposants public         //on change l'exposant public 
db=home_ext_euclide(phib,eb)        #exposant privé



print("Vous êtes Bob, vous souhaitez envoyer un secret à Alice")
print("voici votre clé publique que tout le monde a le droit de consulter")
print("n =",nb)
print("exposant :",eb)
print("voici votre précieux secret")
print("d =",db)
print("*******************************************************************")
print("Voici aussi la clé publique d'Alice que tout le monde peut conslter")
print("n =",na)
print("exposent :",ea)
print("*******************************************************************")
print("il est temps de lui envoyer votre secret ")
print("*******************************************************************")
x=input("appuyer sur entrer")
secret=longueurMaximale(x1b,x2b)
print("*******************************************************************")
print("voici la version en nombre décimal de ",secret," : ")
num_sec=home_string_to_int(secret)
print(num_sec)
print("voici le message chiffré avec la publique d'Alice : ")
chif=home_mod_expnoent(num_sec, ea, na)
print(chif)
print("*******************************************************************")
print("On utilise la fonction de hashage MD5 pour obtenir le hash du message",secret)
Bhachis0=hashlib.sha256(secret.encode(encoding='UTF-8',errors='strict')).digest() #SHA256 du message
print("voici le hash en nombre décimal ")
Bhachis1=binascii.b2a_uu(Bhachis0)
Bhachis2=Bhachis1.decode() #en string
Bhachis3=home_string_to_int(Bhachis2)
print(Bhachis3)
print("voici la signature avec la clé privée de Bob du hachis")
signe=home_mod_expnoent(Bhachis3, db, nb)
print(signe)
print("*******************************************************************")
print("Bob envoie \n \t 1-le message chiffré avec la clé public d'Alice \n",chif,"\n \t 2-et le hash signé \n",signe)
print("*******************************************************************")
x=input("appuyer sur entrer")
print("*******************************************************************")
print("Alice déchiffre le message chiffré \n",chif,"\nce qui donne ")
dechif=home_int_to_string(home_mod_expnoent(chif, da, na))
print(dechif)
print("*******************************************************************")
print("Alice déchiffre la signature de Bob \n",signe,"\n ce qui donne  en décimal")
designe= home_crt(signe, eb, nb, x1b, x2b)
print(designe)
print("Alice vérifie si elle obtient la même chose avec le hash de ",dechif)
Ahachis0=hashlib.sha256(dechif.encode(encoding='UTF-8',errors='strict')).digest()
Ahachis1=binascii.b2a_uu(Ahachis0)
Ahachis2=Ahachis1.decode()
Ahachis3=home_string_to_int(Ahachis2)
print(Ahachis3)
print("La différence =",Ahachis3-designe)
if (Ahachis3-designe==0):
    print("Alice : Bob m'a envoyé : ",dechif)
else:
    print("oups")

