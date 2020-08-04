#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""New main function with the axe thing"""
#Character Class
# a character object represents one version of an in-game character
# multiple character objects are created for different conversations with an in-game character
class Character:
    def __init__(self, description, name, one_line_in_quest, one_line_general, conversation, quest):
        self.description = description
        self.name = name
        self.one_line_in_quest = one_line_in_quest
        self.one_line_general = one_line_general
        self.conversation = conversation
        self.quest = quest # this is the quest/part of quest the player must be on to have a full conversation with this character
        
    def interact_outside_quest(self, quest):
        '''checks if you are on a quest with the character's species, and then prints the characters corresponding generic line'''
        verb = 'says'
        if self.name[:-1] == "Marco and Ray":
            verb = 'say'
        if self.quest[:2] == quest.current_quest[:2] or quest.human_failed and quest.elf_failed and self.quest == "Troll":
            line = self.one_line_in_quest
        else:
            line = self.one_line_general
        print(f"\nAs you pass by, {self.name[:-1]} {verb}: {line}\n")

    def meet(self):
        '''prints a characters description'''
        print(f"\n{self.description}")
        
    def start_conversation(self, quests_object, inventory,coords):
        '''starts a conversation with the character'''
        for char_line, info in self.conversation.items():
            #print(char_line)
            if self.conversation[char_line]["from"] == [""]: #if this line is the first line the character will say
                print(f"\n{char_line}\n")
                self.choose_dialogue(self.conversation[char_line]["to"], quests_object, inventory,coords) #returns player's initial choices
            else: # sometimes you need an item to interact with a character
                if self.conversation[char_line]["from"] in [["Rose"], ["Elven Root"]]:
                    available = False
                    for item in inventory.items: # checks if that item is in the player's inventory
                        if item.name.lower() == self.conversation[char_line]["from"][0].lower(): #if the player has the required item
                            available = True
                            print(f"\n{char_line}\n")
                            self.choose_dialogue(self.conversation[char_line]["to"], quests_object, inventory,coords) # display dialogue choices
                    if not available:
                        print(f"\n{self.name[:-1]} needs you to get the {self.conversation[char_line]['from'][0]}.") # tells what item they need
    
    def choose_dialogue(self, choices, quests_object, inventory,coords):
        '''displays and handles player dialogue choices'''
        nums = []
        for num in range(len(choices)):
            nums.append(num)
            print(f"{num+1}. {choices[num]}")#dialogue choices are printed out
        p_num = input("\n>>> ")
        while not p_num.isdigit() or int(p_num)-1 not in nums: #makes sure input is valid
            p_num = input("Please enter a valid number: ")
        choice = choices[int(p_num)-1] #player chooses
        print(f"\nYou: {choice}\n")
   
        if "Give" in choice: #if the player gives an item in dialogue
            for item in inventory.items:
                if item.name.lower() in choice.lower():
                    inventory.remove_item(item)

        if choice != "Leave": #if you don't end the conversation
            self.char_responds(choice, quests_object, inventory,coords)#character responds

    
    def char_responds(self, player_choice, quests_object, inventory,coords):
        for char_line in self.conversation:
            #print(char_line)
            if player_choice in self.conversation[char_line]["from"]: #if what the player chooses triggers this line
                
                if "Quest Succeeded" in self.conversation[char_line]["to"]: #if this completes a quest
                    print(f"\n{char_line}\n\n-----Quest Completed!------")
                    quests_object.current_quest += "+" # keep track of important quest interactions
                    quests_object.succeeded.append(quests_object.current_quest + "s") # keep track of succeeded quests
                    quests_object.remove_quest()

                elif "Quest Failed" in self.conversation[char_line]["to"]:
                    if "Elf" in quests_object.current_quest: # keeps track of which quest line is failed
                        done = "Elf"
                        quests_object.elf_failed = True
                    elif "Human" in quests_object.current_quest:
                        done = "Human"
                        quests_object.human_failed = True
                    print(f"\n{char_line} It seems as if the {done}s won't be welcoming you back.\n\n-----Quest Failed-----")
                    quests_object.remove_quest()

                elif "Quest Updated" in self.conversation[char_line]["to"]:
                    print(f"\n{char_line}")
                    quests_object.current_quest += "+" # important quest interaction
                    
                elif "Quest Obtained" in self.conversation[char_line]["to"]:
                    print(f"\n{char_line}")
                    print("\n-----New Quest Gained!-----")
                    quests_object.add_quest(self.name) # calls add_quest
                    quests_object.current_quest += "+"

                elif "Restart" in self.conversation[char_line]["to"]: #if dialogue causes the player to restart a quest
                    print(f"\n{char_line}")
                    coords.x = 0 # reset coordinates
                    coords.y = -1
                    print(f"\n{locations[(coords.x,coords.y)].message}\n\nYou're outside the forest again. It's almost as if you went back in time.") # prints location message
                
                elif "may no longer take" in char_line: # if the player chooses dialogue so they can't get a particular quest
                    
                    if "Elf" in char_line:
                        quests_object.elf_failed = True
                    elif "Human" in char_line:
                        quests_object.human_failed = True
                              
                    print(f"\n{char_line}\n")
                    self.choose_dialogue(self.conversation[char_line]["to"], quests_object, inventory,coords)
                
                else: # if no special case
                    print(f"\n{char_line}\n")
                    self.choose_dialogue(self.conversation[char_line]["to"], quests_object, inventory,coords) #player responds to character 

# sets the player's starting coordinates
class Coord():
    def __init__(self):
        self.x = 9
        self.y = 10
                    
#Quest class
#handles adding, removing, clearing quests, as well as printing quest information
class Quests:
    def __init__ (self):
        self.quest_info = "" #description of current quest
        self.current_quest = "" #starts out like 'Human1' and "+" is added after succeeded important interactions
        self.succeeded = []
        self.elf_failed = False
        self.human_failed = False
        
    def add_quest(self, giver_name):
        '''sets current_quest and quest_info when the player gets a quest'''
        if giver_name == "Commander Cedric1":
            self.quest_info = "Find out who stole from the Humans' stockpile."
            self.current_quest = "Human1"
        elif giver_name == "Torma2":
            self.quest_info = "Talk to Tristan."
            self.current_quest = "Human2"
        elif giver_name == "Elf1":
            self.quest_info = "Find out what is killing the plants."
            self.current_quest = "Elf1"
        elif giver_name == "Princess Lyra1":
            self.quest_info = "Interrogate the suspects to find who stole the source of the Princess' magic."
            self.current_quest = "Elf2"
        elif giver_name == "Commander Cedric2":
            self.quest_info = "Get the tree of healing and share it with the Humans."
            self.current_quest = "Final"
        elif giver_name == "Princess Lyra4":
            self.quest_info = "Get the tree of healing and share it with the Elves."
            self.current_quest = "Final"
        
            
    def show_quest(self):
        '''prints out quest_info'''
        if 'Human' in self.current_quest or 'Elf' in self.current_quest or "Secret" in self.current_quest or "Final" in self.current_quest:
            print("\nCurrent quest:")
            print(f"\n{self.quest_info}")
        else:
            print("\nYou are not currently on a quest.")
        
    def clear_quest(self):
        '''handles when the player wants to clear a quest'''
        if "Final" in self.current_quest: # special case for final quest
            print("\nYou cannot clear this quest.")
        elif len(self.current_quest) >= 1: # if the player is on a quest
            print("\nIf you clear this quest, you will automatomatically fail it.")
            print(f"\n{self.quest_info}")
            if "Elf" in self.current_quest:
                people = "Elf"
            elif "Human" in self.current_quest:
                people = "Human"
            answer = input(f"\nAre you sure you want to clear your current quest? Doing so will mean that you cannot do any more quests for the {people}s. (y/n)").lower() # checks if player is sure
            while answer != 'y' and answer != 'n': # input handling
                answer = input("Please type 'y' or 'n': ").lower()
            if answer == 'y': # player fails that questline
                if "Elf" in self.current_quest:
                    self.elf_failed = True
                elif "Human" in self.current_quest:
                    self.human_failed = True
                self.remove_quest()
                print("\nYou have removed your current quest.")
        else: # if the player is not on a quest
            print("\nYou are not currently on a quest.")
    
    def remove_quest(self):
        '''removes all quest information'''
        self.quest_info = ""
        self.current_quest = ""

#Inventory class
class Inventory:
    def __init__(self):
        self.items = [] #will be a list of item objects

    def show_items(self):
        '''prints the names of all items in the inventory'''
        print("\nIn your inventory, you have:")
        for item in self.items:
            print(f"\n{item.name}")

    def add_item(self, thing):
        if thing.weight == 'heavy':
            print(f"\nYou can't take the {thing.name.lower()}.")
            return False
        else:
            self.items.append(thing)
            print(f"\nYou took the {thing.name.lower()}. It was added to your inventory.")
            return True

    def remove_item(self, thing):
        self.items.remove(thing)


#Item class
class Item:
    def __init__(self, name, title, q_description, s_description, quest, weight, hidden, table):
        self.name = name
        self.title = title
        self.q_description = q_description
        self.s_description = s_description
        self.quest = quest
        self.weight = weight
        self.hidden = hidden
        self.table = table
        
    def inspect(self, current_quest):
        if current_quest == self.quest: #if this object is relevant to the quest
            print(f"\n{self.q_description}")
        else:
            print(f"\nYou see a {self.name}.")

#ALL THE DIALOGUE

#Initial Conversation with Torma
torma1_conversation = {"Torma: Welcome. How may I help you?":{"from":[""], "to":["Who are you?", "Who am I?"]},
                      "Torma: I am Torma, I run this place and guide adventurers.":{"from":['Who are you?'], "to":["Where am I?"]},
                      "Torma: That's for you to answer.":{'from':["Who am I?"], "to":["Where am I?"]},
                      "Torma: You are in my tavern. It's a safe space for all who wish to get away from the dangers of the outside world.":{"from":["Where am I?"], "to":["What dangers?"]},
                      "Torma: You don't know? There's a war between the elves and humans, they've been fighting for generations.":{"from":["What dangers?"], "to":["Why are they fighting?"]},
                      "Torma: No one really knows anymore. At least I don't. They both want to get their hands on a magical tree. I think it's called the healing tree. If you help one of them out, you might be able to end this senseless fighting. The humans are north west of here and the elves are directly east. Keep in mind, the elves are more cunning folk, they will test your skills in a more intense manner than the humans in order to determine your worthiness. Good luck, and remember, you're always welcome back here!":{"from":["Why are they fighting?"], "to":["What does the healing tree do?", "Why haven't the humans or elves gotten to the tree?"]},
                      "Torma: No one knows. Ancient stories say just a branch could instantly heal entire armies.":{"from":["What does the healing tree do?"], "to":["*Leave*"]},
                      "Torma: Nasty rumors of dangerous creatures roaming the forest have kept everyone out for millenia.":{"from":["Why haven't the humans or elves gotten to the tree?"], "to":["*Leave*"]}}

torma1 = Character("You see a dwarf cleaning out a glass behind a long bar. When she notices you, she smiles and waves you over.", "Torma1", "Welcome back.", "Welcome back.", torma1_conversation, "All")

