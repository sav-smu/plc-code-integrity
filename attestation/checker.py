def checker(P1,P2,P3,P4,P5,P6):
    pass


def model_checker(model,P1,P2,P3,P4,P5,P6):
    pass


def plc1_checker_status_offline(DO,df,timestep,index):
    # plc1_output_vector = [P1.MV101.DO_Open, P1.MV101.DO_Close, P1.P101.DO_Start, P1.P102.DO_Start]
    a = True
    b = True
    c = True
    d = True
    if DO[0]==1:
        a=(df.loc[index + timestep, 'MV101.Status']==2)
        # print (a)
    if DO[1]==1:
        b=(df.loc[index + timestep, 'MV101.Status']==1)
        # print (b)
    if DO[2] == 1:
        c = (df.loc[index + timestep, 'P101.Status'] == 2)
        # print (c)
    else:
        c = (df.loc[index + timestep, 'P101.Status'] == 1)
        # print (c)
    if DO[3] == 1:
        d = (df.loc[index + timestep, 'P102.Status'] == 2)
        # print (d)
    else:
        d = (df.loc[index + timestep, 'P102.Status'] == 1)
        # print (d)
    if not (a and b and c and d):
        # print ("PLC1 may be under attacked")
        return 1
    else:
        return 0


def plc1_check_online(future_state,HMI):
    a = True
    b = True
    c = True
    d = True
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
        # print (d)
    else:
        d = (HMI.P102.Status == 1)
        # print (d)
    if not (a and b):
        print ("mv101 is abnormal")
        return False
    if not c:
        print ("p101 is abnormal")
        return False
    if not d:
        print ("p102 is abnormal")
        return False

    return True

def plc1_publish(future_state,HMI,oa,time):
    a = True
    b = True
    t1=True
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
        # print (d)
    else:
        d = (HMI.P102.Status == 1)
        # print (d)
    data = {
        "MV101": {
        "actual": HMI.MV101.Status,
        "is_anomaly": (a and b),
        "predicted": future_state[0]+1,
        "process": "PLC1"},

        "P101": {
            "actual": HMI.P101.Status,
            "is_anomaly": c,
            "predicted": future_state[2]+1,
            "process": "PLC1"},

        "P102": {
            "actual": HMI.P102.Status,
            "is_anomaly": d,
            "predicted": future_state[3]+1,
            "process": "PLC1"}
    }
    oa.publish_prediction(
        time,
        data,
    )


def plc2_check_online(future_state,HMI):
    a = True
    b = True
    # [P2.MV201.DO_Open, P2.MV201.DO_Close, P2.P201.DO_Start, P2.P202.DO_Start, P2.P203.DO_Start, P2.P204.DO_Start,
    #  P2.P205.DO_Start, P2.P206.DO_Start]
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
        print ("mv201 is abnormal")
        return False
    if not c:
        print ("p201 is abnormal")
        return False
    if not d:
        print ("p202 is abnormal")
        return False
    if not e:
        print ("p203 is abnormal")
        return False
    if not f:
        print ("p204 is abnormal")
        return False
    if not g:
        print ("p205 is abnormal")
        return False
    if not h:
        print ("p206 is abnormal")
        return False
    return True

def plc2_publish(future_state,HMI,oa,time):
    a = True
    b = True
    # [P2.MV201.DO_Open, P2.MV201.DO_Close, P2.P201.DO_Start, P2.P202.DO_Start, P2.P203.DO_Start, P2.P204.DO_Start,
    #  P2.P205.DO_Start, P2.P206.DO_Start]
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
    data = {
        "MV201": {
        "actual": HMI.MV201.Status,
        "is_anomaly": (a and b),
        "predicted": future_state[0]+1,
        "process": "PLC2"},

        "P201": {
            "actual": HMI.P201.Status,
            "is_anomaly": c,
            "predicted": future_state[2]+1,
            "process": "PLC2"},

        "P202": {
            "actual": HMI.P202.Status,
            "is_anomaly": d,
            "predicted": future_state[3]+1,
            "process": "PLC2"},

        # "P203": {
        #     "actual": HMI.P203.Status,
        #     "is_anomaly": e,
        #     "predicted": future_state[4] + 1,
        #     "process": "PLC2"},
        #
        # "P204": {
        #     "actual": HMI.P204.Status,
        #     "is_anomaly": f,
        #     "predicted": future_state[5] + 1,
        #     "process": "PLC2"},
        "P205": {
            "actual": HMI.P205.Status,
            "is_anomaly": g,
            "predicted": future_state[6] + 1,
            "process": "PLC2"},

        "P206": {
            "actual": HMI.P206.Status,
            "is_anomaly": h,
            "predicted": future_state[7] + 1,
            "process": "PLC2"}
    }


    oa.publish_prediction(
        time,
        data,
    )

