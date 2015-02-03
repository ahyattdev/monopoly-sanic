import simplegui, random

width=1100
height=900
spaceSize=height/7
#define variables
# players=6 players stored in list
# playerData:
# 0 token
# 1 money
# 2 tokenLocation
# 3 property-ids list
# 4 property-metadata
# 5 player-metadata
stage=0
selectedButton=0
selectedToken=0
startingMoney=1000
whosTurn=0
# GUI
buttons=[]
label=""
subLabel=""
subSubLabel=""
auction=False
aucSellPrice=0
aucBuyer=0
aucProp=0
bldg=False
bldgProp=0
oldButtons=[]
# 0 adding players
# 1 in game
# 2 someone wins

propertyData=[[0, "GO", "Black", 0, 0, "go"],
[1, "Junky Junkyard", "Brown", 60, 2, "property"],
[2, "Magma Field", "Brown", 60, 4, "property"],
[3, "Chance", "Black", 0, 0, "chance"],
[4, "Tropical Dungeon", "Light-Blue", 100, 6, "property"],
[5, "Rainbow Beach", "Light-Blue", 100, 6, "property"],
[6, "Jail", "Black", 0, 0, "jail"],
[7, "Cloudtop Cave", "Magenta", 140, 10, "property"],
[8, "Springyard", "Magenta", 140, 10, "property"],
[9, "Community Chest", "Black", 0, 0, "chest"],
[10, "Icecap Volcano", "Orange", 180, 14, "property"],
[11, "Silvurs Mountain", "Orange", 180, 14, "property"],
[12, "Free Parking", "Black", 0, 0, "parking"],
[13, "Shaedew Retreat", "Red", 220, 18, "property"],
[14, "Knakles Alley", "Red", 220, 18, "property"],
[15, "Chance", "Black", 0, 0, "chance"],
[16, "Rouge Casino", "Yellow", 260, 22, "property"],
[17, "Metropolis", "Yellow", 260, 22, "property"],
[18, "Go to Jail", "Black", 0, 0, "gotojail"],
[19, "Amys Garden", "Green", 300, 26, "property"],
[20, "Taels Mansion", "Green", 300, 26, "property"],
[21, "Community Chest", "Black", 0, 0, "chest"],
[22, "Sanic Lake", "Blue", 350, 35, "property"],
[23, "Aegman Lab", "Blue", 400, 50, "property"]]

chance=["You broke teh records, collect $10",
        "+20 Swag Points, collect $20",
        "Cool. Collect $100",
        "3fast5u, go to Jail!",
        "MLG membership fee, pay $75",
        "Speeding ticket, pay $50",
        "NOTSEGA licensing fee, pay $134"]
chest=["You win teh race, collect $75",
       "You got all the rings in every multiverse, collect $10",
       "Noice. Collect $200",
       "You went too many MLGs/s, go directly to jail.",
       "asdfsadfhgfdhfj, pay $75",
       "Nice meme! Collect $35",
       "You are a silly human bean, pay $28"]

# Tokens
sanic = simplegui.load_image("http://i.imgur.com/0ZPraSv.png")
taels = simplegui.load_image("http://i.imgur.com/ijRxqkw.png")
knakles = simplegui.load_image("http://i.imgur.com/nceRr6K.png")
aegman = simplegui.load_image("http://i.imgur.com/aMOuDtV.png")
shadew = simplegui.load_image("http://i.imgur.com/tPYA0wL.png")
sulvur = simplegui.load_image("http://i.imgur.com/0c2GS8g.png")
tokens=[sanic, taels, knakles, aegman, shadew, sulvur]
tokenColors=["Blue", "Orange", "Red", "Tan", "Black", "Silver"]

board=simplegui.load_image("http://i.imgur.com/aLUwZ5z.png")
players=[]

def houseCost(propNum):
    propData=propertyData[propNum]
    return propData[3]/2

