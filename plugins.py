from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from operator import xor

import msgpack

noopIV = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

def encrypt(key, msg , iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)    
    ciphertext = cipher.encrypt(pad(msg,block_size=AES.block_size))   
    return ciphertext[0:len(ciphertext)-AES.block_size]+key
    
def decrypt(ciphertext,get_iv=True, iv=noopIV):
    key = ciphertext[len(ciphertext)-32:len(ciphertext)]    
    ciphertext = ciphertext[0:len(ciphertext)-32]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = cipher.decrypt(ciphertext)
    if get_iv == True:        
        knownBody = bytes([130, 172, 100, 97, 116, 97, 95, 104, 101, 97, 100, 101, 114, 115, 133, 170])
        iv = tuple(map(xor, msg[0:16],knownBody))
        iv = bytes(iv)       
        return iv
    return msg , key

def decyph(msg):
    return msgpack.unpackb(unpad(msg,block_size=AES.block_size), raw=False)

  
def data_viewer(data):
    try:
        
        if data[1][3] =='https://priconne-redive.us/profile/get_profile':
            tmp = {}
            dict_player = {} 
            try:  
                if len(data) > 1:            
                    dict_player['id'], dict_player['time'],dict_player['error'] = data[1][0],data[1][1],data[1][2]
                    if data[1][2] == 1 :                        
                        return dict_player
                    else:
                        tmp['name'], tmp['BA_old_rank'] , tmp['BA_rank'] , tmp['PA_old_rank'] , tmp['PA_rank']=data[0][4]['user_info']['user_name'] ,data[0][4]['user_info']['arena_rank'] ,data[1][4]['user_info']['arena_rank'] ,  data[0][4]['user_info']['grand_arena_rank'] , data[1][4]['user_info']['grand_arena_rank']                             
                        dict_player['url'],dict_player['data'] = data[1][3],tmp
                        return dict_player

            except:
                pass

    except IndexError:
        pass

def filter_by_id(data):
    
    data.sort(key=lambda x: (x[0] , -x[2]['server_conn']['timestamp_start']))  
    data = [item for item in data if len(item[2]['response']['content'])  > 1024]
    data_T = list(zip(*data))    
    tmp1 = list(dict.fromkeys(data_T[0]))
    temp2 =[]
    for i in tmp1:
        for j in data_T[0]:
            if i == j:
                temp2.append(data_T[0].index(i))

    index = list(dict.fromkeys(temp2))
    
    return [data[i] for i in index]    

def index_finder(data):
    tmp = []    
    ids = list(dict.fromkeys([x[0] for x in data]))
    for item in ids:
        index = [ind for ind in range(len(data)) if item in data[ind]]        
        tmp.append(index[len(index)-2:])
    return tmp    

