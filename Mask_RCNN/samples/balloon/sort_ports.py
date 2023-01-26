

def sort(tup):

    temp = tup
    temp = [list(ele) for ele in temp]

    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of
    # sublist lambda has been used

    minY = min(temp, key = lambda x: x[2])
    maxY = max(temp, key = lambda x: x[2])

    avg = (minY[2]+maxY[2])/2

    row_upper = []
    row_lower = []

    for item in temp:
        if item[2] > avg:
            row_lower.append(item)
        else:
            row_upper.append(item)

    row_upper.sort(key = lambda x: x[1])
    row_lower.sort(key = lambda x: x[1])


    rows = row_upper + row_lower

    for i in range(len(rows)):
        rows[i].append(i+1)


    rows.sort(key = lambda x: x[5])

    return rows