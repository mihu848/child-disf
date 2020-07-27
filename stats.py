import sys, argparse, os
import glob
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import minedit

#exports csv with filler data
def filler_rate(t1, name):
    first = pd.read_csv(t1, sep='\t')
    x=0
    tags = []
    fillct = []
    totct = []
    rate = []
    #for x in range(len(first)):
    while(x<len(first)):
        key = first.loc[x, "filename"]
        count = 0
        tot = 0
        while(x<len(first) and first.loc[x, "filename"]==key):
            f=first.loc[x, "filler"]
            if(f==1):
                count+=1
                tot+=1
            else:
                tot+=1
            x+=1
        print(key)
        tags.append(key)
        print("Fillers: " + str(count))
        fillct.append(count)
        print("Total Tokens: " + str(tot))
        totct.append(tot)
        print("Filler rate: " + str(count/tot*100)+"%")
        rate.append(count/tot)
        x+=1
    df = pd.DataFrame(list(zip(tags,fillct,totct,rate)),
                      columns = ["filename", "fillers", "tokens", "rate"])
    outfile = name + ".tsv"
    df.to_csv(outfile, sep="\t", index=False)


#exports csv with disf/reparandum data
def disf_rate(t1, name):
    first = pd.read_csv(t1, sep='\t')
    x=0
    tags = []
    disfct = []
    totct = []
    rate = []
    while(x<len(first)):
        key = first.loc[x, "filename"]
        count = 0
        tot = 0
        while(x<len(first) and first.loc[x, "filename"]==key):
            f=first.loc[x, "disf"]
            if(f==1):
                count+=1
                tot+=1
            else:
                tot+=1
            x+=1
        print(key)
        tags.append(key)
        print("Disfluencies: " + str(count))
        disfct.append(count)
        print("Total Tokens: " + str(tot))
        totct.append(tot)
        print("Disfluency rate: " + str(count/tot*100)+"%")
        rate.append(count/tot)
        x+=1
    df = pd.DataFrame(list(zip(tags,disfct,totct,rate)),
                      columns = ["filename", "disfluencies", "tokens", "disfrate"])
    outfile = name + ".tsv"
    df.to_csv(outfile, sep="\t", index=False)


#percentage of tokens involved in repair
def rep_rate(t1, name):
    first = pd.read_csv(t1, sep='\t')
    x=0
    tags = []
    disfct = []
    totct = []
    rate = []
    while(x<len(first)):
        key = first.loc[x, "filename"]
        count = 0
        tot = 0
        while(x<len(first) and first.loc[x, "filename"]==key):
            f=first.loc[x, "level"]
            if(f>=1):
                count+=1
                tot+=1
            else:
                tot+=1
            x+=1
        print(key)
        tags.append(key)
        print("Repair Tokens: " + str(count))
        disfct.append(count)
        print("Total Tokens: " + str(tot))
        totct.append(tot)
        print("Repair rate: " + str(count/tot*100)+"%")
        rate.append(count/tot)
        x+=1
    df = pd.DataFrame(list(zip(tags,disfct,rate,totct)),
                       columns = ["filename", "repairsegs", "reprate", "tokens"])
    outfile = name + ".tsv"
    df.to_csv(outfile, sep="\t", index=False)

#reads in master tsv, generates data column averaged by gender
def gender_stat(t1,col):
    df = pd.read_csv(t1, sep='\t')
    males = 0
    females = 0
    m_stat = 0
    f_stat = 0
    for x in range(len(df)):
        if(df.loc[x, "gender"]=="M"):
            m_stat+=df.loc[x, col]
            males+=1
        else:
            f_stat+=df.loc[x, col]
            females+=1
    print("Male " + col +": "+ str(m_stat/males) + " across " + str(males)+ " subjects")
    print("Female " + col +": " + str(f_stat/females) + " across " + str(females)+ " subjects")
    
#graph two data columns against each other    
def graph(t1,a1,a2,x_label="x",y_label="y"):
    if(x_label == "x"):
        x_label=a1
    if(y_label == "y"):
        y_label=a2  
    df= pd.read_csv(t1, sep='\t')
    x = df.loc[:,a1]
    y = df.loc[:,a2]
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(y_label+" vs. "+x_label)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
    predict_y = intercept + slope * x
    plt.plot(x,predict_y, color = "red")
    plt.plot(x, y, 'o', color='blue')
    print("Linear R Value: " + str(r_value))

#function to return minimum edit distance
def med(x,y):
    return minedit.WagnerFischer(x,y).cost

#parse reparandums
def parse_repar(t1, x):
    df=pd.read_csv(t1, sep='\t')
    tup = ["", x]
    while(df.loc[tup[1],"boundary"] != "+" and df.loc[tup[1],"boundary"] != "+_/" and df.loc[tup[1],"boundary"] != "+_//"):
        if(df.loc[tup[1],"token"]!="<inaudible>"):
            tup[0]+=df.loc[tup[1],"token"]+" "
        tup[1]+=1
    if(df.loc[tup[1],"token"]!="<inaudible>"):
        tup[0] += df.loc[tup[1],"token"]
    return tup #return reparandum and index number

def parse_repair(t1,x):
    df=pd.read_csv(t1, sep='\t')
    tup = ["", x]
    while(df.loc[tup[1]+1,"level"] != 0):
        if(df.loc[tup[1],"token"]!="<inaudible>"):
            tup[0]+=df.loc[tup[1],"token"]+" "
        tup[1]+=1
    if(df.loc[tup[1],"token"]!="<inaudible>"):
        tup[0] += df.loc[tup[1],"token"]
    return tup #return reparandum and index number
#generate per ID statistics on minimum edit distance between reparandums and repairs, also counts false starts, exports in tsv (wip)
def min_edit(t1):
    df = pd.read_csv(t1, sep='\t')
    tags = []
    disf = []
    rep = []
    med_v = []
    fs = []
    tok = []
    x=0
    while (x < len(df)):
        repar=""
        repair=""
        if(df.loc[x,"disf"]==1): #catch reparandum
            tup=parse_repar(t1,x)
            repar=tup[0]
            x=tup[1]
            if(df.loc[x+1,"level"]==0): #false start
                tags.append(df.loc[x,"filename"])
                disf.append(repar)
                rep.append("0")
                med_v.append("-1")
                fs.append("yes")
                tok.append(x)
                x+=1
            elif(df.loc[x+1,"disf"]==1):#multiple repairs in a row
                tags.append(df.loc[x,"filename"])
                tup = parse_repar(t1,x+1)
                repair = tup[0]
                disf.append(repar)
                rep.append(repair)
                med_v.append(med(repar,repair))
                fs.append("no")
                tok.append(x)
                x+=1
            elif(df.loc[x+1,"disf"]==0): #one reparandum one repair
                tags.append(df.loc[x,"filename"])
                tup = parse_repair(t1, x+1)
                repair=tup[0]
                x=tup[1]
                disf.append(repar)
                rep.append(repair)
                med_v.append(med(repar,repair))
                fs.append("no")
                tok.append(x)
                x+=1
        else:
            x+=1
            
    fin = pd.DataFrame(list(zip(tags,disf,rep,med_v,fs,tok)),
                       columns = ["filename", "reparandum", "repair", "minedit","false start","token number"])
    fin.to_csv("minimumedit.tsv", sep="\t", index=False)
            
            
            
            
            
            
