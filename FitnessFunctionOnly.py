#!/usr/bin/env python
# coding: utf-8

# In[1]:


from DataProvider import *
import pandas as pd
import numpy as np
import json
from pandas.io.json import json_normalize


# In[2]:


with open('./data/cards-all.json', encoding="utf8") as f:
   cards_data = json.load(f)


# In[3]:


cards = json_normalize(cards_data)
cards


# Card Stats

# In[4]:


with open('./data/card-stats.json', encoding="utf8") as f:
   card_stats = json.load(f)


# In[5]:


card_statistics = json_normalize(card_stats['series']['data']['ALL'])
card_statistics.head()


# In[6]:


card_types = list(card_statistics.columns.values)


# In[7]:


card_frame=card_statistics
card_frame[card_frame['dbf_id']==178]


# In[8]:


individual_card_stats =card_frame
individual_card_stats.head()


# Deck Stats

# In[9]:


with open('./data/deck-stats.json', encoding="utf8") as f:
   deck_stats = json.load(f)


# In[10]:


deck_statistics = json_normalize(deck_stats['series']['data'])
#deck_types = list(deck_statistics.columns.values)
deck_statistics.head()


# In[11]:


import glob

deck_types = list(deck_statistics.columns.values)
li = []

for deck_type in deck_types:
    df = json_normalize(deck_stats['series']['data'][deck_type])
    li.append(df)
    df['deck']=deck_type

frame = pd.concat(li, axis=0, ignore_index=True)


# In[12]:


from ast import literal_eval
druid_deck_statistics = frame
druid_deck_statistics['deck_list'] = druid_deck_statistics['deck_list'].apply(literal_eval)
druid_deck_statistics['deck_list'] = pd.Series(druid_deck_statistics['deck_list'])
druid_deck_statistics['unique_cards']=druid_deck_statistics.apply(lambda x: len(x['deck_list']), axis=1)
druid_deck_statistics


# In[13]:


#len(druid_deck_statistics['deck_list'][1])
#druid_deck_statistics
druid_deck_statistics['unique_cards'].unique()


# In[14]:


deck_details = druid_deck_statistics[['deck_id','deck','win_rate','unique_cards']]
deck_details.head()


# In[15]:


deck_list = druid_deck_statistics[['deck_id','deck_list']]
deck_list.head()


# In[16]:


card_breakdown=deck_list.join(pd.DataFrame(deck_list['deck_list'].values.tolist()))
card_breakdown


# In[17]:


deck = card_breakdown.add_prefix('card_')
deck.rename(columns={'card_deck_id':'deck_id','card_deck_list':'deck_list',}, inplace=True)
deck


# In[18]:


melted = pd.melt(deck, id_vars =['deck_id','deck_list'], value_vars =['card_0', 'card_1', 'card_2', 'card_3', 'card_4', 'card_5', 'card_6', 'card_7', 'card_8', 'card_9', 'card_10', 'card_11', 'card_12', 'card_13', 'card_14', 'card_15', 'card_16', 'card_17', 'card_18', 'card_19', 'card_20', 'card_21']) 
alldata = melted.dropna(subset=['value'])
alldata.head()


# In[19]:


alldata['card_id']=alldata.apply(lambda x: x['value'][0], axis=1)
alldata['quantity']=alldata.apply(lambda x: x['value'][1], axis=1)
alldata


# In[20]:


#list(deck.columns.values)
deck_data = alldata[['deck_id','card_id','quantity']]
deck_data.head()


# In[21]:


#deck_data.groupby("deck_id").sum()


# In[22]:


list(cards.columns.values)
selected_cards= cards[['dbfId','cost','armor', 'attack', 'cardClass', 'health', 'mechanics', 'name', 'overload', 'race', 'rarity', 'type']]
selected_cards['dbfId']=selected_cards['dbfId'].fillna(0)
selected_cards['dbfId']=selected_cards['dbfId'].astype('int64')
#selected_cards['armor']=selected_cards['armor'].fillna(0)
#selected_cards['attack']=selected_cards['attack'].fillna(0)
#selected_cards['health']=selected_cards['health'].fillna(0)
selected_cards


# In[23]:


individual_card_merged = selected_cards.merge(individual_card_stats, left_on='dbfId', right_on='dbf_id')
individual_card_merged.head()


# In[24]:


