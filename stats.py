import sys, argparse, os
import glob
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import minedit
import ntpath

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

#reads in master tsv, generates averaged data
def avg(t1,col):
    df = pd.read_csv(t1, sep='\t')
    subj = 0
    stat = 0
    for x in range(len(df)):
            stat+=df.loc[x, col]
            subj+=1
    print("Child " + col +": "+ str(stat/subj) + " across " + str(subj)+ " subjects")

#reads in master tsv, generates averaged data by gender
def gender_avg(t1,col):
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
        if(df.loc[tup[1],"token"]!="<inaudible>" and df.loc[tup[1],"filler"]==0):
            tup[0]+=df.loc[tup[1],"token"]+" "
        tup[1]+=1
    if(df.loc[tup[1],"token"]!="<inaudible>" and df.loc[tup[1],"filler"]==0):
        tup[0] += df.loc[tup[1],"token"]
    return tup #return reparandum and index number

def parse_repair(t1,x):
    df=pd.read_csv(t1, sep='\t')
    tup = ["", x]
    while(df.loc[tup[1]+1,"level"] != 0 and df.loc[tup[1]+1,"disf"]==0):
        if(df.loc[tup[1],"token"]!="<inaudible>" and df.loc[tup[1],"filler"]==0):
            tup[0]+=df.loc[tup[1],"token"]+" "
        tup[1]+=1
    if(df.loc[tup[1],"token"]!="<inaudible>" and df.loc[tup[1],"filler"]==0):
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
            
#exports csv with minimum edit/repair data
def med_rates(t1, name):
    first = pd.read_csv(t1, sep='\t')
    x=0
    tags = []
    fsct = []
    repeats = []
    avg_norep = []
    avg_wrep = []
    #for x in range(len(first)):
    while(x<len(first)):
        key = first.loc[x, "filename"]
        fs = 0
        min_tot = 0 #number of cases with MED value (no false starts)
        min_sum = 0 #sums up MED values
        reps = 0 #repeats (MED = 0)
        no_reps = 0 #count of MED cases without repeats 
        while(x<len(first) and first.loc[x, "filename"]==key):
            f=first.loc[x, "false start"]
            m=first.loc[x,"minedit"]
            if(f=="yes"):
                fs+=1
            else:
                if(m==0):
                    reps+=1
                    min_tot+=1
                else:
                    min_sum+=m
                    min_tot+=1
                    no_reps+=1
            x+=1
            
        print(key)
        tags.append(key)
        print("False Starts: " + str(fs))
        fsct.append(fs)
        print("Repeats: " + str(reps))
        repeats.append(reps)
        if(min_tot!=0):
            if(no_reps!=0):
                print("Average Minimum Edit Distance without Repeats: " + str(min_sum/no_reps))
                avg_norep.append(min_sum/no_reps)
            else:
                print("Average Minimum Edit Distance without Repeats: N/A")
                avg_norep.append(-1)
            print("Average Minimum Edit Distance with Repeats: " + str(min_sum/min_tot))
            avg_wrep.append(min_sum/min_tot)
        else:
            avg_norep.append(-1)
            avg_wrep.append(-1)
    df = pd.DataFrame(list(zip(tags,fsct,repeats,avg_norep,avg_wrep)),
                      columns = ["filename", "false starts", "repeats", "med avg (no repeats)", "med avg (with repeats)"])
    outfile = name + ".tsv"
    df.to_csv(outfile, sep="\t", index=False)        
            
            
#add age/gender information from master csv          
def add_demo(t1,master):
    df = pd.read_csv(t1, sep='\t')
    mas = pd.read_csv(master,sep='\t')
    ages = []
    gender = []
    x=0
    y=0
    while (x < len(df) and y < len(mas)):
        if(mas.loc[y,"filename"]==df.loc[x,"filename"]):
            ages.append(mas.loc[y,"age"])
            gender.append(mas.loc[y,"gender"])
            x+=1
            y+=1
        else:
            y+=1
    df["age"]=ages
    df["gender"]=gender
    df.to_csv(ntpath.basename(t1),sep='\t',index=False)
           
        