def card(kind, player, cardNum):
    pData=players[player]
    # Kind 0 are chance cards
    if kind==0:
        # Broke records, collect $50
        if cardNum==0:
            pData[1]+=50
        # +20 swag points, +$20
        elif cardNum==1:
            pData[1]+=20
        # Cool, collect $100
        elif cardNum==2:
            pData[1]+=100
        # 3fast5u, go to jail
        elif cardNum==3:
            pData[5]["in-jail"]=True
            pData[2]=6
        # MLG membership fee, pay $75
        elif cardNum==4:
            pData[1]-=75
        # Speeding ticket, pay $50
        elif cardNum==5:
            pData[1]-=50
        # NOTSEGA licensing fee, pay $134
        elif cardNum==6:
            pData[1]-=134
    # Kind 1 are chest cards
    elif kind==1:
        # Won race, collect $75
        if cardNum==0:
            pData[1]+=75
        # Got all rings, collect $10
        elif cardNum==1:
            pData[1]+=10
        # Noice. Collect $200
        elif cardNum==2:
            pData[1]+=200
        # Too many MLGs/s, go to jail
        elif cardNum==3:
            pData[5]["in-jail"]=True
            pData[2]=6
        # asdfsadfhgfdhfj, pay $75
        elif cardNum==4:
            pData[1]-=75
        # Nice meme! Collect $35
        elif cardNum==5:
            pData[1]+=35
        # Silly human bean, pay $28
        elif cardNum==6:
            pData[1]-=28
    testDebt(player)

def colorForPlayer(token):
    if token==0:
        return "Blue"
    elif token==1:
        return "Orange"
    elif token==2:
        return "Red"
    elif token==3:
        return "Tan"
    elif token==4:
        return "Black"
    elif token==5:
        return "Silver"

def gameCanStart():
    if len(players)>=2:
        return True
    else:
        return False

def spaceOwned(space):
    for index, player in enumerate(players):
        for prop in player[3]:
            if prop==space:
                return [True, index, propertyData[space][4]]
    return [False]

def canBuyProperty(player, space):
    prop=propertyData[space]
    player=players[player]
    canBuy=True
    # Property is not ownable
    if prop[5]!="property":
        canBuy=False
    # Someone else already owns it
    for player in players:
        for thingy in player[3]:
            if thingy==space:
                canBuy=False
    # The player can not afford it
    if player[1]<prop[3]:
        canBuy=False
    return canBuy

def coordsForSpace(space):
    bottomRowHeight=height-spaceSize
    leftSide=200
    rightSide=width-spaceSize
    # Bottom Row
    if space==0:
        # GO
        return (width-spaceSize,bottomRowHeight)
    elif space==1:
        return (width-spaceSize*2,bottomRowHeight)
    elif space==2:
        return (width-spaceSize*3,bottomRowHeight)
    elif space==3:
        return (width-spaceSize*4,bottomRowHeight)
    elif space==4:
        return (width-spaceSize*5,bottomRowHeight)
    elif space==5:
        return (width-spaceSize*6,bottomRowHeight)
    # Left Side
    elif space==6:
        # Jail
        return (leftSide,height-spaceSize)
    elif space==7:
        return (leftSide,height-spaceSize*2)
    elif space==8:
        return (leftSide,height-spaceSize*3)
    elif space==9:
        return (leftSide,height-spaceSize*4)
    elif space==10:
        return (leftSide,height-spaceSize*5)
    elif space==11:
        return (leftSide,height-spaceSize*6)
    # Top Row
    elif space==12:
        # Free Parking
        return (leftSide,0)
    elif space==13:
        return (leftSide+spaceSize,20)
    elif space==14:
        return (leftSide+spaceSize*2, 20)
    elif space==15:
        return (leftSide+spaceSize*3, 20)
    elif space==16:
        return (leftSide+spaceSize*4, 20)
    elif space==17:
        return (leftSide+spaceSize*5, 20)
    # Right Side
    elif space==18:
        # Go to Jail
        return (rightSide,0)
    elif space==19:
        return (rightSide,spaceSize)
    elif space==20:
        return (rightSide,spaceSize*2)
    elif space==21:
        return (rightSide,spaceSize*3)
    elif space==22:
        return (rightSide,spaceSize*4)
    elif space==23:
        return (rightSide,spaceSize*5)

