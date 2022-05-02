import pickle
no_of_hops = []
Send_string = "FILESEND"
client1_Files = ['file1.txt', 'file2.txt']


def toBytes(x):
    return pickle.dumps(x)


def hopcount(uuid):
    return 2


def isFilePresent(file_name,dict):
    for i in dict:
        uuid = i
        temp_dict = dict[i]
        arr = temp_dict['files']
        count = arr.count(file_name)
        if count>0:
            return True,uuid
    return False,0