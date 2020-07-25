import sys, argparse, os
import glob
import pandas as pd 
import numpy as np
from collections import Counter

#check that word level transcriptions match
def check_tokens(t1, t2): #t1 and t2 are names of files to read from
    first = pd.read_csv(t1, sep='\t')
    sec = pd.read_csv(t2, sep='\t')
    #check token count first
    f_rows = len(first)
    s_rows = len(sec)
    if(f_rows!=s_rows):
        print("Number of tokens are different.")
    else:
        print("Number of tokens are the same.")
    r = max(f_rows, s_rows)
    for x in range(r):
        if(first.loc[x, "token"]!=sec.loc[x,"token"]):
            print("Token error at Position: "+str(x))
            print("Transcription: " + first.loc[x,"filename"])
            print('First file says: "'+first.loc[x, "token"]+'" and second file says: "'+sec.loc[x,"token"]+'"')
            return 
    print("Token Contents All Match!")
    return

#return array index based on boundary marking type
def b_index(f):
    if (f == '/'):
        return 0 
    elif (f == '+'):
        return 1  
    elif (f == '//'):
        return 2
    elif (f == "None"):
        return 3
    elif (f == '{H}'):
        return 4
    elif (f == '{PBC}'):
        return 5
    return -1

#generate confusion matrix
def kappa_arr(t1,t2):
    first = pd.read_csv(t1, sep='\t')
    sec = pd.read_csv(t2, sep='\t')
    k = np.array([[0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0],
                 [0,0,0,0,0,0]])
    for x in range(len(first)):
        f=first.loc[x, "boundary"]
        s=sec.loc[x, "boundary"]
        if(f==s):
            if("_" in f):
                u = f.find("_")
                seg = f[0:u]
                i=b_index(seg)
                k[i][i]=k[i][i]+1
                f=f[u+1]
            i=b_index(f)
            k[i][i]=k[i][i]+1
        else:
            if("_" in f and not ("_" in s)):
                u = f.find("_")
                seg = f[0:u]
                i=b_index(seg)
                j=b_index(s)
                k[i][j]=k[i][j]+1
                f=f[u+1]
            elif("_" in s and not ("_" in f)):
                u = s.find("_")
                seg = s[0:u]
                i=b_index(f)
                j=b_index(seg)
                k[i][j]=k[i][j]+1
                s=s[u+1]
            elif("_" in s and "_" in f):
                u = f.find("_")
                v = s.find("_")
                seg1 = f[0:u]
                seg2 = f[0:v]
                i=b_index(seg1)
                j=b_index(seg2)
                k[i][j]=k[i][j]+1
                f=f[u+1]
                s=s[v+1]      
            i=b_index(f)
            j=b_index(s)
            k[i][j]=k[i][j]+1
    return k;

    
    
    