def plc1_check_offline(future_state,HMI,plc1_delay_set):
    a = True
    b = True
    if plc1_delay_set[0]<0:
        plc1_delay_set[0]=0
    if plc1_delay_set[1]<0:
        plc1_delay_set[1]=0
    if future_state[0]==1:
        a= (HMI.MV101.Status == 2)
    if future_state[1]==1:
        b= (HMI.MV101.Status==1)
        # print (b)
    if future_state[2] == 1:
        c = (HMI.P101.Status == 2)
        # print (c)
    else:
        c = (HMI.P101.Status == 1)
        # print (c)
    if future_state[3] == 1:
        d = (HMI.P102.Status== 2)
        print (d)
    else:
        d = (HMI.P102.Status == 1)
        # print (d)
    if not (a and b):
        plc1_delay_set[0]=plc1_delay_set[0]+1
    else:
        plc1_delay_set[0]=plc1_delay_set[0]-1
    if not c:
        plc1_delay_set[1]=plc1_delay_set[1]+1
    else:
        plc1_delay_set[1] = plc1_delay_set[1] - 1

    # if not d:
    #     print ("p102 is abnormal")
    #     print (HMI.P102.Status)
    #     return False
    if plc1_delay_set[0]>8:
        print ("MV101 is abnormal")
        return False

    if plc1_delay_set[1]>1:
        print ("p101 is abnormal")
        return False
    return True



def plc2_check_offline(future_state,HMI,plc2_delay_set):
    a = True
    b = True
    if plc2_delay_set[0]<0:
        plc2_delay_set[0]=0
    if plc2_delay_set[1]<0:
        plc2_delay_set[1]=0
    if plc2_delay_set[2]<0:
        plc2_delay_set[2]=0
    if plc2_delay_set[3]<0:
        plc2_delay_set[3]=0

    if future_state[0]==1:
        a= (HMI.MV201.Status == 2)
    if future_state[1]==1:
        b= (HMI.MV201.Status==1)


    if future_state[2] == 1:
        c = (HMI.P201.Status == 2)
    else:
        c = (HMI.P201.Status == 1)
    if future_state[3] == 1:
        d = (HMI.P202.Status== 2)
    else:
        d = (HMI.P202.Status == 1)

    if future_state[4] == 1:
        e = (HMI.P203.Status == 2)
    else:
        e = (HMI.P203.Status == 1)
    if future_state[5] == 1:
        f = (HMI.P204.Status== 2)
    else:
        f = (HMI.P204.Status == 1)

    if future_state[6] == 1:
        g = (HMI.P205.Status == 2)
    else:
        g = (HMI.P205.Status == 1)
    if future_state[7] == 1:
        h = (HMI.P206.Status== 2)
    else:
        h = (HMI.P206.Status == 1)

    if not (a and b):
        plc2_delay_set[0]=plc2_delay_set[0]+1
    else:
        plc2_delay_set[0]=plc2_delay_set[0]-1
    if not c:
        plc2_delay_set[1]=plc2_delay_set[1]+1
    else:
        plc2_delay_set[1]=plc2_delay_set[1]-1

    if not e:
        plc2_delay_set[2] = plc2_delay_set[2] + 1
    else:
        plc2_delay_set[2] = plc2_delay_set[2] - 1
    # if not f:
    #     print ("p204 is abnormal")
    #     return False
    if not g:
        plc2_delay_set[3] = plc2_delay_set[3] + 1
    else:
        plc2_delay_set[3] = plc2_delay_set[3] - 1
    # if not h:
    #     print ("p206 is abnormal")
    #     return False
    if plc2_delay_set[0]>8:
        print ("mv201 is abnormal")
        return False
    if plc2_delay_set[1]>1:
        print ("p201 is abnormal")
        return False
    if plc2_delay_set[2]>1:
        print ("p203 is abnormal")
        return False
    if plc2_delay_set[3]>1:
        print ("p205 is abnormal")
        return False
    return True


