Tasks = [75,76,150,196,201,229,90,100,200,101,188,216,176,83,230,159,185,191,122,163]
workers = 6
workerstasks = [[]for i in range(workers)]
for i in range(workers):
    workerstasks[i].append(Tasks[i])
for i in range(workers,len(Tasks)):
    timetotal = []
    for j in range(len(workerstasks)):
        time = sum(workerstasks[j])
        timetotal.append(time)
        nexttask = min(timetotal)
    for k in range(len(workerstasks)):
        if sum(workerstasks[k]) == nexttask:
            workerstasks[k].append(Tasks[i])
timetotal = []
for j in range(len(workerstasks)):
        time = sum(workerstasks[j])
        timetotal.append(time)
print(timetotal)
#if all(i < 600 for i in timetotal):
#    print(workers)
#else:
#    workers = workers + 1
    

    
    
