#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random as ra
import numpy as np
import math


# In[2]:


# Cards will be determined by the following numbers: 3 = 3, 4 = 4... J = 11, Q = 12, K = 13, A = 14, 2 = 15
# Suits will be determined as follows: +0 => Spades, +0.25 => Clubs, +0.5 => Diamonds, +0.75 => Hearts

fulldeck = [x*0.25 for x in range(12, 64)]
ra.shuffle(fulldeck)

def reset_deck():
    global fulldeck
    fulldeck = [x*0.25 for x in range(12, 64)]
    ra.shuffle(fulldeck)


# In[3]:


# Returns the unicode number in decimal int of a card
def card_to_picture(card):
    if (card >= 14):
        card = card-13
    value = math.floor(card)
    #print(value)
    suit = 10+4*(card%1.0)
    if suit == 11:
        suit = 13
    elif suit == 13:
        suit = 11
    #print(suit)
    
    #king is actually E, queen is D
    if value == 13 or value == 12:
        value += 1
    return int(int("1f000",16)+16*suit+value)
    
#print(chr(card_to_picture(12.25)))


# In[4]:


# Returns the unicode representation of the hand
def show_hand(hand0):
    hand = ""
    for i in hand0:
        hand += chr(card_to_picture(i))
    return hand


# In[13]:


# Deal hands
p1 = fulldeck.copy()[0:13]
p2 = fulldeck.copy()[13:26]
p3 = fulldeck.copy()[26:39]
p4 = fulldeck.copy()[39:52]

p1.sort()
p2.sort()
p3.sort()
p4.sort()

p1_original = p1.copy()
p2_original = p2.copy()
p3_original = p3.copy()
p4_original = p4.copy()

playerlist = [None, p1, p2, p3, p4]
playerlist_original = [None, p1_original, p2_original, p3_original, p4_original]

def deal_hands():
    reset_deck()
    global p1, p2, p3, p4, p1_original, p2_original, p3_original, p4_original
    p1 = fulldeck.copy()[0:13]
    p2 = fulldeck.copy()[13:26]
    p3 = fulldeck.copy()[26:39]
    p4 = fulldeck.copy()[39:52]
    p1.sort()
    p2.sort()
    p3.sort()
    p4.sort()
    p1_original = p1.copy()
    p2_original = p2.copy()
    p3_original = p3.copy()
    p4_original = p4.copy()


# In[14]:


# Rules are as follows: single = 0, pair = 1, triple = 2, three-straight = 3, four-straight = 4, five-straight = 5, 6 = new rule

# Also gonna initialize topcard and last played move and turn

rule = 6
lastplay = [2.0]
topcard = 2.0
turn = 1
pass_counter = 0


# In[15]:


def next_turn():
    global turn
    global pass_counter
    turn += 1
    if turn == 5:
        turn = 1
    if pass_counter >= 3:
        global rule
        rule = 6
        global topcard
        topcard = 2.0
        pass_counter = 0


# In[16]:


# Function that gets valid moves given a hand, rule, card-to-beat
def get_moves(hand0):
    hand = hand0.copy()
    hand.sort()
    
    #remove zeros
    for i in range(len(hand)-1,-1,-1):
        if hand[i] == 0:
            hand.pop(i)
    
    values = hand.copy()
    for i in range(len(values)):
        values[i] = math.floor(values[i])
    #print(values)
    suits = hand.copy()
    for i in range(len(suits)):
        suits[i] = suits[i]%1.0
    #print(suits)

    singles = []
    # get singles
    for i in hand:
        singles.append([i])
            
    # get pairs
    pairs = []
    for i in range(len(values)):
        for j in range(len(values)):
            if values[i] == values[j] and i != j:
                pairs += [[hand[i], hand[j]]]
    for i in pairs:
        for j in pairs:
            if sorted(i) == sorted(j) and i!=j:
                pairs.remove(j)
    #print(pairs)
                
    # get triples
    triples = []
    for i in range(len(values)):
        for j in range(len(values)):
            for k in range(len(values)):
                if values[i] == values[j] == values[k] and i != j !=k and i!=k:
                    triples += [[hand[i], hand[j], hand[k]]]
    #print(triples)
    
    # get 3-straights
    three_straights = []
    for i in range(len(values)):
        for j in range(len(values)):
            for k in range(len(values)):
                if values[k] == values[j]+1 and values[j] == values[i]+1:
                    three_straights += [[hand[i], hand[j], hand[k]]]
    #print(three_straights)
                    
    # get 4-straights
    four_straights = []
    for i in range(len(values)):
        for j in range(len(values)):
            for k in range(len(values)):
                for l in range(len(values)):
                    if values[k] == values[j]+1 and values[j] == values[i]+1 and values[l] == values[k]+1:
                        four_straights += [[hand[i], hand[j], hand[k], hand[l]]]
                        
    # get 5-straights
    five_straights = []
    for i in range(len(values)):
        for j in range(len(values)):
            for k in range(len(values)):
                for l in range(len(values)):
                    for m in range(len(values)):
                        if values[k] == values[j]+1 and values[j] == values[i]+1 and values[l] == values[k]+1 and values[m] == values[l]+1:
                            five_straights += [[hand[i], hand[j], hand[k], hand[l], hand[m]]]
    
    # add proper moves based on rule
    #print("Rule is: ", rule)
    moves = []
    if rule == 0:
        moves += singles
    elif rule == 1:
        moves += pairs
    elif rule == 2:
        moves += triples
    elif rule == 3:
        moves += three_straights
    elif rule == 4:
        moves += four_straights
    elif rule == 5:
        moves += five_straights
    else:
        moves += singles
        moves += pairs
        moves += triples
        moves += three_straights
        moves += four_straights
        moves += five_straights
    
    #print(moves)
    # remove moves below topcard
    valid_moves = [[0]]
    #print("Topcard: ", topcard)
    for i in moves:
        if max(i) > topcard:
            valid_moves += [i]
    
    #print("Got valid moves... ", valid_moves)
    return valid_moves


# In[21]:


# Function that translates moves to tiers
# Returns a 13-vector with 1 if that index (tier) is playable 
def tier_moves(original_hand, valid_moves):
    tierlist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in valid_moves:
        if i == [0]:
            pass
        else:
            tierlist[original_hand.index(max(i))] = 1
    return tierlist
        
#print(tier_moves(p1, get_moves(p1, 10)))
#print(p1)

# Function that translates a tier to a move
def tier_to_move(tier, hand, original_hand):
    movelist = get_moves(hand)
    for move in movelist:
        if original_hand[tier] in move:
            return move
        else:
            return [0]
        
def move_to_tier(move, original_hand):
    if move == [0]:
        return 13
    else:
        return original_hand.index(max(move))


# In[22]:


def encode_state(neighbors_hand, tierlist):
    index = 0
    index = int("".join(str(x) for x in tierlist), 2) 
    index += (neighbors_hand-1)*8192
    return index

def decode_state(index):
    neighbors_hand = math.floor(index/8192)+1
    tierlist = bin(index%8192)
    tierlist = [int(d) for d in str(tierlist)[2:]]
    return neighbors_hand, tierlist


# In[19]:


def obs_state(player):
    # We have 13x2^13 states to observe. This functions returns a state index for the corresponding row in Q 
    # First, let's get the neighbor's hand that'll play next and our playable tiers
    neighbors_hand = 13
    tierlist = []
    if player == 1:
        neighbors_hand = len(p2) 
        tierlist = tier_moves(p1, get_moves(p1))
    elif player == 2:
        neighbors_hand = len(p3)
        tierlist = tier_moves(p2, get_moves(p2))
    elif player == 3:
        neighbors_hand = len(p4)
        tierlist = tier_moves(p3, get_moves(p3))
    elif player == 4:
        neighbors_hand = len(p1)
        tierlist = tier_moves(p4, get_moves(p4))
    
    # Now we calculate the State index 
    index = encode_state(neighbors_hand, tierlist)
    #print(index)
    
    return index