def plc3_check_offline(future_state,HMI,plc3_delay_set):
    if plc3_delay_set[0]<0:
        plc3_delay_set[0]=0
    if plc3_delay_set[1]<0:
        plc3_delay_set[1]=0
    if plc3_delay_set[2]<0:
        plc3_delay_set[2]=0
    if plc3_delay_set[3]<0:
        plc3_delay_set[3]=0
    if plc3_delay_set[4]<0:
        plc3_delay_set[4]=0
    a = True
    b = True
    c = True
    d = True
    e = True
    f = True
    g = True
    h = True
    if future_state[0]==1:
        a= (HMI.MV301.Status == 2)
    if future_state[1]==1:
        b= (HMI.MV301.Status==1)
    if future_state[2]==1:
        c= (HMI.MV302.Status == 2)
    if future_state[3]==1:
        d= (HMI.MV302.Status==1)
    if future_state[4]==1:
        e= (HMI.MV303.Status == 2)
    if future_state[5]==1:
        f= (HMI.MV303.Status==1)
    if future_state[6]==1:
        g= (HMI.MV304.Status == 2)
    if future_state[7]==1:
        h= (HMI.MV304.Status==1)
    if future_state[8] == 1:
        i = (HMI.P301.Status == 2)
    else:
        i = (HMI.P301.Status == 1)
    if future_state[9] == 1:
        j = (HMI.P302.Status== 2)
    else:
        j = (HMI.P302.Status == 1)

    if not (a and b):
        plc3_delay_set[0] = plc3_delay_set[0] + 1
    else:
        plc3_delay_set[0] = plc3_delay_set[0] - 1

    if not (c and d):
        plc3_delay_set[1] = plc3_delay_set[1] + 1
    else:
        plc3_delay_set[1] = plc3_delay_set[1] - 1

    if not (e and f):
        plc3_delay_set[2] = plc3_delay_set[2] + 1
    else:
        plc3_delay_set[2] = plc3_delay_set[2] - 1

    if not (g and h):
        plc3_delay_set[3] = plc3_delay_set[3] + 1
    else:
        plc3_delay_set[3] = plc3_delay_set[3] - 1

    if not i:
        plc3_delay_set[4] = plc3_delay_set[4] + 1
    else:
        plc3_delay_set[4] = plc3_delay_set[4] - 1
    # if not j:
    #     print ("p302 is abnormal")
    #     return False
    if plc3_delay_set[0]>8:
        print ("mv301 is abnormal")
        return False
    if plc3_delay_set[1]>8:
        print ("mv302 is abnormal")
        return False
    if plc3_delay_set[2]>8:
        print ("mv303 is abnormal")
        return False
    if plc3_delay_set[3]>8:
        print ("mv304 is abnormal")
        return False
    if plc3_delay_set[4]>1:
        print ("p301 is abnormal")
        return False
    return True




def plc4_check_offline(future_state,HMI,plc4_delay_set):
    if plc4_delay_set[0]<0:
        plc4_delay_set[0]=0

    if plc4_delay_set[1]<0:
        plc4_delay_set[1]=0

    if plc4_delay_set[2]<0:
        plc4_delay_set[2]=0

    if future_state[0] == 1:
        a = (HMI.P401.Status == 2)
    else:
        a = (HMI.P401.Status == 1)


    if future_state[1] == 1:
        b = (HMI.P402.Status == 2)
    else:
        b = (HMI.P402.Status == 1)

    if future_state[2] == 1:
        c = (HMI.P403.Status == 2)
    else:
        c = (HMI.P403.Status == 1)

    if future_state[3] == 1:
        d = (HMI.P404.Status == 2)
    else:
        d = (HMI.P404.Status == 1)

    # if future_state[4] == 1:
    #     e = (HMI.UV401.Status == 2)
    # else:
    #     e = (HMI.UV401.Status == 1)
    e= (HMI.UV401.Status==HMI.P401.Status)
    if not a:
        plc4_delay_set[0]=plc4_delay_set[0]+1
    else:
        plc4_delay_set[0]=plc4_delay_set[0]-1
    # if not b:
    #     print ("p402 is abnormal")
    #     return False
    if not c:
        plc4_delay_set[1] = plc4_delay_set[1] + 1
    else:
        plc4_delay_set[1] = plc4_delay_set[1] - 1
    # if not d:
    #     print ("p404 is abnormal")
    #     return False
    if not e:
        plc4_delay_set[2] = plc4_delay_set[2] + 1
    else:
        plc4_delay_set[2] = plc4_delay_set[2] - 1

    if plc4_delay_set[0]>1:
        print ("p401 is abnormal")
        return False

    if plc4_delay_set[1]>1:
        print ("p403 is abnormal")
        return False

    if plc4_delay_set[2]>6:
        print ("uv401 is abnormal")
        return False
    return True



# def plc5_check_offline(future_state,HMI):
#     a = True
#     b = True
#     c = True
#     d = True
#     e = True
#     f = True
#     g = True
#     h = True
#     if future_state[0] == 1:
#         a = (HMI.MV501.Status == 2)
#     if future_state[1] == 1:
#         b = (HMI.MV501.Status == 1)
#     if future_state[2] == 1:
#         c = (HMI.MV502.Status == 2)
#     if future_state[3] == 1:
#         d = (HMI.MV502.Status == 1)
#     if future_state[4] == 1:
#         e = (HMI.MV503.Status == 2)
#     if future_state[5] == 1:
#         f = (HMI.MV503.Status == 1)
#     if future_state[6] == 1:
#         g = (HMI.MV504.Status == 2)
#     if future_state[7] == 1:
#         h = (HMI.MV504.Status == 1)
#
#     if not (a and b):
#         print("mv501 is abnormal")
#         return False
#
#     if not (c and d):
#         print("mv502 is abnormal")
#         return False
#
#     if not (e and f):
#         print("mv503 is abnormal")
#         return False
#
#     if not (g and h):
#         print("mv504 is abnormal")
#         return False
#
#     return True