# This is the first conversation in human quest 1
commander_conversation = {"Commander Cedric: Hello. Who are you and what is your purpose?":{"from": [""], "to": ["I am Rowan and I am looking for the tree of healing."]},
               "Commander Cedric: As are we. We have some information on it, but first, you must prove to us that you are worthy.":{"from":["I am Rowan and I am looking for the tree of healing."], "to":["I'm happy to help. What must I do?","I don't need your approval. I need the information. But I will do it if I have to, so what must I do?", "If you have some information about the tree of healing, why don't you get it yourself?"]},
               "Commander Cedric: Because it grows in the heart of the forest.":{"from":["If you have some information about the tree of healing, why don't you get it yourself?"],"to":["I'm happy to help. What must I do?","I don't need your approval. I need the information. But I will do it if I have to, so what must I do?"]},
               "Commander Cedric: First you must help us. Someone has been stealing from our stockpile of food and supplies. Find them and talk to them.":{"from":["I'm happy to help. What must I do?","I don't need your approval. I need the information. But I will do it if I have to, so what must I do?"],"to":["Quest Obtained"]}}

commander = Character("Commander Cedric is a gruff man that commands respect. He has a uniform covered in medals commemorating his various achievements.", "Commander Cedric1", "If they aren't working, then they're most likely in the barracks.", "What do you want, elf sympathizer?", commander_conversation, "No Human")

# This is the second conversation in human quest 1
fighters_conversation = {"Marco: Traitor! I'll tell Commander Cedric!\nRay: It was you. YOU. I saw you do it. And if you tell the Commander, I'm going to leave.": {"from": [""], "to": ["Hello?"]},
                        "They stop fighting.\n\nMarco and Ray: We were just talking.": {"from": ["Hello?"], "to": ["About what?", "Do either of you know who stole from the stockpile?", "When was the food last seen?"]},
                        "Marco and Ray: Nothing.": {"from":["About what?"], "to":["See, the thing is, I think it was one of you who stole from the stockpile.", "I'm going to tell Commander Cedric that it was one of you who stole from the stockpile."]},
                        "The soldiers share a look and then run off in opposite directions." :{"from":["I'm going to tell Commander Cedric that it was one of you who stole from the stockpile."], "to":["Quest Failed"]},
                        "Marco and Ray: He did!\nMarco: I did not!\nRay: Well neither did I!": {"from":["Do either of you know who stole from the stockpile?", "See, the thing is, I think it was one of you who stole from the stockpile."], "to":["Do you have any evidence against each other?"]},
                        "Marco: No, but he was a guard on duty right before it was stolen\nRay: The food was there when I left, I can prove it. Another guard logged that it was all there. I heard a weird noise at the shift change, but I decided against checking what it was.\nMarco: That's a lie. He stole the food and forged the logs.": {"from":["Do you have any evidence against each other?"], "to": ["Do you know who would have more information?", "He did it. *point at Ray*"]},
                        "Ray: Last night, right before the shift change. I thought I heard a strange noise, gut it was late and I wanted to go to bed.\nMarco: That's a lie. He stole the food and forged the logs.": {"from":["When was the food last seen?"], "to":["Do you know who would have more information?", "He did it. *point at Ray*"]},
                        "Ray: Torma might have heard something while she was delivering food.":{"from":["Do you know who would have more information?"], "to":["Quest Succeeded"]},
                        "Ray: I can't believe you.\n\nHe leaves quietly, but you know he's bristling on the inside.\n\nMarco: Save yourself the time and give up.\n\nMarco walks away.": {"from":["He did it. *point at Ray*"], "to": ["Quest Failed"]}}

fighters = Character("Marco and Ray are two soldiers that are both wearing simple uniforms. They are too focused on their heated argument to notice you entered the barracks.", "Marco and Ray1", "What? You came back for directions? Find her yourself.", "Leave us alone.", fighters_conversation, "Human1+")

#How you get human quest 2
torma2_conversation = {"Torma: I'm so glad to see you again!":{"from":[""], "to":["What do you know about the missing supplies from the human camp?"]},
                      "Torma: Everything, I saw it happen. A human named Tristan came into the warehouse during shift change and took everything he could carry. He's a warehouse guard so he's probably on duty right now. Make sure to catch him before shift change. You'll know him by the bright green shirt he always wears. Oh... one more thing. Please be good to him. I know he has a good heart.":{"from":["What do you know about the missing supplies from the human camp?"], "to":["Quest Obtained"]}}

torma2 = Character("Torma beams at you, as if she hasn't seen another adventurer in decades.", "Torma2", "Hello, again!", "Hello, again!", torma2_conversation, "Human1++s")

#Talk to Tristan
tristan_conversation = {"Tristan: I'm busy.":{"from":[""], "to":["Are you Tristan?"]},
                       "Tristan: What do you want? Did Cedric send you?":{"from":["Are you Tristan?"], "to":["Yes he did. I just want to help you.", "That doesn't matter. I want you to return what's not yours.", "I want to take you to the commander to face punishment."]},
                       "Tristan: Why would you want to help me?":{"from":["Yes he did. I just want to help you."], "to":["I think we can come to a fair solution for everyone. You just need to return the supplies.", "One bad choice doesn't mean you're a bad person.", "You've done something wrong and the only way to help you is to make you pay for you crimes."]},
                       "Tristan: I'm not sure I can come back from this.":{"from":["One bad choice doesn't mean you're a bad person."], "to":["You can and will. Go clear things up with Commander Cedric.", "You need to accept punishment for you actions."]},
                       "Tristan: I can't. I need the supplies for my family.":{'from':["I think we can come to a fair solution for everyone. You just need to return the supplies.", "That doesn't matter. I want you to return what's not yours."], "to":["The others need these supplies too, it's wrong for you to take them without forethought.", "Why didn't you talk to the commander first?", "No matter, you need to be punished."]},
                       "Tristan: Please, I'll do anything. I just need the supplies for my family.":{"from":["I want to take you to the commander to face punishment."], "to":["The others need these supplies too, it's wrong for you to take them without forethought.", "Why didn't you talk to the commander first?", "No matter, you need to be punished."]},
                       "Tristan: I was so afraid he wouldn't agree.":{"from":["The others need these supplies too, it's wrong for you to take them without forethought.", "Why didn't you talk to the commander first?"], "to":["Return the supplies and go talk to him.", "He might not, but that's his choice to make, not yours. Talk to him."]},
                       "Tristan: Okay, I will. Thank you.\n\nTristan leaves, walking the slightest bit more confidently.":{"from":["Return the supplies and go talk to him.", "You can and will. Go clear things up with Commander Cedric."], "to":["Quest Succeeded"]},
                       "Tristan takes your leave.":{"from":["He might not, but that's his choice to make, not yours. Talk to him."], "to":["Quest Succeeded"]},
                       "Tristan: I can't leave my family. I'm sorry, I just can't.\n\nTristan runs away, careful not to look back.":{"from":["No matter, you need to be punished.", "You've done something wrong and the only way to help you is to make you pay for you crimes.", "You need to accept punishment for your actions."], "to":["Quest Failed"]}}

tristan = Character("Tristan is skinny man with bright red hair. He has a bright green shirt on.", "Tristan1", "I'm busy.", "I'm busy.", tristan_conversation, "Human2+")

#Elf quest 1
#first conversation
elf1_conversation = {"Elf: Hello. Who are you? I haven't seen you around here before.":{"from":[""], "to":["I'm looking for the tree of healing. Where is your leader? I need to talk to them."]},
                    "Elf: No, no. You don't need to talk to her. You need to talk to me. I know everything about the tree. I have dedicated my life to it.":{"from":["I'm looking for the tree of healing. Where is your leader? I need to talk to them."], "to":["And why should I believe you?", "Please, tell me everything!", "First I have a couple questions. If you know so much about this tree, why haven't you gotten a leaf yourself?"]},
                    "Elf: Because I am telling the truth.":{"from":["And why should I believe you?"], "to":["Get lost.", "Let's hear it."]},
                    "Elf: Suit yourself.\n\nThe elf walks away.\n\n-----You may no longer take Elf quests-----":{"from":["Get lost."], "to":["*Leave*"]},
                    "Elf: You think you're trying to be sneaky, don't you?":{"from":["First I have a couple questions. If you know so much about this tree, why haven't you gotten a leaf yourself?"], "to":["I'm not sure if I understand."]},
                    "Elf: Everything comes with a price. Lately, the plants in our garden have started dying unexpectedly, one second normal, the next yellow and shriveled. Find a cure and the information is yours. Take a look at the plants and then report back to me.":{"from":["I'm not sure if I understand.", "Let's hear it.", "Please, tell me everything!"], "to":["Quest Obtained"]}}


elf1 = Character("The elf is a tall woman in common clothes. She seems slightly peculiar, but you can't but your finger on why.", "Elf1", "The garden is a place of magic. So beautiful.", "What do you want, human sympathizer?", elf1_conversation, "No Elf")


#second conversation
elf2_conversation = {"Elf: You're back so soon?":{"from":[""], "to":["The plants have been poisoned. Who could make an antidote?", "There were these weird orange markings near the base. Do you know what they could be?"]},
                    "Elf: Poisoned? Poisoned… The herbalist. She has a hut by the river. She should be able to fix up an antidote, afterwards, return to me.":{"from":["The plants have been poisoned. Who could make an antidote?"], "to":["Quest Updated"]},
                    "Elf: Orange marks… no… it couldn't be… but what if it is? It's from the Legend. It is a disease that was given as punishment to us elves for deception. It sucks magic out of your body. Ooooh...it's terrible. Go to the herbalist. She lives in a hut by the river. She should be able to fix up an antidote, afterwards, return to me.":{"from":["There were these weird orange markings near the base. Do you know what they could be?"], "to":["Quest Updated"]}}

elf2 = Character("The elf rushes toward you.", "Elf2", "Did you find the Herbalist?", "Why would I talk to you again?", elf2_conversation, "Elf1++")


#first conversation with the herbalist
herbalist1_conversation = {"Herbalist: What do you need?":{"from":[""], "to":["It's the elven plants. They're all dying. There's some orange web-like things that are poisoning them."]},
                          "Herbalist: I knew it would happen, the Cleansing. The vital ingredient for the antidote, Elven Roots, grow underground. They grow only in the alpine regions and only Greary Bugs can detect them. There should be some bugs on the river bank -- you just need to catch them. Bring the root back to me so that I can make the antidote. Run, before you are the next victim!":{"from":["It's the elven plants. They're all dying. There's some orange web-like things that are poisoning them."], "to":["Quest Updated"]}}

herbalist1 = Character("The herbalist is hunched over and walks with a wooden cane. She has friendly eyes and a welcoming smile.", "Herbalist1", "You must have lost your way. There's nothing interesting here.", "You must have lost your way. There's nothing interesting here.", herbalist1_conversation, "Elf1+++")


#second conversation with the herbalist
herbalist2_conversation = {"Herbalist: Did you find it? Bring it here.":{"from":["Elven Root"], "to":["Yes. Here it is. (Give Elven Roots)"]},
                          "Herbalist: Fly back to the elves, and warn them that the end is coming.":{"from":["Yes. Here it is. (Give Elven Roots)"], "to":["Quest Updated"]}}

herbalist2 = Character("The Herbalist is busy preparing something, but when she sees you, she stops her work.", "Herbalist2", "Hide! The Cleansing has arrived!", "Hide! The Cleansing has arrived!", herbalist2_conversation, "Elf1++++++")