def setup():
    global buttons, label
    buttons=["Next Token", "Add Player"]
    label="Add players"

def turn(player):
    global buttons, label, subLabel, whosTurn, selectedButton, subSubLabel
    subSubLabel=""
    # Reset the selected button
    selectedButton=0
    # Set the global for whos turn it is
    whosTurn=player
    # Get random numbers for the dice
    roll=(random.randint(1,4),random.randint(1,4))
    # Fetch the data for the current player
    playerData=players[player]
    if playerData[5]["in-jail"]==False:
    # Only move the token if the player is not in jail
        if roll[0]+roll[1]+playerData[2]>23:
            # Overflow over 23
            # Pass Go
            spaceToZero=23-playerData[2]
            playerData[2]=roll[0]+roll[1]-spaceToZero-1
            playerData[1]+=100
        else:
            # Regular math
            playerData[2]+=roll[0]+roll[1]
    if playerData[2]==18:
        # Go to jail space
        playerData[5]["in-jail"]=True
        playerData[2]=6
    label="Player "+str(player+1)+"'s turn"
    subLabel=""
    buttons=["Continue"]
    if playerData[5]["in-jail"]==True:
        # Add the bail text to the label
        subLabel="You are in jail. Bail is $50."
        # Add a button for paying the fine
        buttons.append("Pay Fine")
    else:
        # Add text for what the player rolled
        subLabel="You rolled a "+str(roll[0])+" and a "+str(roll[1])+". "
    if canBuyProperty(player, playerData[2]):
        # Add a buy button if the player can buy the property that they are on
        buttons.append("Buy")
        # Let them know
        subLabel=subLabel+"You can buy "+propertyData[playerData[2]][1]+" for $"+str(propertyData[playerData[2]][3])+". "
    if len(playerData[3])!=0:
           buttons.append("Auction")
           canBuyHouse=False
           pMoney=playerData[3]
           for prop in playerData[3]:
                if pMoney>=houseCost(prop):
                    canBuyHouse=True
#           if canBuyHouse==True:
#               buttons.append("Buy Building")
    # Determine if someone else owns the space the player landed on
    ownedData=spaceOwned(playerData[2])
    if ownedData[0]==True:
        # Get the data we need to pay the rent
        owner=ownedData[1]
        rent=ownedData[2]
        if owner!=player:
            # Subtract the rent from the current player
            playerData[1]-=rent
            # Add the rent to the owner
            players[owner][1]+=rent
            # Add text to the label so the player knows that they payed rent
            subLabel=subLabel+"You are on Player "+str(owner+1)+"'s space. A rent of $"+str(rent)+" was paid. "
    # Chance/community chest spaces
    prop=propertyData[playerData[2]]
    cardNum=random.randint(0,6)
    if prop[5]=="chance" or prop[5]=="chest":
        kind=0
        subLabel+="You got a card, it says: "
        if prop[5]=="chest":
            kind=1
            subSubLabel=chest[cardNum]
        else:
            subSubLabel=chance[cardNum]
        card(kind, player, cardNum)
    testDebt(player)

def testDebt(player):
    global label
    # Use this method to see if the player is out of money. 
    # If they have properties, trigger an auction. 
    # If they do not, then they lose!
    pData=players[player]
    # Test if their money is less than zero
    if pData[1]<0:
        if len(pData[3])==0:
            label="Player "+str(player+1)+" ran out of money and has no properties. They lose!"
            pData[5]["loser"]=True

def startAuction(player):
    global auction, oldButtons, buttons, aucBuyer, aucSellPrice, aucProp, selectedButton
    auction=True
    selectedButton=1
    oldButtons=buttons
    aucBuyer=0
    aucSellPrice=0
    aucProp=0
    if player==0:
        aucBuyer=1
    buttons=["Cancel", "Next Property", "Next Player", "Less Money", "More Money", "Sell"]

def startBuyBuilding(player):
    global bldg, bldgProp, buttons, oldButtons, selectedButton
    selectedButton=1
    pData=players[player]
    bldg=True
    oldButtons=buttons
    buttons=["Cancel", "Next Property", "Buy"]
    bldgProp=pData[3][0]