def calculateRatio(cardType,attack,health,cost):
    try:
        minion=['MINION']
        if any(Ctype in cardType for Ctype in minion):
            summed = attack+health+cost
            if summed>0:
                attackHealth = attack + health
                ratio = attackHealth/cost
                return ratio
            else:
                return 0
        else:
            return 0
    except:
        return 0


# In[87]:


individual_card_merged['Ratio'] = individual_card_merged.apply(lambda x: calculateRatio(x['type'],x['attack'],x['health'],x['cost']), axis=1)
individual_card_merged['Ratio'] = individual_card_merged['Ratio'].astype(float).round(2)
individual_card_merged.head()


# In[26]:


selected_cards['Ratio'].unique()


# In[27]:


selected_cards['armor'].unique()


# In[28]:


deck_data.head()


# In[29]:


deck_card_named = deck_data.merge(selected_cards, left_on='card_id', right_on='dbfId')
deck_card_named


# In[33]:


sample_deck['cost'].skew()


# In[34]:


deck_types = pd.pivot_table(deck_card_named, values=['dbfId'], index=['deck_id'],columns=['type'], aggfunc=lambda x: len(x.unique()))
deck_types.head()


# In[35]:


deck_cardClass = pd.pivot_table(deck_card_named, values=['dbfId'], index=['deck_id'],columns=['cardClass'], aggfunc=lambda x: len(x.unique()))
deck_cardClass.head()


# In[36]:


deck_rarity = pd.pivot_table(deck_card_named, values=['dbfId'], index=['deck_id'],columns=['rarity'], aggfunc=lambda x: len(x.unique()))
deck_rarity.head()


# In[37]:


deck_numerical = pd.pivot_table(deck_card_named, values=['armor','attack','health'], index=['deck_id'], aggfunc=[min, max, np.mean])
deck_numerical.head()


# In[38]:


druid_deck_statistics


# In[39]:


from functools import reduce
data_frames = [deck_types, deck_cardClass, deck_rarity,deck_numerical]
df_merged = reduce(lambda  left,right: pd.merge(left,right, left_index=True, right_index=True,how='outer'), data_frames)
df_merged.head()


# In[40]:


from functools import reduce
deck_rarity.columns = deck_rarity.columns.droplevel()
data_frames = [deck_rarity,deck_details]
deck_details=deck_details.set_index("deck_id")


# In[41]:


deck_rarity.head()


# In[42]:


df_deck_rarity = deck_details.merge(deck_rarity, left_on='deck_id', right_on='deck_id')
df_deck_rarity.head()


# In[46]:


df_deck_rarity['high_win']=df_deck_rarity.apply(lambda x: (x['win_rate']>50.0), axis=1)
df_deck_rarity['high_win']=df_deck_rarity['high_win'].astype(int)
df_deck_rarity.head()


# # E: Fitness Function Generation

# In[47]:


def fitnessFunctionDeck(deck_id):

    #overall fitness function:
    fitnessValue = 0
    try:
        deck = deck_data[deck_data["deck_id"]==deck_id]
        
        #MINIMIZE: Number of times there are duplicated cards
        #identify the number of duplicate cards
        duplicatedCards = deck[deck['quantity']!=1]
        numberDuplicatedCards = len(duplicatedCards.index)
        #MAXIMIZE: Win Rate of the Deck
        #identify the number of duplicate cards
        
        sample_deck_named_cards = deck.merge(individual_card_stats, left_on='card_id', right_on='dbf_id')
        cardWinRates=sample_deck_named_cards["winrate"].mean()
    
        #MINIMIZE: Standard Deviation of 
        #identify the number of duplicate cards
        cardStandardDeviation=sample_deck_named_cards["winrate"].std()
        
        fitnessValue = 0.5*cardWinRates + 0.5*cardStandardDeviation - numberDuplicatedCards
        return [fitnessValue,cardWinRates,cardStandardDeviation,numberDuplicatedCards]
    except:
        return 'error'


# In[115]:


#this function convert the deck to feature array 
def convertToFeaturesArray(card_array):

    d = {'cardWinRates' : 'Unknown','numberDuplicatedCards' : 'Unknown','deckSkew' : 'Unknown','minionRatio' : 'Unknown'}
    
    #overall fitness function:
    fitnessValue = 0
    try:
        #MINIMIZE: Number of Duplicated Cards
        extract_deck = pd.DataFrame(card_array)
        deck_quantity =extract_deck.groupby(0).size()
        deck=deck_quantity.to_frame()
        deck=deck.rename(columns={deck.columns[0]: 'quantity'})
        deck = deck.reset_index()
        
        
        duplicatedCards = deck[deck['quantity']!=1]
        numberDuplicatedCards = len(duplicatedCards.index)
        deck=deck.rename(columns={deck.columns[0]: 'card_id'})
        #return deck
    
        sample_deck_named_cards = deck.merge(individual_card_merged, how='left',left_on='card_id', right_on='dbfId')
        
        #return sample_deck_named_cards
        
        #MAXIMIZE: Win Rate of the Deck
        cardWinRates=sample_deck_named_cards["winrate"].mean()
        
        #Optimize towards Positive Skewness 
        deckSkew = sample_deck_named_cards['cost'].skew()
        
        
        #Minion Cards
        minionsOnly = sample_deck_named_cards[sample_deck_named_cards["type"]=="MINION"]   
        ratioSum = minionsOnly["Ratio"].sum(axis = 0, skipna = True)        
        
        numberOfMinionCards = len(minionsOnly)
        minionRatio = ratioSum/numberOfMinionCards
                
        d['cardWinRates'] = round(cardWinRates,2)
        d['numberDuplicatedCards'] = round(numberDuplicatedCards,2)
        d['deckSkew'] = round(deckSkew,2)
        d['minionRatio'] = round(minionRatio,2)
        
        return d
        
    except:
        return 'error'


# In[112]:


#deck is a list of dfid. this function return the predicted winrate of the deck
def predict(card_array):

    d = {'winRate' : 'Unknown','cardWinRates' : 'Unknown','numberDuplicatedCards' : 'Unknown','deckSkew' : 'Unknown','minionRatio' : 'Unknown'}
    
    #overall fitness function:
    fitnessValue = 0
    try:
        #MINIMIZE: Number of Duplicated Cards
        extract_deck = pd.DataFrame(card_array)
        deck_quantity =extract_deck.groupby(0).size()
        deck=deck_quantity.to_frame()
        deck=deck.rename(columns={deck.columns[0]: 'quantity'})
        deck = deck.reset_index()
        
        
        duplicatedCards = deck[deck['quantity']!=1]
        numberDuplicatedCards = len(duplicatedCards.index)
        deck=deck.rename(columns={deck.columns[0]: 'card_id'})
        #return deck
    
        sample_deck_named_cards = deck.merge(individual_card_merged, how='left',left_on='card_id', right_on='dbfId')
        
        #return sample_deck_named_cards
        
        #MAXIMIZE: Win Rate of the Deck
        cardWinRates=sample_deck_named_cards["winrate"].mean()
        
        #Optimize towards Positive Skewness 
        deckSkew = sample_deck_named_cards['cost'].skew()
        
        
        #Minion Cards
        minionsOnly = sample_deck_named_cards[sample_deck_named_cards["type"]=="MINION"]   
        ratioSum = minionsOnly["Ratio"].sum(axis = 0, skipna = True)        
        
        numberOfMinionCards = len(minionsOnly)
        minionRatio = ratioSum/numberOfMinionCards
        

        
        fitnessValue = cardWinRates + numberDuplicatedCards+deckSkew+minionRatio
        
        d['winRate'] = round(fitnessValue,2)
        d['cardWinRates'] = round(cardWinRates,2)
        d['numberDuplicatedCards'] = round(numberDuplicatedCards,2)
        d['deckSkew'] = round(deckSkew,2)
        d['minionRatio'] = round(minionRatio,2)
        
        return d['winRate']
        
    except:
        return 'error'


# In[89]:


sample_deck = deck_data[deck_data["deck_id"]=="7ORxXwcYQ4LSPwITq0Q60f"]
sample_deck.head()


# In[90]:


#individual_card_stats


# In[91]:


selected_cards


# In[92]:


selected_cards


# In[93]:


fitnessFunctionDeck("7ORxXwcYQ4LSPwITq0Q60f")


# # F: Random Deck Generator

# In[94]:


import random
card_deck_1=np.random.choice(individual_card_stats["dbf_id"].tolist(), 30, replace=True)


# In[116]:


convertToFeaturesArray(card_deck_1)


# In[113]:


predict(card_deck_1)


# In[ ]:




