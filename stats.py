
import sys, argparse, os
import glob
import pandas as pd 
import numpy as np
import csv
from collections import Counter

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

#reads in tsv, generates filler statistics by gender
def gender_filler(t1):
    df = pd.read_csv(t1, sep='\t')
    males = 0
    females = 0
    m_fill = 0
    f_fill = 0
    for x in range(len(df)):
        if(df.loc[x, "gender"]=="M"):
            m_fill+=df.loc[x, "fillrate"]
            males+=1
        else:
            f_fill+=df.loc[x, "fillrate"]
            females+=1
    print("Male Filler Rate: " + str(m_fill/males) + " across " + str(males)+ " subjects")
    print("Female Filler Rate: " + str(f_fill/females) + " across " + str(females)+ " subjects")