def bldgsOnProp(player, prop):
    pData=players[player]
    propMeta=pData[4]
    count=0
    for key in propMeta:
        if key==prop:
            count=pData[4][key]
    print count
    return count
def endBuyBuilding():
    global bldg, bldgProp, buttons
    bldg=False
    buttons=oldButtons
    print bldg, oldButtons

def endAuction():
    global buttons, auction, selectedButton
    buttons=oldButtons
    auction=False
    selectedButton=0

def draw(canvas):
    global buttons
    # Required for each stage
    canvas.draw_image(board, (450, 450), (900, 900), (650, 450), (900, 900))
    canvas.draw_line((200,0),(200,900),4,"Black")
    #Draw sidebar
    for index, player in enumerate(players):
        # xRoot is the x value to base everything of this players stats off of
        xRoot=50+100*index
        color="Black"
        tokenColor=tokenColors[player[0]]
        moneyText="$"+str(player[1])
        if player[5]["loser"]==True:
            color="Grey"
            tokenColor="Grey"
            moneyText="Loser"
        canvas.draw_text("Player "+str(index+1), (75, xRoot), 30, tokenColor)
        canvas.draw_text(moneyText, (75, xRoot+30), 30, color)
        canvas.draw_image(tokens[player[0]], (100,100), (200,200), (20,xRoot), (100, 100))
    # Draw the buttons
    if len(buttons)!=0:
        canvas.draw_polygon(((400, 450), (900, 450), (900, 700), (400, 700)), 4, "Black")
        for index, buttonText in enumerate(buttons):
            buttonColor="Black"
            if selectedButton==index:
                buttonColor="Red"
            canvas.draw_text(buttonText, (420+90*index,670), 15, buttonColor)
    # Draw the labels
    canvas.draw_text(label, (420, 470), 24, "Black")
    canvas.draw_text(subLabel, (420, 500), 14, "Black")
    canvas.draw_text(subSubLabel, (420, 530), 14, "Black")
    # Stage 0, setting up the game
    if stage==0:
        # Draw the border of the dialogue box
        canvas.draw_polygon(((400, 450), (900, 450), (900, 700), (400, 700)), 4, "Black")
        # Draw an icon for the currently selected token
        canvas.draw_image(tokens[selectedToken], (100, 100), (200, 200), (475, 550), (100, 100))
    # Stage 1, the gameplay
    elif stage==1:
        # Draw the tokens
        for index, player in enumerate(players):
            playersBefore=0
            for playerBefore in range(0,index):
                if player[2]==players[playerBefore][2]:
                    playersBefore+=1
            x=coordsForSpace(player[2])[0]+17
            y=coordsForSpace(player[2])[1]+40
            if playersBefore<3:
                x+=40*playersBefore
            else:
                newb4=playersBefore-3
                x+=40*newb4
                y+=40
            canvas.draw_image(tokens[player[0]], (100,100), (200,200), (x,y), (50,50))
        # Draw labels for owned properties
        for index, player in enumerate(players):
            for prop in player[3]:
            # Property will be an integer for the property that the player owns
                propLabel="Player "+str(index+1)
                x=coordsForSpace(prop)[0]+10
                y=coordsForSpace(prop)[1]+120
                canvas.draw_text(propLabel, (x,y), 18, colorForPlayer(player[0]))
    if auction==True:
        prop=players[whosTurn][3][aucProp]
        propTitle="Property: "+propertyData[prop][1]
        x=420
        y=540
        canvas.draw_text(propTitle, (x,y), 18, "Black")
        buyerText="Buyer: Player "+str(aucBuyer+1)
        canvas.draw_text(buyerText, (x,y+30), 18, "Black")
        moneyText="Price: "+str(aucSellPrice)
        canvas.draw_text(moneyText, (x,y+60), 18, "Black")

