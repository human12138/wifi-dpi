def funcList(Wlist):
    f = open('list1.txt','r')
    list1 = f.readlines()
    for ii in range(len(list1)):
        list1[ii] = list1[ii].rstrip('\n')
    resultList = []          
    print(type(list1))
    for i in Wlist:
        if i in list1:
            resultList.append(True)
        else:
            resultList.append(False)
    f.close()
    return resultList