#when you return to the elf
elf3_conversation = {"Elf: Ah...you're back.":{"from":[""], "to":["Yes, here is the antidote. Now what do you know about the tree?"]},
                    "Elf: I really did think you were smarter, you know. I know nothing of it, of course. You need to embrace the game! Play me!":{"from":["Yes, here is the antidote. Now what do you know about the tree?"], "to":["I'm leaving now.", "No need to. I know you're lying."]},
                    "As you leave, the elf begins to laugh.":{"from":["I'm leaving now."], "to":["Quest Failed"]},
                    "Elf: Not a believer, I see. Well, I do know who knows about this tree.":{"from":["No need to. I know you're lying."], "to":["Who?"]},
                    "Elf: The Princess Lyra.":{"from":["Who?"], "to":["How do I get to her?"]},
                    "Elf: She resides in the Tower.":{"from":["How do I get to her?"], "to":["Quest Succeeded"]}}

elf3 = Character("At the sound of your voice, the elf comes toward you.", "Elf3", "Please help. Our gardens are our livelihood.", "You are nowhere near worthy of my time. Leave.", elf3_conversation, "Elf1+++++++")


#when you first meet the princess
princess1_conversation = {"Princess Lyra: It's a pleasure to formally meet you. What should I call you?": {"from":[""], "to":["You can call me Rowan, Princess.","Why should I tell you, after you lied about your identity?"]},
                         "Princess Lyra: And you can call me Lyra, Princess of the southern elves. Now, I have information on the tree of healing... but first I need your help with something else.":{"from":["You can call me Rowan, Princess."], "to":["And what would that be?", "I've had enough of your deception. Give me the information."]},
                         "Princess Lyra: You've earned my trust. That doesn't mean I have to have yours. I will give you the information, with or without your name. I also must request your help again.":{"from":["Why should I tell you, after you lied about your identity?"], "to":["And what would that be?", "I've had enough of your deception. Give me the information."]},
                         "Princess Lyra: Of course. Rumor has it that the forest is a maze of trees. You will have to remember your exact path if you want a chance of getting back out. Are you sure you don't want to help me? I have something which you will need if you want to venture into the forest.":{"from":"I've had enough of your deception. Give me the information.", "to":["I don't need your help, so you won't get mine.", "Actually, what do you need?"]},
                         "Princess Lyra: Overconfidence leads to arrogance. Arrogance leads to failure. Goodbye.\n\nThe princess strides away.\n\n-----You may no longer take Elf quests-----":{"from":["I don't need your help, so you won't get mine."], "to":["*Leave*"]},
                         "Princess Lyra: A terrible tragedy has occurred, someone has stolen my rose plant.":{"from":["Actually, what do you need?"], "to":["What's so important about a silly plant?", "So you just want me to get the rose back to you?"]},
                         "Princess Lyra: First, your information. Rumor has it that the forest is a maze of trees. You will have to remember your exact path if you want a chance of getting back out. All I ask of you is the safe return of my rose plant, which some foolish being has swiped.":{"from":["And what would that be?"], "to":["What's so important about a silly plant?", "So you just want me to get the rose back to you?"]},
                         "Princess Lyra: That 'silly plant' is the source of all my magic, without it I have no way to protect my people. I need you to find out who did it and get it back to me. The suspects are my personal Royal Guard, my brother Prince Aywin, and a measly Human Scout that we caught wandering the camp earlier this morning.":{"from":["What's so important about a silly plant?"], "to":["Quest Obtained"]},
                         "Princess Lyra: I need you to find out who stole the plant. Then find the plant and bring it back to me. The suspects are my Royal Guard, my brother Prince Aywin, and a measly Human Scout that we caught wandering the camp earlier this morning.":{"from":["So you just want me to get the rose back to you?"], "to":["Quest Obtained"]}}

princess1 = Character("The Princess beckons you inside of the tower. She looks oddly similar to the elf which you talked to earlier. You ascend a flight of stairs to a room with elaborate decoration.", "Princess Lyra1", "Go. Work.", "I'm a bit busy. Let's talk later.", princess1_conversation, "Elf1++++++++s")
#Elf1++++++++s