def keydown(key):
    global selectedButton, selectedToken, stage, buttons, auction, oldButtons, aucProp, aucSellPrice, aucBuyer
    if key==simplegui.KEY_MAP["space"]:
        # Like an "enter" key
        if stage==0:
            if selectedButton==0:
                # Next token
                if selectedToken==len(tokens)-1:
                    selectedToken=0
                else:
                    selectedToken+=1
            elif selectedButton==1:
                # Add player
                players.append([selectedToken, startingMoney, 0, [], {}, {"in-jail":False, "loser":False}])
                selectedToken=0
                selectedButton=0
                if gameCanStart()==True:
                    found=False
                    for item in buttons:
                        if item=="Start":
                            found=True
                    if found==False:
                        buttons.append("Start")
                # Test if there now are 6 players
                if len(players)==6:
                    stage=1
                    turn(0)
            elif selectedButton==2:
                # Start game
                stage=1
                turn(0)
        elif stage==1:
            button=buttons[selectedButton]
            if button=="Continue":
                # Next Turn
                if whosTurn<len(players)-1:
                    # Not last player
                    turn(whosTurn+1)
                else:
                    # Last player
                    turn(0)
            elif button=="Buy":
                player=players[whosTurn]
                space=player[2]
                propertyCost=propertyData[space][3]
                player[1]-=propertyCost
                player[3].append(space)
                buttons.remove("Buy")
                for index, butttton in enumerate(buttons):
                    if butttton=="Continue":
                        selectedButton=index
                if len(player[3])==1:
                   buttons.append("Auction")
            elif button=="Auction":
                startAuction(whosTurn)
            elif button=="Pay Fine":
                player=players[whosTurn]
                player[1]-=50
                buttons.remove("Pay Fine")
                player[5]["in-jail"]=False
                selectedButton=0
            # Auction buttons
            elif button=="Next Property" and auction==True:
                pData=players[whosTurn]
                props=pData[3]
                if aucProp>=len(props)-1:
                    aucProp=0
                else:
                    aucProp+=1
            elif button=="Next Player" and auction==True:
                def next():
                    global aucBuyer
                    if aucBuyer>=len(players)-1:
                        aucBuyer=0
                    else:
                        aucBuyer+=1
                next()
                if aucBuyer==whosTurn:
                    next()
            elif button=="Buy Building" and bldg==False:
                print "kek"
                startBuyBuilding(whosTurn)
            buyerData=players[aucBuyer]
            if buyerData[1]<aucSellPrice:
                aucSellPrice=buyerData[1]-buyerData[1]%20
            elif button=="Less Money" and auction==True:
                if aucSellPrice>=20:
                    aucSellPrice-=20
            elif button=="More Money" and auction==True:
                aucBuyerMoney=players[aucBuyer][1]
                if aucSellPrice+20<=aucBuyerMoney:
                    aucSellPrice+=20
            elif button=="Sell" and auction==True:
                sellerData=players[whosTurn]
                buyerData=players[aucBuyer]
                sellerData[1]+=aucSellPrice
                buyerData[1]-=aucSellPrice
                soldProp=sellerData[3][aucProp]
                sellerData[3].remove(soldProp)
                buyerData[3].append(soldProp)
                endAuction()
                if len(sellerData[3])==0:
                    buttons.remove("Auction")
            elif button=="Cancel" and auction==True:
                endAuction()
            # Buying buildings (houses and hotels)
            elif button=="Cancel" and bldg==True:
                endBuyBuilding()
            elif button=="Buy" and bldg==True:
                endBuyBuilding()
                pData=players[whosTurn]
                print "mouse rat"
def keyup(key):
    global selectedButton
    if key==simplegui.KEY_MAP["right"]:
        # Change selected button
        if selectedButton==len(buttons)-1:
            selectedButton=0
        else:
            selectedButton+=1
    if key==simplegui.KEY_MAP["left"]:
        # Change selected button
        if selectedButton==0:
            selectedButton=len(buttons)-1
        else:
            selectedButton-=1

frame = simplegui.create_frame("Monopoly: Sanic Edition", width, height)
frame.set_draw_handler(draw)
frame.add_label("Welcome to Monopoly:")
frame.add_label("Sanic Edition")
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_canvas_background("White")
frame.start()
setup()
