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


#compare reparandum length to repair length


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
  #  p=np.polyfit(x,y,2)
  #  f=np.poly1d(p)
 #   plt.plot(x,f(x), color="blue")
    plt.plot(x,predict_y, color = "red")
    plt.plot(x, y, 'o', color='black')
    print("Linear R Value: " + str(r_value))
    
#generate per ID statistics on minimum edit distance between reparandums and repairs
def min_edit(t1):
    df = pd.read_csv(t1, sep='\t')
    
    x="Asd"
    y="Asdsd"
    return minedit.WagnerFischer(x,y).cost