#Question the Prince
prince_conversation = {"Prince Aywin: Hello.":{"from":[""], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?"]},
                      "Prince Aywin: I was in my quarters, obviously. Every single night I retire to my quarters immediately after supper. Lyra must have had another one of her nightmares; I woke up to her shouting at some point in the middle of the night. She was peacefully asleep after a few minutes though.":{"from":["Where were you last night?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                      "Prince Aywin: Of course I do, she's my sister. I go in there all the time to get the stuff she took from me.":{"from":["Do you have access to the Princesses room?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                      "Prince Aywin: I saw the guard searching in the warehouse while I was on my daily walk. I think she might have a lead as to where it is.":{"from":["Do you know where the plant could be?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                      "Prince Aywin: I think it was the human. Why else would she be in the encampment. It can't be a coincidence. Lyra's guard on the other hand, is her most trusted advisor and we've known her since we were kids. There's no way she would ever do anything to hurt us.":{"from":["Do you have any evidence against the other two?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                      "Prince Aywin turns away.":{"from":["Farewell"], "to":["Quest Updated"]}}

prince1 = Character("Prince Aywin looks almost exactly like Princess Lyra. He is slightly taller than her with significantly darker eyes.", "Prince Aywin1", "Please find out who did this.", "We'll find who did this, with or without you", prince_conversation, "Elf2+")

#Question the guard
guard_conversation = {"Royal Guard: Fire away.":{"from":[""], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?"]},
                     "Royal Guard: I was with the princess like always. She went to bed not long after dark, it was a very uneventful night. I almost fell asleep in the middle of the night. I didn't hear anyone enter her quarters. The thief must have come in while we were at breakfast.":{"from":["Where were you last night?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                     "Royal Guard: Yes, I do. Anywhere Lyra goes, I go. No one came into the room while we were there.":{"from":["Do you have access to the Princesses room?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                     "Royal Guard: Yes and no. Aywin's guard didn't notice him moving around last night so he couldn't have done it. The human scum was found just before breakfast. The princess didn't notice her Rose was missing until we returned for her to get ready to meet with the human commander. Of course we cancelled the meeting immediately. Anyway, I think the human did it.":{"from":["Do you have any evidence against the other two?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                     "Royal Guard: I have no idea. The human probably would know.":{"from":["Do you know where the plant could be?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                     "The Royal Guard turns away.":{"from":["Farewell"], "to":["Quest Updated"]}}

guard1 = Character("The Royal Guald wears silver armour and wields a broad sword and has her hair in a loose braid.", "Royal Guard1", "At your service.", "Of course you weren't up to a task only fit for a true elf.", guard_conversation, "Elf2++")

#Question the human
scout_conversation = {"Human Scout: I promise you I didn't do anything.":{"from":[""], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?"]},
                     "Human Scout: I was in the warehouse. I thought the elves had stolen our supplies and I was going to be a hero by getting them back.":{"from":["Where were you last night?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                     "Human Scout: How would I? I don't even know who the princess is or why I'm here. Are they going to hurt me? I swear I didn't do anything wrong.":{"from":["Do you have access to the Princesses room?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                     "Human Scout: Actually the opposite, I may not completely know what's happening but I've heard the two of them speaking all morning. The one in fancy clothes talks tough but he is very worried about the Princess, I don't think he would ever do anything to hurt her.":{"from":["Do you have any evidence against the other two?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                     "Human Scout: I think I heard someone rifling around in the warehouse while I was there last night. I was hiding in behind some crates so I didn't see who it was.":{"from":["Do you know where the plant could be?"], "to":["Where were you last night?", "Do you have access to the Princesses room?", "Do you have any evidence against the other two?", "Do you know where the plant could be?", "Farewell"]},
                     "The Human turns away.":{"from":["Farewell"], "to":["Quest Updated"]}}

scout = Character("The Human stands out among the elves, with tanner skin, smaller ears, and a shorter stature.", "Human Scout1", "I promise I didn't to this. I swear.", "Why didn't you prove my innocence?", scout_conversation, "Elf2+++")
#Accusation time
accusation_conversation = {"Princess Lyra: What is your verdict?": {"from":[""], "to":["It was Prince Aywin.", "It was your Royal Guard.", "It was the human.", "I don't know yet."]},
                          "Princess Lyra: I don't believe you.\n\nPrince Aywin: Becuase it's not true. I would never hurt my sister. You're crazy!":{"from":["It was Prince Aywin."], "to":["Quest Failed"]},
                          "Royal Guard: She doesn't deserve the magic, I do! With her in charge, we have no chance of winning this war! I'm the one with training in fighting and she's just a child. I should be the one leading this army.\nPrincess Lyra: My own guard? How could it be my own guard? Please find the rose and bring it back to me.":{"from":["It was your Royal Guard."], "to":["Quest Updated"]},
                          "Human Scout: No no, I didn't do it. I- I just wanted to help my people.\n\nPrincess Lyra: I'm not buying that, but I see no way that this scrawny, incomptent -- thing -- could be capable of stealing such powerful magic.":{"from":["It was the human."], "to":["Quest Failed"]},
                          "Well then, get to work!":{"from":["I don't know yet."], "to":["*Leave*"]}}

accusation1 = Character("You can almost hear the buzz of tension.", "Princess Lyra2", "Who did it?", "You are no help at all. Leave my sight.", accusation_conversation, "Elf2++++")

princess2_conversation = {"Princess Lyra: Did you find my rose?": {"from":["Rose"], "to":["Yes (Give Rose)", "No."]},
                         "Princess Lyra: I will forever be in your debt.":{"from":["Yes (Give Rose)"], "to":["Quest Succeeded"]},
                         "Princess Lyra: Keep looking. It can't be far.":{"from":["No."], "to":["*Leave*"]}}

princess2 = Character("You can plainly see the Princesses excitement in her face.", "Princess Lyra3", "Please find my rose.", "I can't believe my guard would do this to me, but I still don't have my rose. I'll be sending out search parties to track it down.", princess2_conversation, "Elf2+++++")

princess3_conversation = {"Princess Lyra: I can not thank you enough for returning my magic to me. With this, I can say without a doubt that you are a trustworthy individual. Would you be willing to retrieve the healing tree for the elven army? With it, we will have a much greater chance of winning this stalemate of a war.":{"from":[""], "to":["Absolutely.", "I can't. Not now."]},
                         "Princess Lyra: Thank the Earth. We elves will forever be in your debt. Would you like some guidance for the journey?":{"from":["Absolutely."], "to":["That would be greatly appreciated.", "I can do it on my own."]},
                         "Princess Lyra: Living in the forest is a beast of great power. It is said to be stronger than any living creature but dumber than most. Simply meaning, you will have to trick it into leaving the tree. After you have the item, you won't have long to escape before it catches you. The last adventurers we sent out were determined that the tree was east of the forest entry and they never found anything of note, try going west. Some of our magical plants might help you defeat the beast. I wish you the best of luck.":{"from":["That would be greatly appreciated."], "to":["Quest Obtained"]},
                         "Princess Lyra: Then I wish you the best of luck. Feel free to take some plants, they may just be the help you need on your journey.":{"from":["I can do it on my own."], "to":["Quest Obtained"]},
                         "Princess Lyra: Oh… I see. Goodbye then.":{"from":["I can't. Not now."], "to":["*Leave*"]}}

princess3 = Character("Her voice beckons you closer.", "Princess Lyra4", "Thank you again for your help. When you're free, I have another task for you.", "We need the tree. All of us.", princess3_conversation, 'Elf2++++++s')

commander2_conversation = {"Commander Cedric: Hello again doctor. Thank you for convincing Tristan to return the supplies. He finally asked me for help and we worked out a way to get him the food and medicine he so desperately needs. You have officially proven yourself worthy of retrieving the healing tree for us. Will you accept the task?":{"from":[""], "to":["Yes I will.", "No I won't. Not yet at least."]},
                          "Commander Cedric: Wonderful. Do you want some advice on finding it?":{"from":["Yes I will."], "to":["That would be great, thank you.", "No thank you. I'll just start now."]},
                          "Commander Cedric: You must enter the forest and talk with the beast guarding the tree. If you upset him, he will forcefully remove you from the forest and there's no way anyone could fight against him. My advice is to trick him into leaving the tree and then getting a piece of it. Keep in mind, he will notice the tree being disturbed so you will have to get out of there before he catches up to you. The last adventurers we sent out were determined that the tree was west of the forest entry and they never found anything of note, try going east. Feel free to take some food from the warehouse, it might help you defeat the beast.":{"from":["That would be great, thank you."], "to":["Quest Obtained"]},
                          "Commander Cedric: Good luck then mighty traveler.":{"from":["No thank you. I'll just start now."], "to":["Quest Obtained"]},
                          "Commander Cedric: I understand. I hope you succeed.":{"from":["No I won't."], "to":["*Leave*"]}}

commander2 = Character("He gestures to you to talk to him.", "Commander Cedric2", "You have proven yourself a helpful hand. If you get the time, I would like your help to finally retrieve the healing tree for my legion.", "If we don't get the tree, the elves will win.", commander2_conversation, "Human2++s")
#Human2++s
#Talk to the beast
beast_conversation = {"Beast: Who are you and why are you here?":{"from":[""], "to":["I am Rowan. I am here to take the tree of healing.", "I am here to warn you of an incoming attack for your tree. The elves will be here in minutes to steal it from you.", "Why do you need to know?"]},
                     "Beast: I will never let you have it. I will do anything to protect the tree. I was created for this purpose and this purpose only.":{"from":["I am Rowan. I am here to take the tree of healing.", "Well I'm going to take it anyway.", "I am going to take it from you."], "to":["Restart"]},
                     "Beast: Where will they be attacking from? I must stop them.":{"from":["I am here to warn you of an incoming attack for your tree. The elves will be here in minutes to steal it from you.", "There is an elf attack incoming."], "to":["They will be coming from the south. Hurry to stop them."]},
                     "Beast: I am the protector of the healing tree. I can not let anyone take it.":{'from':["Why do you need to know?"], "to":["Well I'm going to take it anyway.", "I understand, and I am here to offer you some vital information towards protecting the tree.", "You can't protect it forever, beast."]},
                     "Beast: What is it, mortal.":{"from":["I understand, and I am here to offer you some vital information towards protecting the tree."], "to":["I am here to warn you of an incoming attack for your tree. The elves will be here in minutes to steal it from you."]},
                     "Beast: How do you know?":{"from":["You can't protect it forever, beast."], "to":["I am going to take it from you.", "There is an elf attack incoming."]},
                     "The beast leaves to the south, crushing various plants in its path. You are now alone in the forest. You see the healing tree, infront of you, giving off a whitish glow. All you need is one branch.":{"from":["They will be coming from the south. Hurry to stop them."], "to":["Quest Updated"]}}

beast = Character("The beast is a dragon, its skin a deep purple, its eyes bright yellow. It slowly turns its head to the left and to the right, as if to sniff out danger.", "Beast1", "This is mine. Mine.", "This is mine. Mine.", beast_conversation, "Final+")

                              
troll = Character("The troll walks with his head down, and you can't help but notice his ragged clothes.", "Troll1", "Go home. That is where you will find the answers. Everything is a circle, you know? Round...round...infinite...you always end up where you started.", "We are all creations...conflict is pointless...there is no tree. It's a thing of legend that they believe is real just so they can fight another day.", {}, "Troll")
                              
                              
fail_end = "\nThe elves and the humans are different, now. They have no meaning. It's as if they are talking to a wall. Or a see-through person. Sadness? Loneliness?  No. You feel the same as before. As if none of your adventures in this world changed you, as if none of its people changed you. As if you were a bystander, watching this world happen. You weren't supposed to know. You were supposed to fail.\n\nSuddenly, everything around you is gone. All you can feel is cool air on your face."
            
#Item objects
o1 = Item('Branch', 'a branch of the healing tree', 'A branch from the healing tree with a faint glow of magic.', 'A branch from the healing tree with a faint glow of magic.', 'Final++', 'light', False, False)
o2 = Item('Human food', 'some human food that must have been abandoned', "Some dried goods from the human territory.", 'Some dried goods from the human territory.', 'Final+', 'light', False, False)
o3 = Item('Elven plant', 'some elven plants with purple stems', "Orange webs tangle within the many crops. Some of the plants have already started wilting. They must have some sort of disease. It won't be long until the poison takes over and kills all of them plants.", 'Unidentifiable elven plants.', 'Elf1+', 'light', False, False)
o15 = Item('Healthy elven plant', 'some healthy elven plants', 'All the plants are already back in full health. Most of the crops are for food but some of them appear to be for medicine and magic purposes. How fast they grow! Before your very eyes their height increases inches and then feet.', 'Healthy elven plants. I wonder what they do?', 'Final+', 'light', False, False)
o4 = Item('Rose', 'a rose', 'A small potted plant, likely a cutting of a much larger one. A single purple rose with blue accents blooms, pulsating magical energy.', 'You see a strange looking rose. You have no need for it.', 'Elf2++++++++', 'light', False, False)
o5 = Item('Crate', 'a crate used to store goods', 'A wooden box just like the many others in the warehouse. Too heavy to pick up but moveable if you tried to push it.', 'Crate', 'Elf2+++++', 'heavy', False, False)
o6 = Item('Bug', 'a swarm of bugs', 'The bright blue bugs move too fast to grab with your bare hands but if you had a contraption you could collect them easily. These must be the bugs the herbalist was talking about.', 'Just bugs flying around. You have no use for them.', 'Elf1++++', 'heavy', False, False)
o7 = Item('Shovel', 'a shovel', "A simple shovel made of metal with a wooden handle. You can use the command 'dig'.", "A simple shovel made of metal with a wooden handle. You can use the command 'dig'.", 'All', 'light', False, False)
o8 = Item('Elven root', 'some elven roots', "A root that the bugs you've trapped seem strangely drawn to.", 'A simple root.', 'Elf1+++++', 'heavy', False, False)
o9 = Item('Bug trap', 'a bug trap', "A small metallic trap with bug bait in a small compartment. This could be helpful in collecting bugs, if the need arises. You can use the command 'catch ' and an object name.", "A small metallic trap with bug bait in a small compartment. This could be helpful in collecting bugs, if the need arises. You can use the command 'catch ' with an object name", 'All', 'light', False, True)
o10 = Item('Axe', 'an axe', "A simple axe made of metal with a wooden handle. Usefull for chopping wood. You can use the command 'use axe'", "A simple axe made of metal with a wooden handle. Usefull for chopping wood. You can use the command 'use axe'", 'All', 'light', False, False)
o11 = Item('Mirror', 'a tall mirror', "A glass mirror in a simplistic wooden frame. An unfamiliar face stares back at you. You have small ears with slightest point at the end, and you can't help noticing you're just barely too tall for the average human. Your shoulders are slender for a human but not so much that it's unheard of and your eyes are definitely not those of a human.", "An unfamiliar face stares back at you. You have small ears with slightest point at the end, and you can't help noticing you're just barely too tall for the average human. Your shoulders are slender for a human but not so much that it's unheard of and your eyes are definitely not those of a human.", 'All', 'heavy', False, False)
o12 = Item('Table', 'a table', 'A simple table.', 'A simple table.', 'All', 'heavy', False, False)
o13 = Item('Paper', 'a folded piece of paper', "\n\nWelcome to text adventure! Here you can explore a unique world and complete various quests using simple text commands. \n\nUse commands 'go north', 'go south', 'go east', and 'go west' to navigate the world. There are certain areas of the map which you can 'enter' and 'exit'. These locations include 'human territory', 'elf territory', 'forest', and 'tavern'. To enter one of these places, type 'enter ' and then the location. You can only enter these places from certain points on the map, however. \n\nWhile inside the tavern you must use commands 'go left' and 'go right' to navigate. \n\nAs you explore the world, you may encounter characters you wish to interact with. To do so, type 'talk to ' and then the character name. In certain locations, you can type 'talk to elf'. Otherwise, characters names will be clear and in the title case. When in dialogue, enter the number beside the dialogue option that you wish to choose. \n\nOnce you have received a quest, you can enter ‘q’ to get a quick refresher on your current task. You may also enter ‘clear quest’ if you wish to get rid of your current quest, but you won’t be able to do anymore quests for the group that you were working for. Make sure to pay close attention to what NPCs say for tips on how to finish each quest \n\nThere are also objects that you can interact with around the world. Some objects you can learn more about by entering 'inspect ' and the name of the object. Be warned, some object descriptions change the more you interact with and learn about the world and the people in it. \n\nThere are also objects you can add to your inventory by using the command 'take ' and the name of the object. This comes in handy when you need to use an object or bring an object somewhere else. You can see what's in your inventory at any time by typing 'open inventory'. \n\nThere are some objects that are too heavy for you to take. On rare occasions you can 'move' these objects by entering 'move ' and the name of the object. \n\nThere are also different ways to use objects. Use your best judgement. If nothing happens, make sure you spelled everything correctly. It's also possible you tried to use an object in a way it can't be used. This game is all about exploration, so don't be afraid to mess around.\n\nAt any time, you may type 'end game' to end the game. Your progress will not be saved.\n\nPress 'i' at any time to get a list of all available commands.\n\n", "Welcome to text adventure!", 'All', 'light', False, True)
o14 = Item('Lantern', 'a lantern', 'A regular gas lantern with an easy to understand lighting mechanism.', 'A regular gas lantern with an easy to understand lighting mechanism', 'All', 'light', False, True)

o16 = Item('Door', 'a heavy wooden door', 'Ornately carved out of old oak, if it was a person, you imagine it would be a wise sage.', 'Ornately carved out of old oak, if it was a person, you imagine it would be a wise sage.', 'All', 'heavy', True, False)
o17 = Item('Dresser', 'a simple dresser', "The dresser is made out of mahogany. It's red hues remind you of fire...", "The dresser is made out of mahogany. It's red hues remind you of fire...", 'All', 'heavy', True, False)                        
o18 = Item('Lantern', 'elven lanterns', 'Hanging lights made of dark metal that glow purple with magical fire', 'Hanging lights made of dark metal that glow blue with magical fire', 'All', 'heavy', True, False)                              
o19 = Item('Flag', 'elven flags', 'Triangular shaped purple flags with blue borders and elven insignia in the center. Each one has signs of being hand sewn, yet each one is still almost identical to the next', 'Triangular shaped purple flags with blue borders and elven insignia in the center. Each one has signs of being hand sewn, yet each one is still almost identical to the next', 'All', 'heavy', True, False)
o20 = Item('Table', 'tables', 'Large wooden tables that each could sit up to eight patrons', 'Large wooden tables that each could sit up to eight patrons', 'All', 'heavy', True, False)
o21 = Item('Chair', 'chairs', 'Made out of the same type of wood as the tables. There are probably fifty scattered around the tavern and more stacked at the edge of the room', 'Made out of the same type of wood as the tables. There are probably fifty scattered around the tavern and more stacked at the edge of the room', 'All', 'heavy', True, False)                              
o22 = Item('Bunk bed', 'bunk beds', 'The bunks are as rudimentary as possible, made out of logs with hay tossed on top. The humans must spend most of their time outside. Under one of the bunks is a red alarm clock.', 'The bunks are as rudimentary as possible, made out of logs with hay tossed on top. The humans must spend most of their time outside. Under one of the bunks is a red alarm clock.', 'All', 'heavy', True, False)                              
o23 = Item('Clock', 'a clock', "Your eyes have trouble focusing on its face -- something looks wrong. There aren't any numbers and the hands move in semi-random patterns.", "Your eyes have trouble focusing on its face -- something looks wrong. There aren't any numbers and the hands move in semi-random patterns.", 'All', 'heavy', True, False)                              
o24 = Item('Personal item', 'personal items', 'A couple dirty shirts, photographs of their families, etc.. Nothing interesting.', 'A couple dirty shirts, photographs of their families, etc.. Nothing interesting.', 'All', 'heavy', True, False)                              
o25 = Item('Food', 'some food', 'Dried goods that the humans eat.', 'Dried goods that the humans eat.', 'All', 'heavy', True, False)                              
o26 = Item('Drink', 'some human drinks', 'Jars of water, likely collected from the river and stored here in the hopes of surviving the dry months of the year', 'Jars of water, likely collected from the river and stored here in the hopes of surviving the dry months of the year', 'All', 'heavy', True, False)                             
o27 = Item('Medical supplies', 'some medical supplies', 'A large collection of rudimentary medical supplies bandages, numbing cream, splints, etc.', 'A large collection of rudimentary medical supplies bandages, numbing cream, splints, etc.', 'All', 'heavy', True, False)
o28 = Item('Bed', 'a bed', 'A simple straw bed sitting underneath the window. Although the bed looks uncomfortable, you feel oddly well rested.', 'A simple straw bed sitting underneath the window. Although the bed looks uncomfortable, you feel oddly well rested.', 'All', 'heavy', True, False)
o29 = Item('Window', 'a window', 'Dark red curtains cover most of the window. Shifting them slightly shows a view of a raging river.', 'Dark red curtains cover most of the window. Shifting them slightly shows a view of a raging river.', 'All', 'heavy', True, False)                            
o30 = Item('Bar', 'a tavern bar', 'A long wooden bar. Behind it, you see shelves with nothing on them, no food, no drinks, nothing. Making you wonder, where is Torma getting the ingredients when she makes food and drinks for her patrons?', 'A long wooden bar. Behind it, you see shelves with nothing on them, no food, no drinks, nothing. Making you wonder, where is Torma getting the ingredients when she makes food and drinks for her patrons?', 'All', 'heavy', True, False)
o31 = Item('Dresser', 'some wooden dressers', 'Crude wooden drawers, likely made in haste and never fixed. Years of ware show on the handles and corners.', 'Crude wooden drawers, likely made in haste and never fixed. Years of ware show on the handles and corners.', 'All', 'heavy', True, False)

o32 = Item("Tower", "", "A stone tower with a large circular door. A few small windows line the walls, likely built to allow light in. The top of the tower is barely visible but you can tell it’s made out of wood.", "A stone tower with a large circular door. A few small windows line the walls, likely built to allow light in. The top of the tower is barely visible but you can tell it’s made out of wood.", "All", "heavy", True, False)
o33 = Item("Door", "", "An almost perfectly round door, with a length of about eight feet. It has a small window but you can’t seem to see through it.", "An almost perfectly round door, with a length of about eight feet. It has a small window but you can’t seem to see through it.", "All", "heavy", True, False)
o34 = Item("Yellow Bird", "", "A small yellow song bird perched on a branch. It’s too high up for you to reach it.", "A small yellow song bird perched on a branch. It’s too high up for you to reach it.", "All", "heavy", True, False)
o35 = Item("Campfire", "", "A circle of rocks with a few pieces of charcoal. This fire has been out for a long time.", "A circle of rocks with a few pieces of charcoal. This fire has been out for a long time.", "All", "heavy", True, False)
o36 = Item("Moss", "", "Soft, green moss lines many of the rocks and sticks surrounding the river.", "Soft, green moss lines many of the rocks and sticks surrounding the river.", "All", "heavy", True, False)
o37 = Item("Cabin", "", "A well built log cabin, that looks hardly big enough to hold a single room. The only door in is locked and all the windows are closed tight.", "A well built log cabin, that looks hardly big enough to hold a single room. The only door in is locked and all the windows are closed tight.", "All", "heavy", True, False)
o38 = Item("Plant", "", "Various flowers, herbs, vegetables, and fruits grow plentifully here.", "Various flowers, herbs, vegetables, and fruits grow plentifully here.", "All", "heavy", True, False)
o39 = Item("Plant", "", "Ferns, lichen, wildflowers, and other small plants can be found surrounding the area.", "Ferns, lichen, wildflowers, and other small plants can be found surrounding the area.", "All", "heavy", True, False)
o40 = Item("Trees", "", " Mostly native trees with a few planter boxes growing off of them.", " Mostly native trees with a few planter boxes growing off of them.", "All", "heavy", True, False)
#o41 = Item("Plant", "", "Herbs, flowers, vegetables, and fruits sectioned off and being tended to by various elves.", "Herbs, flowers, vegetables, and fruits sectioned off and being tended to by various elves.", "All", "heavy", True, False)
o42 = Item("Fruit", "", "Fruits you don’t quite recognize but are  similar to those you can almost remember. You get the feeling it wouldn’t be smart to try eating them.", "Fruits you don’t quite recognize but are  similar to those you can almost remember. You get the feeling it wouldn’t be smart to try eating them.", "All", "heavy", True, False)
o43 = Item("Vegetable", "", "Vegetables of various shapes and colors. You probably wouldn’t want to eat one of them.", "Vegetables of various shapes and colors. You probably wouldn’t want to eat one of them.", "All", "heavy", True, False)
o44 = Item("Megical Item", "", "Goblets, torches, it’s hard to tell what else. They have a purple glow and seem to phase in and out of existence.", "Goblets, torches, it’s hard to tell what else. They have a purple glow and seem to phase in and out of existence.", "All", "heavy", True, False)
o45 = Item("Animal", "", "Most of these creatures have some resemblance to animals you know from before, but they seem to be wrong in some strange way.", "Most of these creatures have some resemblance to animals you know from before, but they seem to be wrong in some strange way.", "All", "heavy", True, False)
o46 = Item("Magazine", "", "You flip through the pages, which are all blank. Only the front cover has an image, which seems to change between portraits of people you've never met every time you look at it.", "You flip through the pages, which are all blank. Only the front cover has an image, which seems to change between portraits of people you've never met every time you look at it.", "All", "heavy", True, False)
                              
                              
#Location class
class Location:
    def __init__(self, name, message, items, npcs):
        self.name = name
        self.message = message
        self.items = items
        self.npcs = npcs

#Locations and descriptions (most descriptions need to be changed, it's just a start)
l1 = Location('tavern', "You enter a large clearing. The sun is shining and the sky is perfectly clear, the grass below you is yellow and dry. Directly in front of you is a small path leading south into a dense forest. A well traveled path stands to the west. Countless footprints, horse tracks, and wheel marks litter the ground leading to a large open field. It's hard to make out from this far away, but you can tell there are a few rudimentary buildings and many people hustling to get work done. To the east purplish lanterns illuminate a covered path into the forest. You would have to get closer to know where they lead. The tavern blocks your view to the north, but you hear the rushing of water.", [o18], [])
l2 = Location('river', 'A large river, too ferocious to pass, rages on to the north of you. No living creature could survive currents like those. The ground is rocky, gray, with splashes of green of moss.', [o6, o36], [])
l3 = Location('forest', 'A dense forest stretches on to the south. From deep in the forest, you can hear the rumbling breath of something much too big to be trifled with.', [], [])
l4 = Location('canyon', 'A canyon lays to the west of you, too steep to climb down and too wide to cross. A worn path coming from the east turns north.', [o10], [])
l5 = Location('river/mountain', "To the north you hear river rapids and your east you see tall snowy mountains. An older elf you assume to be the Herbalist hobbles around a garden watering her various plants in a large garden. Behind the garden stands a small cabin. The woman doesn't seem to notice your appearance.", [o7, o37, o38], [herbalist1, herbalist2])
l6 = Location('river/canyon', "To the north a river rages on and to the west you see a canyon. A worn path leads into what you assume to be human territory.", [], [])
l7 = Location('canyon/forest',"A canyon lays to the west and a great forest to the south. You notice a small man with wild hair, a large nose, and small but pointed ears. He appears to be a middle aged Troll.", [], [troll])
l8 = Location('forest/mountains', "You hear the sounds of a forest to the south. Snow peaked mountains reach into the sky, blocking you from traveling east. Trees litter the area with a few hard to define plants.", [o8, o39], [])
l9 = Location('mountains', "Through the lit path you enter an encampment adorned with blue and purple flags. This must be elf territory. The temporary structures seem to be intertwined with the surrounding flora. Further east you notice tall mountains that tower above you.", [o19], [])
l10 = Location('tavern main room', 'You find yourself in a large tavern common room filled with tables and chairs, a few various people are sitting at tables chatting or just simply enjoying a meal. At the edge of the room there is a long bar with a gruff but kind looking dwarf. You overhear someone call her Torma. The door to return to your room is to the left.', [o20, o21, o30], [torma1, torma2])
l11 = Location('tavern left room', "You find yourself in the room in which you woke up. You see a mirror, a table, a dresser, a simple bed, and a window. To the right is a door which leads to the tavern.", [o9, o11, o12, o13, o14, o16, o17, o28, o29], [])
l12 = Location('human territory main', 'You find yourself in a large courtyard. The area is bustling- everywhere you look you can see a different human toiling away. On one side, some type of sword training is taking place. Near the back, Commander Cedric surveys his people.', [], [commander, commander2])
l13 = Location('human north', 'You enter a large building filled with bunk beds, dressers, various personal items, and a few tired soldiers. You make out the names of two of them -- Marco and Ray. Candles light the barracks, making shadows dance on the walls.', [o22, o23, o24, o31], [fighters])
l14 = Location('human south', 'You enter a simplistic building holding food, drinks, medical supplies, and more. Many humans are organizing the supplies, including one man with a bright green shirt.', [o2, o26, o27, o25], [tristan])
l15 = Location('elf main', "In front of you stands a tower, the only elven building that is taller than the trees. It is made completely of stone, except for a large circular door. It's almost tall enough that you can't see the top. Elves populate the square infront of you, going about their daily business.", [o32, o33], [elf1, elf2, elf3, princess1, princess2, princess3, accusation1, prince1, guard1, scout])
l16 = Location('elf north', 'You enter a vast garden that is intertwined with the trees and local plants. Many colorful fruits and vegetables are being harvested by a few young elves.', [o3, o15, o40, o42, o43], [])
l17 = Location('elf south', "You see a storage building guarded by elves. It's smaller structure filled with magical items and a few animals you've never seen before. Under one pile, you see what seems to be a magazine.", [o4, o5, o44, o45, o46], [])
l18 = Location('1', 'Trees. All around you. Tall and stern.', [], [])
l19 = Location('2', 'A few trees have been cut down here.', [], [])
l20 = Location('3', 'Trees. All around you. Tall and stern.', [], [])
l21 = Location('4', "You find yourself in a small clearing with dense forest all around.", [], [])
l22 = Location('5', 'Trees. All around you. Tall and stern.', [], [])
l23 = Location('6', 'Trees. All around you. Tall and stern.', [], [])
l24 = Location('7', 'Trees. All around you. Tall and stern.', [], [])
l25 = Location('8', 'Trees. All around you. Tall and stern.', [], [])
l26 = Location('9', 'Trees. All around you. Tall and stern.', [], [])
l27 = Location('10', 'You see a bright yellow bird.', [o34], [])
l28 = Location('11', 'Trees. All around you. Tall and stern.', [], [])
l29 = Location('12', 'Trees. All around you. Tall and stern.', [], [])
l30 = Location('13', 'Trees. All around you. Tall and stern.', [], [])
l31 = Location('14', 'Trees. All around you. Tall and stern.', [], [])
l32 = Location('15', 'Trees. All around you. Tall and stern.', [], [])
l33 = Location('16', 'Trees. All around you. Tall and stern.', [], [])
l34 = Location('17', 'You see the reminants of a campfire', [o35], [])
l35 = Location('18', 'Trees. All around you. Tall and stern.', [], [])
l36 = Location('19', 'Trees. All around you. Tall and stern.', [], [])
l37 = Location('20', 'Trees. All around you. Tall and stern.', [], [])
l38 = Location('21', 'Trees. All around you. Tall and stern.', [], [])
l39 = Location('22', 'You see a giant beehive in one of the low-hanging branches', [], [])
l40 = Location('23', 'Trees. All around you. Tall and stern.', [], [])
l41 = Location('24', 'Trees. All around you. Tall and stern.', [], [])
l42 = Location('25', 'Trees. All around you. Tall and stern.', [], [])
l43 = Location('26', 'Trees. All around you. Tall and stern.', [], [])
l44 = Location('27', 'Trees. All around you. Tall and stern.', [], [])
l45 = Location('28', 'Trees. All around you. Tall and stern.', [], [])
l46 = Location('29', 'A few trees have been cut down here.', [], [])
l47 = Location('30', 'Trees. All around you. Tall and stern.', [], [])
l48 = Location('31', 'Trees. All around you. Tall and stern.', [], [])
l49 = Location('32', 'Trees. All around you. Tall and stern.', [], [])
l50 = Location('33', 'Trees. All around you. Tall and stern.', [], [])
l51 = Location('34', 'Trees. All around you. Tall and stern.', [], [])
l52 = Location('35', 'Trees. All around you. Tall and stern.', [], [])
l53 = Location('36', 'Trees. All around you. Tall and stern.', [], [])
l54 = Location('37', "You enter a small clearing where a large beast looms over you. You see a branch of the healing tree that looks like it might be easy to break off. Try talking to the beast before you take the branch, though. Be reasonable.", [o1], [beast])
l55 = Location('38', 'Trees. All around you. Tall and stern.', [], [])
l56 = Location('39', 'Trees. All around you. Tall and stern.', [], [])
l57 = Location('40', 'Trees. All around you. Tall and stern.', [], [])
l58 = Location('41', 'Trees. All around you. Tall and stern.', [], [])
l59 = Location('42', 'Trees. All around you. Tall and stern.', [], [])
l60 = Location('43', 'Trees. All around you. Tall and stern.', [], [])
l61 = Location('44', 'Trees. All around you. Tall and stern.', [], [])
l62 = Location('45', 'A few trees have been cut down here.', [], [])
l63 = Location('46', 'Trees. All around you. Tall and stern.', [], [])
l64 = Location('47', 'Trees. All around you. Tall and stern.', [], [])
l65 = Location('48', 'Trees. All around you. Tall and stern.', [], [])
l66 = Location('49', 'Trees. All around you. Tall and stern.', [], [])

def take(i, command, coords):
    if 'take' in command:
        thing = command.replace('take ', '')
        atLocation = False
        for item in locations[(coords.x,coords.y)].items:
            if item.name.lower() == thing:
                atLocation = True
                if item == o1:
                    if coords.x == 28 and coords.y == 25:
                        print("\nYou prepare to grab a branch of the healing tree.")
                        locations[(coords.x,coords.y)].items.remove(item)
                        return True
                    else:
                        print("\nYou took the branch. It was added to your inventory.")
                        locations[(coords.x,coords.y)].items.remove(item)
                        if o1 not in i.items:
                            i.add_item(item)
                        return False
                else:
                    taken = i.add_item(item)
                    if taken == True:
                        locations[(coords.x,coords.y)].items.remove(item)
        if atLocation == False:
            print(f"\nYou can't take that.")
    return False
            
def open_inventory(i, command):
    if command == 'open inventory':
        i.show_items()

def talk_to(person_name, player_quest,coords, inventory):
    already = False
    available = False
    for character in locations[coords.x, coords.y].npcs:
        if character.name.lower()[:-1] == person_name.lower(): #making sure you can talk to that person
            available = True
                              
#             print(f"\n{player_quest.current_quest}")
#             print(f"\n{player_quest.succeeded}")
#             print(f"\n{character.quest}")
            
            if character.quest == player_quest.current_quest or character.quest in player_quest.succeeded and len(player_quest.current_quest) == 0 or "No" in character.quest and character.quest[3:] not in "".join(player_quest.succeeded) and player_quest.current_quest == '' or character.quest == 'All': #if you are on the correct quest
                character.meet()
                already = True
                character.start_conversation(player_quest, inventory, coords)
#                 print(coords)
#                 print("______")
#                 print(coordinates)
#                 if coords != "":
#                     coordinates = coords
#                 print(coords.x, coords.y)
                if character.name in ["Commander Cedric1", "Torma1", "Elf1", "Elf2", "Elf3", "Princess Lyra1", "Herbalist1", "Royal Guard1", "Human Scout1", "Prince Aywin1"] or character.name == "Princess Lyra2" and player_quest.current_quest == "Elf2+++++" or character.name == "Princess Lyra3" and "Elf2++++++s" in player_quest.succeeded or character.name == "Commander Cedric2" and player_quest.current_quest == "Final+" or character.name == "Princess Lyra4" and player_quest.current_quest == "Final+":
                    locations[(coords.x, coords.y)].npcs.remove(character)
                
            else:
                if not already:
                    character.interact_outside_quest(player_quest)
                    already = True
    if not available:
        print("\nThe person you're looking for isn't here.")
#     return coordinates

def move(command, coords):
    thing = command.replace('move ', '')
    if thing == 'crate':
        if coords.x == 40 and coords.y == 39:
            print("\nWith some effort you manage to slide the crate a few feet. Underneath you find a trap door. In the trap door you see a single rose.")
        else:
            print("\nThere is no crate here.")
    else:
        print("\nThere's no reason to move this.")


def dig(i,coords, q):
    if o7 in i.items:
        if coords.x == 1 and coords.y == -1:
            if q.current_quest == 'Elf1+++++':
                if o8 not in i.items:
                    q.current_quest += "+"
                    print("\nYou dig and find the antidote!")
                    o8.weight = "light"
                    i.add_item(o8)
                    o8.weight = "heavy"
                else:
                    print("\nYou already have enough antidote.")
            else:
                print("\nYou dig a little hole.")
        else:
            print("\nYou dig a little hole.")
    else:
        print("\nYou don't have a shovel or anything to dig with.")
    return(i)


def catch(command, coords, i, q):
    thing = command.replace('catch ', '')
    if thing == 'bug' or thing == 'bugs':
        if coords.x == 0 and coords.y == 1:
            if q.current_quest == 'Elf1++++':
                if o9 in i.items:
                    if o6 in i.items:
                        print("\nYou already have some bugs in your inventory. You don't need any more.")
                    else:
                        q.current_quest += "+"
                        o6.weight = "light"
                        print("\nYou successfully catch some bugs.")
                        i.add_item(o6)
                        o6.weight = "heavy"
                else:
                    print("\nYou need something to catch the bugs with.")
            else:
                print('\nYou have no reason to catch these bugs.')
        else:
            print("\nThere are no bugs here.")
    else:
        print(f"\nYou can't catch '{thing}'")
    return(i)


def inspect(command, q,coords, i):
    thing = command.replace('inspect ', '')
    atLocation = False
    inInventory = False
    if thing == 'area' or thing == 'room':
        print(locations[(coords.x,coords.y)].message)
    else:
        for item in locations[(coords.x,coords.y)].items:
            if item.name.lower() == thing:
                atLocation = True
                if thing == 'table':
                    objs = []
                    for obj in locations[(coords.x,coords.y)].items:
                        if obj.table == True:
                            objs.append(obj.title)
                    if len(objs) == 0:
                        print("A table with nothing on it.")
                    elif len(objs) == 1:
                        print(f"On the table you see {objs[0]}")
                    elif len(objs) == 2:
                        print(f"On the table you see {objs[0]} and {objs[1]}")
                    else:
                        print("On the table you see ", end = '')
                        for obje in objs:
                            if obje != objs[-1]:
                                print(f"{obje}, ", end = '')
                            else:
                                print(f"and {obje}.")

                else:    
                    if q.current_quest == item.quest or item.quest == "All":
                        print(f"\n{item.q_description}")
                        if item.name == "Elven plant":
                            q.current_quest += "+"
                    else:
                        print(f"\n{item.s_description}")
        if atLocation == False:
            for item in i.items:
                if item.name.lower() == thing:
                    inInventory = True
                    if q.current_quest == item.quest or item.quest == "All":
                        print(f"\n{item.q_description}")
                    else:
                        print(f"\n{item.s_description}")
        if atLocation == False and inInventory == False:
            print(f"\nYou can't inspect that.")

def beast(i):
    
    print()
    print("\nThe beast won't be happy once it realizes what you're doing, so don't take too long in breaking it off. Maybe there's something in your inventory that can help speed up the process? To view your inventory enter 'open inventory'. To use something from it enter 'use __'.")
    print("\nUse commands 'go north', 'go south', 'go east', and 'go west' to get to the exit of the forest! Keep in mind there are many obstacles in the way such as logs, large trees, hedges, and more. The beast is chasing you, so try not to backtrack! If you get stuck and really need to, there might be something in your inventory that can help. You only have 20 moves to escape the forest before the beast catches you, but some inventory items will slow the beast down and give you extra moves. Good luck!")
    print("\nNow quick, take the branch!")
    print("\n")
    
    oginventory = []
    for item in i.items:
        oginventory.append(item)
    
    moves = 20
    print(f"\n{moves} moves left")
    moveslist = ['outta range']
    coords.x = 28
    y = 25
    axed = False

    command = input("\n>>> ").lower()
    
    while command:
        illegal = False
        
        if command == 'use axe':
            if o10 not in i.items:
                illegal = True
                print("\nThere is no axe in your inventory!")
            elif o1 in i.items:
                illegal = True
                print("\nYou throw the axe at the beast and it dodges it gracefully. Uh-oh...")
                i.remove_item(o10)
            else:
                illegal = True
                i.remove_item(o10)
                axed = True
                print("\nThe axe saves you a lot of time and a branch falls to the ground. Take it, quick!")
        
        elif command == 'take branch':
            illegal = True
            if axed == True:
                print("\nUh-oh. The beast isn't too happy about you taking a branch off the healing tree. I hope you remember the path you took to get here- run!!")
                if o1 not in i.items:
                    i.add_item(o1)
            if axed == False:
                print("\nIf only you had used an axe or something. It takes a long time for you to break the branch off the tree and the beast is gaining on you quickly. I hope you remember the path you took to get here- run!!")
                moves -= 2
                if o1 not in i.items:
                    i.add_item(o1)
        
        elif command == 'go north':
            if coords.y + 1 > 30:
                illegal = True
                print("\nThe forest grows too dense to get through that direction. Look for a clearing to exit.") 
            elif (coords.x,coords.y+1) not in locations:
                illegal = True
                print("\nThere is a large tree blocking the way! Try going another direction.")
            elif moveslist[-1] == 'go south':
                illegal = True
                moveslist.append('go north')
                print("\nYou just came from that direction! If you go back now the beast will get you. Try going another direction or using something from your inventory to distract it while you run by. ")
            else:
                coords.y += 1
        
        elif command == 'go east':
            if coords.x + 1 > 33:
                illegal = True
                print("\nThe forest grows too dense to get through that direction. Look for a clearing to exit.")
            elif (coords.x+1,coords.y) not in locations:
                illegal = True
                print("\nThere is a fallen log blocking the way! Try going another direction.")
            elif moveslist[-1] == 'go west':
                illegal = True
                moveslist.append('go east')
                print("\nYou just came from that direction! If you go back now the beast will get you. Try going another direction or using something from your inventory to distract it while you run by. ")
            else:
                coords.x += 1
        
        elif command == 'go south':
            if coords.y - 1 < 24:
                illegal = True
                print("\nThe forest grows too dense to get through that direction. Look for a clearing to exit.")
            elif (coords.x,coords.y-1) not in locations:
                illegal = True
                print("\nThere is a giant hedge blocking the way! Try going another direction.")
            elif moveslist[-1] == 'go north':
                illegal = True
                moveslist.append('go south')
                print("\nYou just came from that direction! If you go back now the beast will get you. Try going another direction or using something from your inventory to distract it while you run by. ")
            else:
                coords.y -= 1
        
        elif command == 'go west':
            if coords.x - 1 < 27:
                illegal = True
                print("\nThe forest grows too dense to get through that direction. Look for a clearing to exit.")
            elif (coords.x-1,coords.y) not in locations:
                illegal = True
                print("\nThere is a boulder blocking the way! Try going another direction.")
            elif moveslist[-1] == 'go east':
                illegal = True
                moveslist.append('go west')
                print("\nYou just came from that direction! If you go back now the beast will get you. Try going another direction or using something from your inventory to distract it while you run by. ")
            else:
                coords.x -= 1
        
        elif command == 'use human food':
            if o2 not in i.items:
                illegal = True
                print("\nThere's no human food in your inventory!")
            elif coords.x == 28 and coords.y == 25:
                illegal = True
                print("\nYou're still in the clearing with the tree! Only use this valuable resource if you're stuck!")
            else:
                i.remove_item(o2)
                moves += 4
                print("\nYou throw the food on the ground at the feet of the beast and it stops to eat- you've temporarily distracted it! You run past it in the direction you came from.")
                if moveslist[-1] == 'go north':
                    coords.y+=1
                elif moveslist[-1] == 'go south':
                    coords.y-=1
                elif moveslist[-1] == 'go east':
                    coords.x+=1
                elif moveslist[-1] == 'go west':
                    coords.x-=1
        
        elif command == 'use elven plants':
            if o3 not in i.items:
                illegal = True
                print("\nThere are no elven plants in your inventory!")
            elif coords.x == 28 and coords.y == 25:
                illegal = True
                print("\nYou're still in the clearing with the tree! Only use this valuable resource if you're stuck!")
            else:
                i.remove_item(o3)
                moves += 4
                print("\nYou toss the magical plants behind you and they grow huge in an instant, blocking the path of the beast!")
                if moveslist[-1] == 'go north':
                    del locations[(coords.x,coords.y-1)]
                elif moveslist[-1] == 'go south':
                    del locations[(coords.x,coords.y+1)]
                elif moveslist[-1] == 'go east':
                    del locations[(coords.x-1,coords.y)]
                elif moveslist[-1] == 'go west':
                    del locations[(coords.x+1,coords.y)]
        
        elif command == 'open inventory':
            illegal = True
            print("\nInventory:")
            for item in i.items:
                print(item.name)
            print()
            moves += 1
        
        elif 'use ' in command:
            illegal = True
            invent = False
            thing = command.replace('use ', '')
            for item in i.items:
                if item.name.lower() == thing:
                    invent = True
                    print("\nYou have no use for this item against the beast.")
            if invent == False:
                print(f"\nI don't see a '{thing}' in your inventory.")

        if not illegal:
            if (coords.x,coords.y) != (28,25):
                print(locations[(coords.x,coords.y)].message)
            else:
                print("\nYou're back at the clearing where you stole the healing tree from!")
            moveslist.append(command)
        
        moves-=1
        print("\n" + str(moves) + " moves left")
        
        if moves == 0:
            print("\nThe beast catches you and throws you out of the forest. You collect yourself and look around. You're at the very edge of the forest to the south of the tavern.")
            return(False, oginventory)
        elif locations[(coords.x,coords.y)].message == "You find yourself in a small clearing with dense forest all around.":
            print("\nYou escaped from the beast.")
            if o1 not in i.items:
                i.add_item(o1)
            return(True, oginventory)
        else:
            command = input("\n>>> ").lower()



def motions(command,coords, q, game_end):
    
    coords.x = int(coords.x)
    coords.y = int(coords.y)
    
    #edges of the main map
    max_coord_pos = 1.0
    max_coord_neg = -1.0

    illegal = False
    #checks to see if you're in the tavern
    if 15 > coords.x > 5:
        intavern = True
    else:
        intavern = False
    #checks to see if you're anywhere but the main map and the tavern
    if coords.x > 15:
        inside = True
    else:
        inside = False

    #base directional commands      
    if command == 'go north':
        if intavern == False: #if you're in the tavern it skips this cuz you can't use NESW
            if inside == False:
                if coords.y + 1 > max_coord_pos:
                    illegal = True
                    print("\nThe river is too fast to pass through.") 
                else:
                    coords.y += 1.0
            else:
                if 25 > coords.y+1 > 21:
                    illegal = True
                    print("\nA wall around the human territory prevents you from going that way.")
                elif 35 > coords.y+1 > 30:
                    illegal = True
                    print("\nThe forest is too thick to pass through here.")
                elif (coords.x,coords.y+1) not in locations:
                    illegal = True
                    print("\nThere is a large tree blocking the way! Try going another direction.")
                elif coords.y+1 > 41:
                    illegal = True
                    print("\nA wall around the elven territory prevents you from going that way.")
                else:
                    coords.y+=1.0
        else:
            illegal = True
            print("\nWithout seeing the sun, you have no sense of direction! You still know your lefts and rights though...")

    elif command == 'go east':
        if intavern == False:
            if inside == False:
                if coords.x + 1 > max_coord_pos:
                    illegal = True
                    print("\nThe mountains are too steep to climb.")
                else:
                    coords.x += 1.0
            else:
                if 25 > coords.x+1 > 20:
                    illegal = True
                    print("\nA wall around the human territory prevents you from going that way.")
                elif 35 > coords.x+1 > 33:
                    illegal = True
                    print("\nThe forest grows too dense to travel that direction.")
                elif (coords.x+1,coords.y) not in locations:
                    illegal = True
                    print("\nThere is a fallen log blocking the way! Try going another direction.")
                elif coords.x+1 > 40:
                    illegal = True
                    print("\nA wall around the elven territory prevents you from going that way.")
                else:
                    coords.x+=1.0
        else:
            illegal = True
            print("\nWithout seeing the sun, you have no sense of direction! You still know your lefts and rights though...")

    elif command == 'go south':
        if intavern == False:
            if inside == False:
                if coords.y - 1 < max_coord_neg:
                    illegal = True
                    print("\nThe forest is too overgrown to pass through.")
                else:
                    coords.y -= 1.0
            else:
                if 39 > coords.y-1 >35:
                    illegal = True
                    print("\nA wall around the elven territory prevents you from going that way.")
                elif 24 > coords.y-1 > 20:
                    illegal = True
                    print("\nThe forest grows too dense to travel that direction.")
                elif (coords.x,coords.y-1) not in locations:
                    illegal = True
                    print("\nThere is a giant hedge blocking the way! Try going another direction.")
                elif 19 > coords.y-1:
                    illegal = True
                    print("\nA wall around the human territory prevents you from going that way.")
                else:
                    coords.y-=1.0
        else:
            illegal = True
            print("\nWithout seeing the sun, you have no sense of direction! You still know your lefts and rights though...")

    elif command == 'go west':
        if intavern == False:
            if inside == False:
                if coords.x - 1 < max_coord_neg:
                    illegal = True
                    print("\nThe canyon is impassable.")
                else:
                    coords.x -= 1.0
            else:
                if 40 > coords.x-1 >35:
                    illegal = True
                    print("\nA wall around the elven territory prevents you from going that way.")
                elif 27 > coords.x-1 > 25:
                    illegal = True
                    print("\nThe forest grows too dense to travel that direction.")
                elif (coords.x-1,coords.y) not in locations:
                    illegal = True
                    print("\nThere is a boulder blocking the way! Try going another direction.")
                elif 20 > coords.x-1:
                    illegal = True
                    print("\nA wall around the human territory prevents you from going that way.")
                else:
                    coords.x-=1
        else:
            illegal = True
            print("\nWithout seeing the sun, you have no sense of direction! You still know your lefts and rights though...")

#tavern commands
    elif command == 'enter tavern':
        if q.elf_failed and q.human_failed:
            answer = input(f"The tavern door is missing. Not open. Missing. And there is some sort of green mist in the doorway preventing you from looking inside. Are you sure you want to enter the tavern? (y/n)").lower()
            while answer != 'y' and answer != 'n':
                answer = input("Please type 'y' or 'n': ").lower()
            if answer == 'y':
                illegal = True
                q.remove_quest()
                print(fail_end)
                game_end = True
        else:
            if intavern == True:
                illegal = True
                print("\nYou're already in the tavern!")
            elif coords.x != 0 or coords.y != 0:
                illegal = True
                print("\nYou don't see the tavern nearby.")
            else:
                coords.y = 10
                coords.x = 10
    elif command == 'go left':
        if intavern == True:
            if coords.x - 1 < 9:
                illegal = True
                print("\nThere is no door that way.")
            else:
                coords.x-=1
        else:
            illegal = True
            print("\nIt's easier to navigate using north, south, east, and west when you're outside.")
    elif command == 'go right':
        if intavern == True:
            if 18 > coords.x + 1 > 10:
                illegal = True
                print("\nThere is no door that way.")
            else:
                coords.x +=1
        else:
            illegal = True
            print("\nIt's easier to navigate using north, south, east, and west when you're outside.")
    elif command == 'exit tavern':
        if 15 < coords.x or 8 > coords.x or 15 < coords.y or 8 > coords.y:
            illegal = True
            print("\nYou're not in the tavern.")
        elif coords.y != 10 or coords.x != 10:
            illegal = True
            print("\nThe door to leave the tavern is not in this room.")
        else:
#             print(coords.x, coords.y)
            coords.x=0
            coords.y=0
#             print(coords.x, coords.y)

#human territory commands
    elif command == 'enter human territory':
        if inside == True:
            illegal = True
            print("\nYou're already there!")
        elif coords.x != -1 or coords.y != 1:
            illegal = True
            print("\nYou don't see an entrance nearby.")
        else:
            coords.y = 20
            coords.x = 20
    elif command == 'exit human territory':
        if 22 < coords.x or 16 > coords.x or 22 < coords.y or 16 > coords.y:
            illegal = True
            print("\nYou're not in human territory.")
        else:
            coords.x=-1
            coords.y=1

#elf territory commands
    elif command == 'enter elf territory':
        if inside == True:
            illegal = True
            print("\nYou're already there!")
        elif coords.x != 1 or coords.y != 0:
            illegal = True
            print("\nYou don't see an entrance nearby.")
        else:
            coords.y = 40
            coords.x = 40
    elif command == 'exit elf territory':
        if coords.x < 35 or coords.y < 35:
            illegal = True
            print("\nYou're not in elf territory.")
        else:
            coords.x=1
            coords.y=0

#forest commands
    elif command == 'enter forest':
        if inside == True:
            illegal = True
            print("\nYou're already there!")
        elif coords.x != 0 or coords.y != -1:
            illegal = True
            print("\nYou can't enter the forest from here.")
        else:
            coords.y = 30
            coords.x = 30
    elif command == 'exit forest':
        if 35 < coords.x or 23 > coords.x or 35 < coords.y or 23 > coords.y:
            illegal = True
            print("\nYou're not in the forest.")
        elif coords.y != 30 or coords.x != 30:
            illegal = True
            print("\nThe forest is too dense to exit from here.")
        else:
            coords.x=0
            coords.y=-1
    
    else:
        illegal = True
        print("You've entered a command I don't recognize. Please try again.")

    if not illegal:
        objs = []
        for obj in locations[(coords.x,coords.y)].items:
            if obj.quest == q.current_quest or obj.quest == 'All':
                if obj.hidden == False:
                    if obj.table == False:
                        objs.append(obj.title.lower())
        if len(objs) == 0:
            print(f"\n{locations[(coords.x,coords.y)].message}")
        else:
            print(f"\n{locations[(coords.x,coords.y)].message}", end = ' ')
        if 0 < len(objs) < 2:
            print("You see ", end = '')
            print(f"{objs[0]}.")
        if len(objs) == 2:
            print(f"You see {objs[0]} and {objs[1]}.")
        if len(objs) > 2:
            print("You see ", end = '')
            for obj in objs:
                if obj != objs[-1]:
                    print(f"{obj}, ", end = '')
                else:
                    print(f"and {obj}.")        
    return((coords.x,coords.y), game_end)
        

if __name__ == "__main__":
    
    print("\n\n\nYou wake up in a small room, with no memories of who or where you are, except for your name. You are laying on a simple straw bed with light filtering in from a barely curtained window. In the room you can see a mirror hanging on the wall above a simple dresser, a small table with a few non-descript items, and a dark wooden door to the right. A sign on the wall reads 'Dragon's Whisper Tavern and Inn' Use the command 'inspect ___' to search the room.")
    #starting coords
#     coords.x = 9
#     coords.y = 10
    #dictionary of locations from above along with coordinates as key
    similar_words = {"elf" : ["elven", "elfs"], "marco and ray" : ["marco", "ray"],
                     "commander cedric" : ["cedric"], "princess lyra" : ["lyra", "princess"], 
                     "clock" : ["red alarm clock", "alarm clock"],
                     "elven plant" : ["plant", "purple stem", "elf plant"], "plant" : ["garden"],
                     "door" : ["circular door"], "take" : ["get", "pick up"], "exit" : ["leave"],
                     'elf territory' : ["elven territory", "elf encampment", "elven encampment"],
                     "human territory" : ["human encampment"], "talk" : ["speak"],
                     "i" : ["?", "help", "available commands"],
                     "healthy elven plant" : ["elven plant", "plant", "healthy plant"],
                     "yellow bird" : ["bird"], "inspect":["investigate", "check out", "examine"],
                     "window" : ["curtain", "curtains", "windows"],
                     "bug trap" : ["trap"], "paper" : ["piece of paper"]}
    locations = {
        (0.0,0.0) : l1, 
        (0.0,1.0) : l2, 
        (0.0,-1.0) : l3, 
        (-1.0,0.0) : l4, 
        (1.0,1.0) : l5, 
        (-1.0,1.0) : l6, 
        (-1.0, -1.0) : l7, 
        (1.0,-1.0) : l8,
        (1.0,0.0) : l9,
        (10,10) : l10,
        (9,10) : l11,
        (20,20) : l12,
        (20,21) : l13,
        (20,19) : l14,
        (40,40) : l15, 
        (40,41) : l16, 
        (40,39) : l17, 
        (27,30) : l18, 
        #(28,30) : l19, 
        (29,30) : l20, 
        (30,30) : l21, 
        (31,30) : l22, 
        (32,30) : l23, 
        #(33,30) : l24, 
        (27,29) : l25,
        (28,29) : l26,
        (29,29) : l27,
        (30,29) : l28,
        (31,29) : l29,
        (32,29) : l30,
        (33,29) : l31,
        #(27,28) : l32,
        (28,28) : l33,
        (29,28) : l34,
        #(30,28) : l35,
        (31,28) : l36,
        #(32,28) : l37,
        (33,28) : l38,
        (27,27) : l39,
        #(28,27) : l40,
        (29,27) : l41,
        (30,27) : l42,
        (31,27) : l43,
        (32,27) : l44,
        #(33,27) : l45,
        (27,26) : l46,
        (28,26) : l47,
        (29,26) : l48,
        (30,26) : l49,
        (31,26) : l50,
        #(32,26) : l51,
        (33,26) : l52,
        (27,25) : l53,
        (28,25) : l54,
        (29,25) : l55,
        #(30,25) : l56,
        (31,25) : l57,
        (32,25) : l58,
        (33,25) : l59,
        (27,24) : l60,
        (28,24) : l61,
        (29,24) : l62,
        (30,24) : l63,
        (31,24) : l64,
        #(32,24) : l65,
        (33,24) : l66,
        }
    #key words for motions
    motionlist = ['go', 'enter', 'exit']
    itemlist = ['take']
    new_plants = False
    i = Inventory()
    q = Quests()
    coords = Coord()
    beasttime = False
    realcommand = False
    game_end = False
    command = input("\n>>> ").lower()
    while not game_end:
        if len(command) > 1:
            commandlist = [command.split()[0], " ".join(command.split()[1:])]
            for word in commandlist:
                if word[-1] == 's':
                    commandlist[commandlist.index(word)] = commandlist[commandlist.index(word)][:-1]
                    word = word[:-1]
                for w, similar in similar_words.items():
                    if word == w or word in similar:
                        commandlist[commandlist.index(word)] = w

            command = " ".join(commandlist)
        if command == 'q':
            realcommand = True
            q.show_quest()
        elif command == 'clear quest':
            realcommand = True
            q.clear_quest()
        elif command == 'i':
            realcommand = True
            print("\n\nAvailable Commands: \n\n-Go: right (only in starting room), left (only in tavern common room), north, east, south, west. \n-Enter/Exit: tavern, elf territory, human territory, forest. \n-Inspect: most listed objects in any given area (bug trap, flags, food, etc.). \n-Take: many listed objects (bug trap, axe, elf plants, etc.). \n-Use axe (only available in certain situations). \n-Talk to: any NPC listed in a given area. \n-Open Inventory(list all items currently in the inventory) \n-Dig (must have shovel in inventory). \n-Catch Bugs (must have bug trap in inventory). \n-Move. \n-Q (see current quest). \n-I (see available commands). \n-Clear Quest. \n-End Game (progress will not be saved).\n\n")
        elif 'move' in commandlist:
            realcommand = True
            move(command,coords)
        elif 'dig' in commandlist:
            realcommand = True
            i = dig(i,coords, q)
        elif 'catch' in commandlist:
            realcommand = True
            i = catch(command,coords, i, q)
        elif 'inspect' in commandlist:
            realcommand = True
            inspect(command, q,coords, i)
        elif 'talk to' in command:
            realcommand = True
            person = command.replace('talk to ', '')
            talk_to(person, q,coords, i)
        elif command == "end game":
            realcommand = True
            game_end = True
        elif command == "open inventory":
            realcommand = True
            open_inventory(i, command)
                 
        else:
            commandlist = command.split()
            movementcommand = False
            for motion in motionlist:
                if motion in commandlist:
                    movementcommand = True
                    realcommand = True
                    newcoords = motions(command,coords, q, game_end)
                    coords.x = newcoords[0][0]
                    coords.y = newcoords[0][1]
                    game_end = newcoords[1]
                              
            if movementcommand == False:
                for item in itemlist:
                    if item in commandlist:
                        realcommand = True
                        beasttime = take(i, command, coords)
                if beasttime == True:
                    escape = beast(i)
                    if escape: ##MADE CHANGE
                        if escape[0] == True:
                            coords.x = 0
                            coords.y = -1
                            print ("\nYou beat the beast! All that hard work paid off. It is now your choice to return the branch. You can help the people you've been working with all along or you can betray them and switch sides. Doing so will allow the side you helped win the war. After that, the enemy will retreat and your allies will fill all spaces of the map. Mostly Torma's tavern.")
                            print ("\nDo you want to help the elves or help the humans?")
                            print ("\n1.Humans")
                            print ("2.Elves")
                            choice = input("\n>>> ")
                            while choice != "1" and "2":
                                print ("\nEnter a valid number")
                                choice = input("\n>>> ")
                            game_end = True
                            if choice == "1":
                                print ("\nYou have finished the game, and the humans have won the war. The elves quickly got word of the humans getting a piece of the healing tree and they surrendered without a second thought. They are quickly retreating to their homelands while the humans are celebrating at the tavern. Congratulations")
                            elif choice == "2":
                                print ("\nYou have finished the game, and the elves have won the war. The humans quickly got word of the elves getting a piece of the healing tree and they surrendered without a second thought. They are quickly retreating to their homelands while the elves are celebrating at the tavern. Congratulations!")
                                
                                    
                        else:
                            for item in escape[1]:
                                if item not in i.items:
                                    i.add_item(item)
                            i.remove_item(o1)
                            coords.x = 0
                            coords.y = -1
        if realcommand == False:
            print("You've entered a command I don't recognize. Please try again.")
            
        if "Elf1++++++++s" in q.succeeded and not new_plants:
            new_plants = True
            if o3 in locations[(40, 41)].items:  
                locations[(40, 41)].items.remove(o3)    

        if not game_end:
            command = input("\n>>> ").lower()
            realcommand = False


# In[ ]:





# In[ ]:





# In[ ]:




