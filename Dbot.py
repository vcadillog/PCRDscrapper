import asyncio
import os
import sys
from discord.ext import commands, tasks
from replayChecker import Checker
import time
import random
import pickle 
from datetime import datetime
import profile as pf

class pvpBot(commands.Bot):
    async def on_ready(self):
        print(f'{self.user.name} has connected to Discord! at ' + '<t:'+str(round(time.time())) +':f>')

class discordPVP(commands.Cog , Checker):

    def __init__(self,bot, url):    
        self.url = url
        self.USER = pf.USER        
        self.MY_CHANNEL_ID = pf.MY_CHANNEL_ID
        self.bot = bot
        self.pvp_error = 1
        self.TOKEN = pf.TOKEN
        try:
            with open('saved_flow.pickle', 'rb') as handle:
                self.saved_flow = pickle.load(handle)       
        except FileNotFoundError:
            with open('saved_flow.pickle', 'wb') as handle:
                pickle.dump([], handle, protocol=pickle.HIGHEST_PROTOCOL)       
                self.saved_flow = []
        
        self.ivKey = [item[1] for item in self.saved_flow]        
        self.pvp = Checker(self.url, self.ivKey)        

    async def loader(self):
        for tmp in self.saved_flow:                                         
            await self.pvp.request(flow = tmp[2], replayer= True)              



    @commands.command(name = 'pvp', help='Shows Princess and Battle arena rank')
    async def pvp_rank(self,ctx):
        await self.bot.wait_until_ready()            
        tmp_data = Checker.data                
        for item in tmp_data:            
            if item['url'] == "https://priconne-redive.us/profile/get_profile":
                output_text = "<@" + str(self.USER) + "> " + item['data']['name']+ " BA rank is : " + str(item['data']['BA_rank']) + " PA rank is : " + str(item['data']['PA_rank']) + "\n Last update: "+ '<t:'+ str(item['time']) +':f> '                                                          
                await ctx.send(output_text)             
               


    @tasks.loop(seconds = random.randint(15,30)) 
    async def dataLoop(self):        
        await self.bot.wait_until_ready()
                
        flow = Checker.flow_by_id
        
        for index in range(len(flow)):     
            
            if flow[index][2]['request']['path'] == b'/profile/get_profile':               
                              
                await self.pvp.request(flow = flow[index][2], replayer= True)
                
                tmp_data = Checker.data                           
                for item in tmp_data:

                    try:
                        if item['url'] == "https://priconne-redive.us/profile/get_profile" and item['id'] == flow[index][0] :  
                            channel = self.bot.get_channel(self.MY_CHANNEL_ID) 
                            
                            print('Time: ' + datetime.fromtimestamp(item['time']).strftime('%H:%M:%S')+ ' id: ' + item['data']['name'] + ' BA rank: ' + str(item['data']['BA_rank']) + ' PA rank: ' + str(item['data']['PA_rank']))                            
                            if item['data']['BA_rank'] > item['data']['BA_old_rank']:
                                await channel.send("<@" + str(self.USER) + "> " + item['data']['name'] + " dropped in BA 📉: " + str(item['data']['BA_old_rank']) + " to " + str(item['data']['BA_rank']))                                

                            elif item['data']['BA_rank'] < item['data']['BA_old_rank']:
                                await channel.send("<@" + str(self.USER) + "> " + item['data']['name'] + " climbed in BA 📈: " + str(item['data']['BA_old_rank']) + " to " + str(item['data']['BA_rank']))                                


                            if item['data']['PA_rank'] > item['data']['PA_old_rank']:

                                await channel.send("<@" + str(self.USER) + "> " + item['data']['name'] + " dropped in PA 📉: " + str(item['data']['PA_old_rank']) + " to " + str(item['data']['PA_rank']))                                

                            elif item['data']['PA_rank'] < item['data']['PA_old_rank']:

                                await channel.send("<@" + str(self.USER) + "> " + item['data']['name'] + " climbed in PA 📈: " + str(item['data']['PA_old_rank']) + " to " + str(item['data']['PA_rank']))                                

                            self.pvp_error = 0    

                    except:               
                        if self.pvp_error == 0:                                                             
                            await channel.send("Data not received, contact with the admi " + '<t:'+str(round(time.time())) +':f>')                   
                            self.pvp_error = 1                           
                   

    @tasks.loop(seconds = 3)
    async def timeLoop(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.MY_CHANNEL_ID)

        tmp_data = Checker.data          
        flow = Checker.flow_by_id       
        data = [tmp_data, flow]

        try:
            Checker.data = [tmp for tmp in tmp_data if tmp['error']==0]

            flow = [elem for item in data[0] if item['error'] == 0 for elem in data[1] if item['id'] == elem[0]]
            if flow != []:
                with open('saved_flow.pickle', 'wb') as handle:
                    pickle.dump(flow, handle, protocol=pickle.HIGHEST_PROTOCOL)       

        except TypeError:
            pass        

        for item in tmp_data:
            
            try:                                          
                if  time.time() - item['time']> 180:
                    await channel.send( "<@" + str(self.USER) + "> " + 'Timed out')
                    os.execv(sys.argv[0],sys.argv)

            except TypeError:
                pass

  
    def start(self):                 
        asyncio.create_task(self.bot.start(self.TOKEN))        
        asyncio.create_task(self.loader(),name='flow_loader')

        self.dataLoop.start()     
        self.timeLoop.start()



