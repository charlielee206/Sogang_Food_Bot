from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import discord
from discord.ext import commands
import random
import disnake
import ctypes

#===============SELECTION VARIABLES===============
DistanceVariable = -1
MenuVariable = -1
#===============DISCORD SETUP DIVISION START==========

description = '''Sogang Food Recommendation Bot. Prefix: `미식봇! `, `미식봇! 정보` for more info.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

help_command = commands.DefaultHelpCommand(
    no_category = '명령어'
)

bot = commands.Bot(command_prefix='미식봇! ', description=description, intents=intents, help_command = help_command)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name = "Type ｢미식봇! 정보｣ for help."))
    print('------')

#===============DISCORD SETUP DIVISION END================
#==========GOOGLE API SETUP DIVISION START===============

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = 'A2:J1000'


def GetSheets():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                    range=SAMPLE_RANGE_NAME).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        return values

    except HttpError as err:
        print(err)
        
 #==========GOOGLE API SETUP DIVISION END===============       
#if __name__ == '__main__':

values = GetSheets()
print('---------------------------')
print(len(values))

#===============RECOMMENDATION CANDIDATE ARRAY===============
class CandidateList(object):
     
    def __init__(self):
        self.n = 0 #Number of Elements
        self.capacity = 1 # Default Capacity
        self.A = self.make_array(self.capacity)
         
    def __len__(self): #Current Array Length
        return self.n
     
    def __getitem__(self, k):#Return kth Element
        if not 0 <= k <self.n:#Check if K is within bounds
            return IndexError('K is out of bounds !')
        return self.A[k]
         
    def append(self, ele):
        if self.n == self.capacity:
            # Double capacity if not enough room
            self._resize(2 * self.capacity)
         
        self.A[self.n] = ele # Set self.n index to element
        self.n += 1
 
    def delete(self): #Deletes the Tail
        if self.n==0:
            print("Array is empty; Deletion not Possible!")
            return
         
        self.A[self.n-1]=0
        self.n-=1
    
    def removeAt(self,index):
        """
        This function deletes item from a specified index..
        """       
 
        if self.n==0:
            print("Array is empty deletion not Possible")
            return
                 
        if index<0 or index>=self.n:
            return IndexError("Index out of bound....deletion not possible")       
         
        if index==self.n-1:
            self.A[index]=0
            self.n-=1
            return       
         
        for i in range(index,self.n-1):
            self.A[i]=self.A[i+1]           
             
         
        self.A[self.n-1]=0
        self.n-=1
    
    def _resize(self, new_cap):#Force Resize Array
        B = self.make_array(new_cap) # New bigger array
         
        for k in range(self.n): # Reference all existing values
            B[k] = self.A[k]
             
        self.A = B # Call A the new bigger array
        self.capacity = new_cap # Reset the capacity
         
    def make_array(self, new_cap):#New Array with capacity
        return (new_cap * ctypes.py_object)()


#==========RECOMMENDATION DIVISION===============
def RandomRecommend():
    global values
    
    Selection = random.randint(0,len(values) -1)
    #print(values[Selection][0])
    return values[Selection]

def AlcoholRecommend():
    global values
    
    AlcoholArray = CandidateList()
    
    for i in range(len(values)):
        if values[i][5] == '1':
            AlcoholArray.append(values[i])
    
    Lottery = random.randint(0, AlcoholArray.n-1)
    #print(len(AlcoholArray[Lottery]))
    return AlcoholArray[Lottery]

def NormalRecommend():
    global values
    global DistanceVariable
    global MenuVariable
    
    RecommendArray = CandidateList()
    #sift if dist is 0
    MenuVariable = int(MenuVariable)
    DistanceVariable = int(DistanceVariable)
    
    for i in range(len(values)):
        #print(f"i = {i}")
        if DistanceVariable == 1:
            if MenuVariable == 0:
                if values[i][1] == "한식":
                    RecommendArray.append(values[i])
            elif MenuVariable == 1:
                if values[i][1] == "중식":
                    RecommendArray.append(values[i])
            elif MenuVariable == 2:
                if values[i][1] == "일식":
                    RecommendArray.append(values[i])
            elif MenuVariable == 3:
                if values[i][1] == "양식":
                    RecommendArray.append(values[i])
            elif MenuVariable == 4:
                if values[i][1] == "기타":
                    RecommendArray.append(values[i])
            else:
                RecommendArray.append(values[i])
                
        elif DistanceVariable == 0 and values[i][4] == '1':
            if MenuVariable == 0:
                if values[i][1] == "한식":
                    RecommendArray.append(values[i])
            elif MenuVariable == 1:
                if values[i][1] == "중식":
                    RecommendArray.append(values[i])
            elif MenuVariable == 2:
                if values[i][1] == "일식":
                    RecommendArray.append(values[i])
            elif MenuVariable == 3:
                if values[i][1] == "양식":
                    RecommendArray.append(values[i])
            elif MenuVariable == 4:
                if values[i][1] == "기타":
                    RecommendArray.append(values[i])
            else:
                RecommendArray.append(values[i])
                
    #Yes, I know that this is a stupid way to do this, but I just couldn't be arsed to fix it once it was working.
            
    MenuVariable = -1
    DistanceVariable = -1
    
    if RecommendArray.n == 0:
        ErrorArray = ['그런거 없다','없다','없다','없다','없다','없다','조건에 만족하는 식당이 없어요 ㅠㅠ','없다','없다']
        return ErrorArray
    else:    
        Selection = random.randint(0,RecommendArray.n-1)
        #print("******************")
        #print(Selection)
        #print(RecommendArray[Selection])
        return RecommendArray[Selection]
            

def EmbedMaker(InputArray):
    if len(InputArray) == 9: #Placeholder if image link is not there.
        InputArray.append("https://cdn.discordapp.com/attachments/1022464938800857098/1090565996454092831/img_12.jpg")
    
    Description = "메뉴: " + InputArray[1] + ' - ' + InputArray[3] + "\n" + "위치: " + InputArray[2]
    
    if InputArray[4] == '1':
        Description = Description + "\n+ 학교근처"
    if InputArray[5] == '1':
        if InputArray[4] == '1':
            Description = Description + ","
        else:
            Description = Description + "\n+ "
        Description = Description + "술집"
        
    Description = Description + "\n\n**｢" + InputArray[6] + "｣**\n"
        
    EmbedOutput = {
        "title": InputArray[0],
        "description": Description,
        "color": 0xe617cd,
        "author": {
            "name":"여기는 어때?!",
            "icon_url": "https://cdn.discordapp.com/attachments/1075222754837663744/1075688660172804106/5339d7bf5a49bf3871914557abed259f2.jpg",
        },
        "footer": {"text": "이름을 클릭하면 지도를 표시합니다."},
        "image": {"url": InputArray[9]},
        "url":InputArray[8] 
        }
    #print(Description)
    return EmbedOutput

#===============COMMAND DIVISION===============

@bot.command(name="Info", aliases=["Info!","도와줘요","도와줘요!","도와줘","도와줘!","정보","정보!","안내"])
async def Info(ctx):
    """Prints a quick summary about this bot."""
    
    InfoEmbed = {
    "title": "뭘 먹을지 추천해주는 궁극의 미식봇!",
    "color": 0xe617cd,
    "footer": {"text": "Cobbled together by Charlie_Lee_Rhee"},
    }
    embed = disnake.Embed.from_dict(InfoEmbed)  
    embed.add_field(value="오늘 뭐 먹을지 고민은 그만! 미식봇에게 물어봐요!\n개발자와 친구들의 편파 주관적인 맛집 데이터베이스를 바탕으로 적절한 식당을 추천해줍니다!",name = "" ,inline=False) 
    embed.add_field(name="사용법:",value = '`미식봇! 뭐먹지?` 를 통해 무엇을 먹을지 정해요!\n`미식봇! 빨리!` 를 입력하면 학교에서 가까운 곳을 추천해줘요! ("가깝다" 의 기준은 주관적입니다.)\n`미식봇! 배고파!` 를 입력하면 랜덤으로 식당을 추천해줘요!\n`미식봇! 술` 을 입력하면 학교 주변 술집을 하나 추천해줍니다!' ,inline=False)
       
    await ctx.send(embed=embed)


@bot.command(name="빨리", aliases=["빨리!"])
async def 빨리(ctx):
    """Prints a random place within the vicinity."""
    
    global DistanceVariable 
    DistanceVariable = 0
    embed = disnake.Embed.from_dict(EmbedMaker(NormalRecommend()))
    await ctx.send(embed=embed)
        
@bot.command(name="배고파", aliases=["배고파!"])
async def 배고파(ctx):
    """Prints a random place from the catalogue."""
    
    Recommendation = RandomRecommend()
    embed = disnake.Embed.from_dict(EmbedMaker(Recommendation))
    await ctx.send(embed=embed)
    
@bot.command(name="술", aliases=["술!"])
async def 술(ctx):
    """Prints a random place to drink from the catalogue."""
    
    embed = disnake.Embed.from_dict(EmbedMaker(AlcoholRecommend()))
    await ctx.send(embed=embed)
 
@bot.command()
async def Catalogue(ctx):
    """Prints how many elements are in the bot's catalogue."""
    
    global values
    await ctx.send(f"현재 미식봇의 데이터베이스에는 {len(values)}개의 식당이 입력되어있습니다!") 
        
@bot.command()
async def Update(ctx):
    """Updates the bot's catalogue."""
    global values
    await ctx.send("Updating...")
    LastValue = len(values)
    values = GetSheets()
    CurrentValue = len(values)
    await ctx.send("Done!")
    await ctx.send(f"Catalogue Updated from {LastValue} elements to {CurrentValue} elements.")

class DistanceSelect(discord.ui.View):
    @discord.ui.select( 
        placeholder = "거리는?", 
        min_values = 1, 
        options = [ 
            discord.SelectOption(
                label="가까운데!",
                description="나 지금 바뻐 ㅠㅠ",
                value = 0
            ),
            discord.SelectOption(
                label="멀어도 OK!",
                description="거리는 상관 없고 맛만 좋으면 됨",
                value = 1
            )
        ]
    )
    async def select_callback(self, interaction, select): 
        global DistanceVariable
        DistanceVariable = select.values[0]
        print(f"DistanceVariable:{DistanceVariable}")
        embed = disnake.Embed.from_dict(EmbedMaker(NormalRecommend()))
        await interaction.response.send_message(f"여기는 어때?", embed = embed)
        await interaction.followup.edit_message(interaction.message.id,content = (f"선택 거리: {select.options[int(select.values[0])].label}"), view=None)

class MenuSelect(discord.ui.View):
    @discord.ui.select( 
        placeholder = "뭐먹을까?", 
        min_values = 1, 
        max_values = 1, 
        options = [ 
            discord.SelectOption(
                label="한식",
                description="트래디쇼날 코리안-스타일",
                value = 0
            ),
            discord.SelectOption(
                label="중식",
                description="你吃了吗？",
                value = 1
            ),
            discord.SelectOption(
                label="일식",
                description="おいしくな～れ～",
                value = 2
            ),
            discord.SelectOption(
                label="양식",
                description="서양 오랑캐들의 영향을 받은 식사",
                value = 3
            ),
            discord.SelectOption(
                label="기타",
                description="나의 입맛은 그렇게 간단하게 분류할 수 있는것이 아니다!",
                value = 4
            ),
            discord.SelectOption(
                label="뭐든지 OK!",
                description="다 필요없고 밥이나 묵자.",
                value = 5
            )
        ]
    )
    async def select_callback(self, interaction, select): # the function called when the user is done selecting options
        global MenuVariable
        MenuVariable = select.values[0]
        print(f"MenuVariable:{MenuVariable}")
        await interaction.response.send_message("거리는? 학교 근처? 아니면 좀 멀어도 괜찮아?", view=DistanceSelect())
        await interaction.followup.edit_message(interaction.message.id,content = (f"선택 메뉴: {select.options[int(select.values[0])].label}"), view=None)

@bot.command(name="뭐먹지", aliases=["뭐먹지?"])
async def 뭐먹지(ctx):
    """Prints a random place based on your selections."""
    await ctx.send("우선 메뉴부터! 원하는거 있어?", view=MenuSelect())






#===============BOT.RUN===============
bot.run('')