def plc3_check_online(future_state,HMI):
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
        print ("mv301 is abnormal")
        return False

    if not (c and d):
        print ("mv302 is abnormal")
        return False

    if not (e and f):
        print ("mv303 is abnormal")
        return False

    if not (g and h):
        print ("mv304 is abnormal")
        return False

    if not i:
        print ("p301 is abnormal")
        return False
    if not j:
        print ("p302 is abnormal")
        return False

    return True


def plc3_publish(future_state,HMI,oa,time):
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
    data = {
        "MV301": {
        "actual": HMI.MV301.Status,
        "is_anomaly": (a and b),
        "predicted": future_state[0]+1,
        "process": "PLC3"},

        "MV302": {
            "actual": HMI.MV301.Status,
            "is_anomaly": (c and d),
            "predicted": future_state[2]+1,
            "process": "PLC3"},

        "MV303": {
            "actual": HMI.MV303.Status,
            "is_anomaly": (e and f),
            "predicted": future_state[4]+1,
            "process": "PLC3"},

        "MV304": {
            "actual": HMI.MV304.Status,
            "is_anomaly": (g and h),
            "predicted": future_state[6] + 1,
            "process": "PLC3"},
        "P301": {
            "actual": HMI.P301.Status,
            "is_anomaly": i,
            "predicted": future_state[8] + 1,
            "process": "PLC3"},

        "P302": {
            "actual": HMI.P302.Status,
            "is_anomaly": j,
            "predicted": future_state[9] + 1,
            "process": "PLC3"},
    }
    oa.publish_prediction(
        time,
        data,
    )

def plc4_check_online(future_state,HMI):
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

    if future_state[4] == 1:
        e = (HMI.UV401.Status == 2)
    else:
        e = (HMI.UV401.Status == 1)
    if not a:
        print ("p401 is abnormal")
        return False
    if not b:
        print ("p402 is abnormal")
        return False
    if not c:
        print ("p403 is abnormal")
        return False
    if not d:
        print ("p404 is abnormal")
        return False


    return True


def plc4_publish(future_state,HMI,oa,time):
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

    data = {
        "P401": {
            "actual": HMI.P401.Status,
            "is_anomaly": a,
            "predicted": future_state[0]+1,
            "process": "PLC4"},

        "P402": {
            "actual": HMI.P402.Status,
            "is_anomaly": b,
            "predicted": future_state[1]+1,
            "process": "PLC4"},

        "P403": {
            "actual": HMI.P403.Status,
            "is_anomaly": c,
            "predicted": future_state[2] + 1,
            "process": "PLC4"},

        "P404": {
            "actual": HMI.P404.Status,
            "is_anomaly": d,
            "predicted": future_state[3] + 1,
            "process": "PLC4"}
    }
    oa.publish_prediction(
        time,
        data,
    )


def plc5_check_online(future_state,HMI):
    a = True
    b = True
    c = True
    d = True
    e = True
    f = True
    g = True
    h = True
    if future_state[0] == 1:
        a = (HMI.MV501.Status == 2)
    if future_state[1] == 1:
        b = (HMI.MV501.Status == 1)
    if future_state[2] == 1:
        c = (HMI.MV502.Status == 2)
    if future_state[3] == 1:
        d = (HMI.MV502.Status == 1)
    if future_state[4] == 1:
        e = (HMI.MV503.Status == 2)
    if future_state[5] == 1:
        f = (HMI.MV503.Status == 1)
    if future_state[6] == 1:
        g = (HMI.MV504.Status == 2)
    if future_state[7] == 1:
        h = (HMI.MV504.Status == 1)

    if not (a and b):
        print("mv501 is abnormal")
        return False

    if not (c and d):
        print("mv502 is abnormal")
        return False

    if not (e and f):
        print("mv503 is abnormal")
        return False

    if not (g and h):
        print("mv504 is abnormal")
        return False

    return True
# plc4_output_vector = [P4.P401.DO_Start, P4.P402.DO_Start, P4.P403.DO_Start, P4.P404.DO_Start, P4.UV401.DO_Start]
# plc5_output_vector = [P5.MV501.DO_Open, P5.MV501.DO_Close, P5.MV502.DO_Open, P5.MV502.DO_Close, P5.MV503.DO_Open,
#                       P5.MV503.DO_Close, P5.MV504.DO_Open, P5.MV504.DO_Close]
