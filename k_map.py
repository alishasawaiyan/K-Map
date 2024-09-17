#THIS PROGRAM IS CREATED FOR SOLVING KARNAUGH MAP FOR ANY NUMBER OF VARIABLES

def mul(x,y): 
    res = []
    for i in x:
        if i+"'" in y or (len(i)==2 and i[0] in y):
            return []
        else:
            res.append(i)
    for i in y:
        if i not in res:
            res.append(i)
    return res

def multiply(x,y):
    res = []
    for i in x:
        for j in y:
            tmp = mul(i,j)
            res.append(tmp) if len(tmp) != 0 else None
    return res

def refine(my_list,dc_list): 
    res = []
    for i in my_list:
        if int(i) not in dc_list:
            res.append(i)
    return res

def findEPI(x): 
    res = []
    for i in x:
        if len(x[i]) == 1:
            res.append(x[i][0]) if x[i][0] not in res else None
    return res

def sumExpression(x):
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
           var_list.append(chr(i+65)+"'")
        elif x[i] == '1':
           var_list.append(chr(i+65))
    a=('('+'+'.join(''.join(i) for i in var_list)+')')
    return a

def findVariables(x): 
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(chr(i+65)+"'")
        elif x[i] == '1':
            var_list.append(chr(i+65))
    return var_list

def flatten(x): 
    flattened_items = []
    for i in x:
        flattened_items.extend(x[i])
    return flattened_items

def findterms(a): 
    gaps = a.count('-')
    if gaps == 0:
        return [str(int(a,2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2,gaps))]
    temp = []
    for i in range(pow(2,gaps)):
        temp2,ind = a[:],-1
        for j in x[0]:
            if ind != -1:
                ind = ind+temp2[ind+1:].find('-')+1
            else:
                ind = temp2[ind+1:].find('-')
            temp2 = temp2[:ind]+j+temp2[ind+1:]
        temp.append(str(int(temp2,2)))
        x.pop(0)
    return temp

def compare(a,b): 
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            mismatch_index = i
            c += 1
            if c>1:
                return (False,None)
    return (True,mismatch_index)

def removeTerms(_chart,terms): 
    for i in terms:
        for j in findterms(i):
            try:
                del _chart[j]
            except KeyError:
                pass

def SOP():
    mit = [int(i) for i in input("\nEnter the minterms: ").strip().split()]
    dc = [int(i) for i in input("\nEnter the don't cares(If any): ").strip().split()]
    mit.sort()
    minterms = mit+dc
    minterms.sort()
    groups,all_pi = {},set()


    for minterm in minterms:
        try:
           groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
        except KeyError:
           groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]

    while True:
        tmp = groups.copy()
        groups,m,marked,should_stop = {},0,set(),True
        l = sorted(list(tmp.keys()))
        for i in range(len(l)-1):
            for j in tmp[l[i]]: 
                for k in tmp[l[i+1]]: 
                    res = compare(j,k) 
                    if res[0]: 
                        try:
                           groups[m].append(j[:res[1]]+'-'+j[res[1]+1:]) if j[:res[1]]+'-'+j[res[1]+1:] not in groups[m] else None 
                        except KeyError:
                            groups[m] = [j[:res[1]]+'-'+j[res[1]+1:]] 
                        should_stop = False
                        marked.add(j) 
                        marked.add(k) 
            m += 1
        local_unmarked = set(flatten(tmp)).difference(marked) 
        all_pi = all_pi.union(local_unmarked)
        if should_stop: 
           
           break
    
    sz = len(str(mit[-1])) 
    chart = {}
    
    for i in all_pi:
        merged_minterms,y = findterms(i),0
        
        for j in refine(merged_minterms,dc):
            x = mit.index(int(j))*(sz+1) 
           
            y = x+sz
            try:
               chart[j].append(i) if i not in chart[j] else None 
            except KeyError:
               chart[j] = [i]
    
    EPI = findEPI(chart) 
    
    removeTerms(chart,EPI) 

    if(len(chart) == 0): # If no minterms remain after removing EPI related columns
      final_result = [findVariables(i) for i in EPI]
    else: 
        P = [[findVariables(j) for j in chart[i]] for i in chart]
        while len(P)>1: 
           P[1] = multiply(P[0],P[1])
           P.pop(0)
        final_result = [min(P[0],key=len)] 
        final_result.extend(findVariables(i) for i in EPI) 
    print('\nSolution F=')
    print(''+' + '.join(''.join(i) for i in final_result))

def POS():
    mat = [int(i) for i in input("\nEnter the maxterms: ").strip().split()]
    dc = [int(i) for i in input("\nEnter the don't cares(If any): ").strip().split()]
    mat.sort()
    maxterms = mat+dc
    maxterms.sort()
    groups,all_pi = {},set()


    for maxterm in maxterms:
        try:
           groups[bin(maxterm).count('1')].append(bin(maxterm)[2:].zfill(size))
        except KeyError:
           groups[bin(maxterm).count('1')] = [bin(maxterm)[2:].zfill(size)]

    while True:
        tmp = groups.copy()
        groups,m,marked,should_stop = {},0,set(),True
        l = sorted(list(tmp.keys()))
        for i in range(len(l)-1):
            for j in tmp[l[i]]: 
                for k in tmp[l[i+1]]:
                    res = compare(j,k)
                    if res[0]:
                        try:
                           groups[m].append(j[:res[1]]+'-'+j[res[1]+1:]) if j[:res[1]]+'-'+j[res[1]+1:] not in groups[m] else None 
                        except KeyError:
                            groups[m] = [j[:res[1]]+'-'+j[res[1]+1:]] 
                        should_stop = False
                        marked.add(j) 
                        marked.add(k) 
            m += 1
        local_unmarked = set(flatten(tmp)).difference(marked)
        all_pi = all_pi.union(local_unmarked)
        if should_stop:
           
           break
    
    sz = len(str(mat[-1])) 
    chart = {}
    
    for i in all_pi:
        merged_maxterms,y = findterms(i),0
        
        for j in refine(merged_maxterms,dc):
            x = mat.index(int(j))*(sz+1) 
           
            y = x+sz
            try:
               chart[j].append(i) if i not in chart[j] else None 
            except KeyError:
               chart[j] = [i]
    
    EPI = findEPI(chart) 
    
    removeTerms(chart,EPI) 

    if(len(chart) == 0):
      final_result = [sumExpression(i) for i in EPI]
    else: 
        P = [[sumExpression(j) for j in chart[i]] for i in chart]
        while len(P)>1: 
           P[1] = multiply(P[0],P[1])
           P.pop(0)
        final_result = [min(P[0],key=len)] 
        final_result.extend(sumExpression(i) for i in EPI) 
    print("\nSolution F= ")
    print(''.join(''.join(i) for i in final_result))

print("\n########## INSTRUCTIONS ##########")
print("\n1.You can select any number of variable you want for the k-map.")
print("\n2.You can choose whether you want to solve in SOP or POS form from the main menu")
print("\n3. While entering the minterms\maxterms\don't care values write in format[ 0 1 2 3 ]")

while True:
    size=int(input("\nEnter the number of variables: "))
    print("\n##### MAIN MENU #####")
    print("\n1.SOP\n2.POS\n3.End")
    choice=int(input("\nEnter your choice:"))

    if choice==1:
        SOP()
    elif choice==2:
        POS()
    elif choice==3:
        print("Thankyou")
        break
    else:
        print("\nWrong Choice")

input("\nPress enter to exit...")

