import asyncio
from plugins import decrypt, decyph, data_viewer, filter_by_id,index_finder
from mitmproxy import ctx
from  base64 import b64decode
from mitmproxy import http

class Checker:   
    flow_by_id= []
    data = []


    def __init__(self, url , ivKey = [] ):
        self.ivKey = ivKey          
        self.ArenaRank = []
        self.playerRank = []
        self.url = url
        self.data = []
        self.data_list = []
        self.data_dict = {}
        

    async def request(self,flow,replayer = False):        

        if isinstance(flow, dict):
             flow = http.HTTPFlow.from_state(flow)      

        if replayer == True:        
            flow = flow.copy()
            playback = ctx.master.addons.get('clientplayback')
            playback.start_replay([flow])  

        if flow.is_replay == "request":            
            return          
            
        await asyncio.sleep(1)
            

    async def response(self,flow):        
        
        if flow.request.pretty_url == 'https://priconne-redive.us/check/check_agreement':
        
            ivKey = decrypt(ciphertext = b64decode(flow.response.data.content))
            self.ivKey.append(ivKey)
            self.ivKey = list(dict.fromkeys(self.ivKey))            
           

            await asyncio.sleep(1)
     
        for URL in self.url:
               
            if flow.request.pretty_url == URL :        
                
                for key in self.ivKey:                    
                    try:
                        
                        res , _ = decrypt(b64decode(flow.response.data.content),False,key)  
                               
                        dec_res = decyph(res)  
                        
                        
                        if dec_res['data_headers']['result_code'] == 1:
                            error_code = 0     
                        else:
                            error_code = 1                       
                        error_timeout = dec_res['data_headers']['servertime']
                        
                        id = dec_res['data_headers']['viewer_id']                        

                        Checker.flow_by_id.append([id, key, flow.get_state()])
                        Checker.flow_by_id = filter_by_id(Checker.flow_by_id)          
                                             
                        self.data.append([id , error_timeout, error_code, URL, dec_res['data']])     
                        index = index_finder(self.data) 
                        self.data = [self.data[item] for sublist in index for item in sublist] 
                      
                        Checker.data = [[i,j] for i,j in zip(self.data,self.data[1:])  if i[0] == j[0]]
                        Checker.data = [data_viewer(Checker.data[item]) for item in range(len(Checker.data))]

   

                        await asyncio.sleep(1)
                    except ValueError:                        
                        pass