# In[20]:


# Function that plays a move
def play(player, move):
    global pass_counter
    if move == [0]:
        pass_counter += 1
        next_turn()
        return
    else:
        pass_counter = 0
    
    movelength = len(move)
    for i in move:
        player.remove(i)
    
    global topcard
    topcard = max(move)
    global lastplay
    lastplay = move
    
    #check what move it is
    move.sort()
    values = move.copy()
    for i in range(len(values)):
        values[i] = math.floor(values[i])
    
    global rule
    if movelength == 1:
        rule = 0
    elif movelength == 2:
        rule = 1
    elif movelength == 3:
        if values[0] == values[1]:
            rule = 2
        elif values[1] == values[0]+1:
            rule = 3
    elif movelength == 4:
        rule = 4
    elif movelength == 5:
        rule = 5
    
    next_turn()
    #print("New rule is:", rule)
    #print("New topcard is:", topcard)
    if player == p4:
        print("P4 plays ", move);
    elif player == p2:
        print("P2 plays ", move);
    elif player == p3:
        print("P3 plays ", move);
    else:
        print("P1 plays ", move)


# In[48]:


def newgame():
    deal_hands()
    global rule
    rule = 6
    global topcard
    topcard = 2.0
    global lastplay 
    lastplay = [2.0]
    if 3.0 in p4:
        turn = 4
    elif 3.0 in p2:
        turn = 2
    elif 3.0 in p3:
        turn = 3
    else:
        turn = 1 
    return turn


# In[47]:


import tkinter as tk
from tkinter import messagebox

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        #Get the unicode strings to render
        p1hand = ""
        for i in p1:
            p1hand += chr(card_to_picture(i))
        lastplayed = ""
        for i in lastplay:
            lastplayed += chr(card_to_picture(i))
        if topcard == 2.0 or rule == 6:
            lastplayed = "0"
        
        #these are the widgets
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Reset"
        self.hi_there["command"] = self.reset
        self.hi_there.grid(row = 0)
        
        # Move input
        self.playlabel = tk.Label(self, text="Your Move (input as 'C1, C2, C3...', where Ci is a float):", font = ("Courier", 10))
        self.playlabel.grid(row=4, column = 2)
        self.playbox = tk.Entry(self)
        self.playbox.bind("<Return>", self.play_user_move)
        self.playbox.grid(row = 4, column = 3)
        
        # Last play
        self.lp = tk.Label(self, text=lastplayed, font = ("Times", 120))
        self.lp.grid(row = 1, columnspan = 6)
        
        # Dashboard
        self.dashboard = tk.Label(self, text="P2: "+str(len(p2))+" cards left, "+"P3: "+str(len(p3))+" cards left, "+"P4: "+str(len(p4))+" cards left", font = ("Courier", 10))
        self.dashboard.grid(row = 2, columnspan = 6)
        
        # My Hand
        self.hand = tk.Label(self, text=p1hand, font = ("Times", 120))
        self.hand.grid(row = 3, columnspan = 6)
        
        self.seehands = tk.Button(self)
        self.seehands["text"] = "See all hands"
        self.seehands["command"] = self.show_all_hands
        self.seehands.grid(row = 0, column = 1)
        
        self.hidehands = tk.Button(self)
        self.hidehands["text"] = "Hide other hands"
        self.hidehands["command"] = self.hide_hands
        self.hidehands.grid(row = 0, column = 2)
    
    hands_showing = False
    def show_all_hands(self):
        p2hand = ""
        for i in p2:
            p2hand += chr(card_to_picture(i))
        p3hand = ""
        for i in p3:
            p3hand += chr(card_to_picture(i))
        p4hand = ""
        for i in p4:
            p4hand += chr(card_to_picture(i))
        # Other hands
        self.hand2 = tk.Label(self, text=p2hand, font = ("Times", 120))
        self.hand3 = tk.Label(self, text=p3hand, font = ("Times", 120))
        self.hand4 = tk.Label(self, text=p4hand, font = ("Times", 120))
        self.hand2.grid(row = 5, columnspan = 6)
        self.hand3.grid(row = 6, columnspan = 6)
        self.hand4.grid(row = 7, columnspan = 6)
        self.hands_showing = True
    def hide_hands(self):
        self.hand2.destroy()
        self.hand3.destroy()
        self.hand4.destroy()
        self.hands_showing = False
        
    def play_user_move(self, random_stuff_idk):
        text = self.playbox.get()
        print(text)
        move_as_strings = list(text.split(", "))
        try:
            move = [float(i) for i in move_as_strings]
        except ValueError:
            tk.messagebox.showwarning(title = "Bad input", message = "Your move can only be floats separated by a comma and space.\nRemember: card values are 3~15, suits are 0.0, 0.25, 0.5, or 0.75.")
            return
        if move not in get_moves(p1):
            tk.messagebox.showwarning(title = "Invalid move", message = "Invalid move. \nRemember: card values are 3~15, suits are 0.0, 0.25, 0.5, or 0.75. \nPlease list in ascending order.")
        else:
            play(p1, move)
            next_turn()
            self.refresh()
            
    def reset(self):
        newgame()
        self.refresh()

    def refresh(self):
        self.hand.destroy()
        self.lp.destroy()
        self.dashboard.destroy()
        self.playlabel.destroy()
        self.playbox.destroy()
        if self.hands_showing:
            self.hide_hands()
            self.show_all_hands()
        self.create_widgets()

root = tk.Tk()
app = Application(master=root)
#app.mainloop()


# In[52]:


def render_game(mode='text'):
    if mode == 'human':
        app.mainloop()
    else:
        print("Last play: ", lastplay, " Rule: ", rule)
        print("=====================================p1 hand=====================================")
        print(p1)
        print("=====================================p2 hand=====================================")
        print(p2)
        print("=====================================p3 hand=====================================")
        print(p3)
        print("=====================================p4 hand=====================================")
        print(p4)
def derender_game():
    app.master.destroy()


# In[55]:


#newgame()
#render_game()


# In[58]:


""""
import sys
from contextlib import closing
from io import StringIO
from gym import utils
from gym.envs.toy_text import discrete

class KillerEnv(discrete.DiscreteEnv):
    def __init__(self):
        self.action_space = spaces.Discrete(14)
        self.observation_space = spaces.Tuple((
            spaces.Discrete(14),
            spaces.Discrete(13)))

        # Start the first game
        self.reset()

    #Types of Actions: 1-13 => play a move from tier 1-13, 0 => pass,  
    def step(self, action):
        #this is for the machine
        assert self.action_space.contains(action)
        if action == 0:
            reward = 0
        else:
            if tier_moves(p4, get_moves(p4))[action-1] == 0:
                reward = -100
            else:
                myMove = tier_to_move(action-1)
                play(p4, myMove)
                reward = len(myMove)
        if len(p1) == 0 or len(p2) == 0 or len(p3) == 0 or len(p4) == 0:
            done = True
        else:
            done = False
            
        #this is for user input
        open_app()
        
        return self._get_obs(), reward, done, {}

    def _get_obs(self):
        return (len(p1), tier_moves(p4, get_moves(p4)))

    def reset(self):
        deal_hands()
        global rule
        rule = 0
        global topcard
        topcard = 2.0
        global turn
        if 3.0 in p1:
            turn = 1
        elif 3.0 in p2:
            turn = 2
        elif 3.0 in p3:
            turn = 3
        else:
            turn = 4
"""
print("Killer Functions Imported")


# In[ ]:




