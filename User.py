from os import system
from Cards import all_cards, value
from random import choice, sample, randint
from table import show_table


class User:

    total = 0#total points of bot in a round
    b_bid = 0#bids of bot in a round
    card = None #cards of bot
    
    def __init__(self):
        
        self.all_cards = [i for i in all_cards]
        
        self.points = [] #point tracer
        
        self.card_distribution()

    def card_distribution(self):
        '''
        Cards are randomly disturbuted to user and bot
        user: dict 
        bot: list
        '''
        self.user = {
            key:value for key,value in zip(range(1,14),sample(self.all_cards,k = 13))
        } # selecting random cards
        for i in self.user.values(): self.all_cards.pop(self.all_cards.index(i)) # removing used items from main list

        self.p1 = [i for i in sample(self.all_cards,k = 13)]
        for i in self.p1: self.all_cards.pop(self.all_cards.index(i))
        
        User.card = ' '.join(self.p1) # to keep the track of selected cards of bot so as to display to for later!

    def bid(self):
        # Bid of user and bot is stored here
        # For now the bid for bot is selected randomly between 1 - 3. 
        while True:
            try: int(input('Call a bid: '))

            except ValueError: print('Invalid option')

            else: break
        
        self.bid_of_bot = float(randint(1,3))
        User.b_bid = self.bid_of_bot

    def card_throw(self):
        '''
        The card is thrown randomly by bot (using choice function for now).
        The used card is removed from the main list of bot's card.
        '''
        self.bot = choice(self.p1)
        self.p1.pop(self.p1.index(self.bot))

        return f'bot: {self.bot}\n'

    def display_user_cards(self):
        '''
        Option of card for user == color of card thrown by bot
        If no such colored card then show all sphade cards
        If no sphade card then show all other left over cards 
        '''
        try:
            self.to_be_displayed = [i for i in self.user.values() if i[1] == self.bot[1]]
            
            if len(self.to_be_displayed) == 0: 
                self.to_be_displayed = [i for i in self.user.values() if i[1] == 'S']
                if len(self.to_be_displayed) == 0:
                    self.to_be_displayed = self.user.values()

            for i in self.user.keys():
                if self.user[i] in self.to_be_displayed:
                    print(f'{i}: {self.user[i]}',end='   ')

        except AttributeError:
            "Displayes the total cards given to user in the begnning!"
            print('Your cards: ')
            for key,value in zip(self.user.keys(),self.user.values()):
                print(f'{key}: {value}',end='   ')
        print('\n')
    
    def take_input(self):
        while True:
            # asks for input
            try: 
                card_index = int(input("Select your card: "))
                self.user[card_index]
            #if any input other than integer or key is 0. Show the 'invalid option' message!
            except Exception: print('Invalid option')
            
            else: # if card not in option again show the 'invalid option' message!
                if self.user[card_index] not in self.to_be_displayed:
                    print('Invalid option')

                else: break # else take the valid option and break the loop

        self.track(card_index) # run track method
        self.user.pop(card_index) # remove the used card of user from main cards.
        
    def track(self,index:int):
        '''
        if value of card thrown by user > value of card thrown by bot: append u in self.points

        elif value of card thrown by bot > value of card thrown by user: append b in self.points
        
        else: pass
        '''
        if value[self.user[index]] > value[self.bot]: self.points.append('u')
        
        elif value[self.user[index]] < value[self.bot]: self.points.append('b')
        
        else: pass
    
    def result(self):
        '''
        if bid of bot == total number of b in self.points: append bid of bot in total

        elif bid of bot > total number of b in self.points: append - (bid of bot) in total

        elif bid of bot < total number of b in self.points: 
            if bid of bot == total number of b in self.points + 1: append (bid of bot) + 0.1 in total
        '''
        if self.bid_of_bot == self.points.count('b'):
            User.total += self.bid_of_bot 
        
        elif self.bid_of_bot < self.points.count('b'):
            User.total += self.bid_of_bot + ( ( self.points.count('b') - self.bid_of_bot) / 10 )
        
        elif self.bid_of_bot > self.points.count('b'):
            User.total -= self.bid_of_bot

for i in range(int(input('Select rounds: '))):
    print()
    user = User()
    user.display_user_cards()
    user.bid()
    system('CLS')
    for j in range(13):
        print(user.card_throw())
        user.display_user_cards()
        user.take_input()
        print('----------------------------------------\n')
    user.result()
    show_table(user.bid_of_bot, user.total, user.card)
    print(f'\n-------------------------------- end of round: {i+1} -------------------------------------------\n')
