import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import random

# constant variables to handle regularly used values
FONT = ('Times', 14, 'bold')
Y_FONT = ('Times', 50, 'bold italic')
SECTION_FONT = ('Times', 16, 'bold')

PHOTO_WIDTH = 85
PHOTO_HEIGHT = 85

WINDOW_WIDTH = '850'
WINDOW_HEIGHT = '950'

SF_COLOR = 'beige'
P1_COLOR = 'red'
P2_COLOR = 'blue'
BTM_COLOR = 'green'

class Yahtzee(tk.Frame):
    def __init__(self, window):
        tk.Frame.__init__(self, window)
        self.window = window

        # window name and size
        window.title('Yahtzee')
        window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+300+0')

        self.reset()

        # load the dice images and set up the game board
        self.load_images()
        self.load_lock_photos()
        self.game_board()
        self.player_label.configure(text='Player 1')
        self.roll_button.configure(state=tk.DISABLED)
        self.score_button.configure(state=tk.DISABLED)

    def reset(self):
        #initialize game variables

        self.roll_outcome = [0, 0, 0, 0, 0]
        self.dice_focus = [1, 1, 1, 1, 1]
        self.scoring_btns_focus_p1 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
        self.scoring_btns_focus_p2 = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

        self.p1_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.p2_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.up_bonus_p1 = 0
        self.yahtzee_bonus_p1 = 0
        self.up_bonus_p2 = 0
        self.yahtzee_bonus_p2 = 0

        self.turn_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.up_score_p1 = 0
        self.lo_score_p1 = 0
        self.tot_score_p1 = 0

        self.up_score_p2 = 0
        self.lo_score_p2 = 0
        self.tot_score_p2 = 0

        self.roll_number = 0

        self.player_one = True
        self.player_two = False

    def load_lock_photos(self):
        self.lock_photo_list = ['dice_one_lock.png', 'dice_two_lock.png', 'dice_three_lock.png',
                                'dice_four_lock.png', 'dice_five_lock.png', 'dice_six_lock.png', ]
        self.lock_photos = []

        for photo in self.lock_photo_list:
            PHOTO = Image.open(photo)
            img_copy = PHOTO.copy()
            PHOTO = img_copy.resize((PHOTO_WIDTH, PHOTO_HEIGHT))
            img = ImageTk.PhotoImage(PHOTO)
            self.lock_photos.append(img)

    def load_images(self):
        # dice png's and values associated with them
        self.photo_list = [('dice_one.png', 1), ('dice_two.png', 2), ('dice_three.png', 3),
                           ('dice_four.png', 4), ('dice_five.png', 5), ('dice_six.png', 6)]

        # list to hold tkinter dice images and values associated with them
        self.photos = []

        # create the tkinter images and fill the list with the image and its point value
        for photo in self.photo_list:
            PHOTO = Image.open(photo[0])
            img_copy = PHOTO.copy()
            PHOTO = img_copy.resize((PHOTO_WIDTH, PHOTO_HEIGHT))
            img = ImageTk.PhotoImage(PHOTO)
            self.photos.append([img, photo[1]])

    def isHiLo(self, a_list):
        '''
        determine whether a straight exists and if hi or low
        :param a_list: list containing the dice values
        :return: whether the straight is low, both(hi and low) or neither
        '''

        new_list = list(set(a_list))        # get unique die and put into copy of the list
        in_order = 1
        orders_seen = []
        last_d = None

        for d in new_list:
            if last_d:
                if last_d == (d - 1):
                    in_order += 1
                else:
                    orders_seen.append(in_order)
                    in_order = 1
            last_d = d

        orders_seen.append(in_order)
        max_order = max(orders_seen)

        # determine if we have a large straight or small straight
        if max_order == 5:
            return 'both'
        elif max_order == 4:
            return 'low'
        else:
            return 'neither'

    def isFullHouse(self):
        '''
        determine if a roll is full house
        :return: True if there is, else false
        '''

        recurring = {}

        # populate the dictionary with the number of occurances of die values for a given roll
        for d in self.roll_outcome:
            if d in recurring.keys():
                recurring[d] += 1
            else:
                recurring[d] = 1

        two_of_a_kind_seen = False
        three_of_a_kind_seen = False

        # look thru the dict for full house combo's
        for d, occurrences in recurring.items():
            if occurrences == 2:
                two_of_a_kind_seen = True
            elif occurrences == 3:
                three_of_a_kind_seen = True

        if two_of_a_kind_seen and three_of_a_kind_seen:
            return True
        else:
            return False

    def turn_score(self):
        '''
        1. for each roll update the up_lev list
        2. reset to all 0's after each roll
        '''

        # upper section scoring
        self.ones = self.roll_outcome.count(1)      # ones
        self.turn_scores[0] = self.ones * 1

        self.twos = self.roll_outcome.count(2)      # twos
        self.turn_scores[1] = self.twos * 2

        self.threes = self.roll_outcome.count(3)    # threes
        self.turn_scores[2] = self.threes * 3

        self.fours = self.roll_outcome.count(4)     # fours
        self.turn_scores[3] = self.fours * 4

        self.fives = self.roll_outcome.count(5)     # fives
        self.turn_scores[4] = self.fives * 5

        self.sixes = self.roll_outcome.count(6)     # sixes
        self.turn_scores[5] = self.sixes * 6

        # lower section scoring
        score_list = [self.ones, self.twos, self.threes, self.fours, self.fives, self.sixes]


        if self.isHiLo(self.roll_outcome) == 'low' or \
            self.isHiLo(self.roll_outcome) == 'both':         # Low Straight

            self.turn_scores[9] = 30

        if self.isHiLo(self.roll_outcome) == 'both':          # High Straight

            self.turn_scores[10] = 40

        if self.isFullHouse():                                  # Full House
            self.turn_scores[8] = 25

        self.turn_scores[12] = sum(self.roll_outcome)           # chance

        for option in score_list:
            if option >= 3:                                     # 3 of a kind
                self.turn_scores[6]=sum(self.roll_outcome)

            if option >= 4:                                     # 4 of a kind
                self.turn_scores[7]=sum(self.roll_outcome)

            if option == 5:  # Yahtzee

                self.flash(0)

                # handle if first yahtzee and subsequent yahtzees
                if (self.player_one and self.scoring_btns_focus_p1[11] == 1) or \
                        (self.player_two and self.scoring_btns_focus_p2[11] == 1):

                    self.turn_scores[11] = 50

                if (self.player_one and self.scoring_btns_focus_p1[11] == 0) or \
                        (self.player_two and self.scoring_btns_focus_p2[11] == 0):

                    self.scoring_btns_focus_p2[13] = 1
                    self.scoring_btns_focus_p1[13] = 1

                    self.turn_scores[13] = 100

                self.scoring()

    def flash(self, count):

        bg = self.yahtzee_label.cget("background")
        fg = self.yahtzee_label.cget("foreground")
        self.yahtzee_label.configure(text="Yahtzee!!!", background=fg, foreground=bg)
        count += 1
        if (count < 3):
            self.after(1000, self.flash, count)

    def start(self):
        # functioning of the "start" button

        self.roll_button.configure(state=tk.NORMAL, text='Roll')

    def next_turn(self, die_index):
        '''
        handles what happens when a score choice is made
        1. make roll button active, reset dice focus and outcome lists
        2. update upper/lower bonuses and scores (not complete)
        3. update total score for each player (not complete)
        4. change player label
        5. disable score buttons
        '''

        self.yahtzee_label.configure(text="Yahtzee", background='beige', foreground='black')
        self.roll_button.configure(state=tk.NORMAL, text='Roll')
        self.roll_label.configure(text='')

        if self.player_one:
            # don't turn yahtzee bonus button off
            #if die_index != 13:
            self.scoring_btns_focus_p1[die_index] = 0

            score = self.turn_scores[die_index]

            # add to yahtzee bonus to players yahtzee bonus score value
            if die_index == 13:
                self.p1_scores[die_index] += score
            else:
                self.p1_scores[die_index] = score

            self.p1_buttons[die_index].configure(state=tk.DISABLED, text=str(score))

            # upper bonus for player 2
            if sum(self.p1_scores[:6]) >= 62:
                self.up_bonus_p1 = 35
                self.p1_bonus_lbl.configure(text='35')

            # update player 1 upper/lower/total scores
            self.up_score_p1 = sum(self.p1_scores[:6]) + self.up_bonus_p1
            self.lo_score_p1 = sum(self.p1_scores[6:]) + self.yahtzee_bonus_p1
            self.tot_score_p1 = self.up_score_p1 + self.lo_score_p1
            self.p1_upTotal_lbl.configure(text=str(self.up_score_p1))
            self.p1_loTotal_lbl.configure(text=str(self.lo_score_p1))
            self.p1_total_label.configure(text=str(self.tot_score_p1))

            # change player turn
            self.player_label.configure(text='Player 2')
            self.player_one = False
            self.player_two = True

        elif self.player_two:

            # don't turn yahtzee bonus button off
            self.scoring_btns_focus_p2[die_index] = 0

            score = self.turn_scores[die_index]

            # add to yahtzee bonus to players yahtzee bonus score value
            if die_index == 13:
                self.p2_scores[die_index] += score
            else:
                self.p2_scores[die_index] = score

            self.p2_buttons[die_index].configure(state=tk.DISABLED, text=str(score))

            # upper bonus for player 2
            if sum(self.p2_scores[:6]) >= 62:
                self.up_bonus_p2 = 35
                self.p2_bonus_lbl.configure(text='35')

            # update player 2 upper/lower/total scores
            self.up_score_p2 = sum(self.p2_scores[:6]) + self.up_bonus_p2
            self.lo_score_p2 = sum(self.p2_scores[6:]) + self.yahtzee_bonus_p2
            self.tot_score_p2 = self.up_score_p2 + self.lo_score_p2
            self.p2_upTotal_lbl.configure(text=str(self.up_score_p2))
            self.p2_loTotal_lbl.configure(text=str(self.lo_score_p2))
            self.p2_total_label.configure(text=str(self.tot_score_p2))

            # change player turn
            self.player_label.configure(text='Player 1')
            self.player_one = True
            self.player_two = False

        # disable and clear unchosen buttons from scoring buttons for next turn
        for index in range(len(self.p1_buttons)):
            if self.scoring_btns_focus_p1[index] == 1:
                self.p1_buttons[13].configure(state=tk.DISABLED, text='')
                self.p1_buttons[index].configure(state=tk.DISABLED, text='')
            if self.scoring_btns_focus_p2[index] == 1:
                self.p2_buttons[13].configure(state=tk.DISABLED, text='')
                self.p2_buttons[index].configure(state=tk.DISABLED, text='')

        # make dice buttons active for next turn
        for button in self.dice_buttons:
            button.configure(state=tk.NORMAL)

        # reset turn lists and clear the dice
        self.dice_focus = [1, 1, 1, 1, 1]
        self.roll_outcome = [0, 0, 0, 0, 0]
        self.turn_scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.roll_number = 0
        self.die_frame()

        # handle game over
        if sum(self.scoring_btns_focus_p2) == 0 and self.tot_score_p2 > self.tot_score_p1:
            self.yahtzee_label.configure(text='Game Over\nPlayer 2 Wins!!', font=SECTION_FONT)
        elif sum(self.scoring_btns_focus_p2) == 0 and self.tot_score_p2 < self.tot_score_p1:
            self.yahtzee_label.configure(text='Game Over\nPlayer 1 Wins!!', font=SECTION_FONT)

    def scoring(self):
        '''
        1. scoring available when score button pressed
        2. "turn" buttons disabled on score button press
        3. enable "scoring" buttons for current player
        4. fill enabled buttons with possible scoring options
        5. change players turn
        '''
        self.roll_button.configure(state=tk.DISABLED, text='Choose Score')
        self.score_button.configure(state=tk.DISABLED)

        if self.player_one:
            # enable player_one scoring options and fill the buttons with possible scoring options
            for index, button in enumerate(self.p1_buttons):

                score = self.turn_scores[index]

                if self.scoring_btns_focus_p1[index] == 1:
                    self.turn_scores[index] = score
                    button.configure(state=tk.NORMAL, text=str(score)) # text= score from score list

        elif self.player_two:
            # enable player_two scoring options and fill the buttons with possible scoring options
            for index, button in enumerate(self.p2_buttons):

                score = self.turn_scores[index]

                if self.scoring_btns_focus_p2[index] == 1:
                    self.turn_scores[index] = score
                    button.configure(state=tk.NORMAL, text=str(score))  # text= score from score list

    def dice_hold(self, die):
        '''
        on dice choice
        1. make die button active/inactive
        2. get the index of the die chosen and update dice_focus list at that index
        '''

        index = self.dice_buttons.index(die)
        die_value = self.roll_outcome[index] - 1

        if self.dice_focus[index] == 0:
            img = self.photos[die_value][0]
            self.activate_die(die, img)
            self.dice_focus[index] = 1

        elif self.dice_focus[index] == 1:
            lock_img = self.lock_photos[die_value]
            self.disable_die(die, lock_img)
            self.dice_focus[index] = 0

    def roll(self):
        '''
        handles board configuration when roll button pressed
        1. activate score button and disable start button
        2. increment roll number
        3. handle configuration of widgets depending on whose rolling
            and how many rolls have been made
        5. loop thru active dice buttons and place a randomly chose dice image in the button
        6. update roll_outcome list
        7. determine possible scoring options for dice shown (held and active using turn-score function)
        '''
        self.score_button.configure(state=tk.NORMAL)
        self.start_button.configure(state=tk.DISABLED)

        for index in range(len(self.dice_buttons)):
            if self.dice_focus[index] == 1:
                img = random.choice(self.photos)        # random choice of dice image

                self.dice_buttons[index].configure(image=img[0])    # set button image kwarg to that image
                self.dice_buttons[index].image = img[0]  # save the image from Python garbage collection

                # save the value of the the specific dice in the correct position in a list
                self.roll_outcome[index] = img[1]

                # to force a yahtzee, comment out the line above and uncomment below
                #self.roll_outcome = [1, 1, 1, 1, 1]

        self.roll_number += 1

        if self.player_one:

            self.turn_score()

            if self.roll_number < 3:
                self.player_label.configure(text='Player 1', anchor=tk.W)
                roll_message = f'Roll {self.roll_number}'
                self.roll_button.configure(text=roll_message)   # update the roll number
                self.roll_label.configure(text='Roll Again or\nChoose score', anchor=tk.W)

                print(self.roll_outcome)

            elif self.roll_number == 3:
                roll_message = f'Roll {self.roll_number}'
                self.roll_button.configure(text=roll_message, state=tk.DISABLED)  # update the roll number
                self.roll_label.configure(text='Choose your score')

                print(self.roll_outcome)

        elif self.player_two:

            self.turn_score()

            if self.roll_number < 3:
                self.player_label.configure(text='Player 2')
                roll_message = f'Roll {self.roll_number}'
                self.roll_button.configure(text=roll_message)   # update the roll number
                self.roll_label.configure(text='Roll Again or\nChoose score', anchor=tk.W)

                print(self.roll_outcome)

            elif self.roll_number == 3:
                roll_message = f'Roll {self.roll_number}'
                self.roll_button.configure(text=roll_message, state=tk.DISABLED)  # update the roll number
                self.roll_label.configure(text='Choose your score')

                print(self.roll_outcome)

    def activate_die(self, die, image):
        # make a button "NORMAL" (active)
        die.configure(image=image)
        die.image = image

    def disable_die(self, die, image):
        # make a button "DISABLED" (not active)
        die.configure(image=image)
        die.image = image

    def is_disabled(self, button):
        '''
        test for the state of a button
        :param button: the button of interest
        :return True if button disabled, False otherwise
        '''

        state = str(button.cget('state'))

        if state == 'disabled':
            return True
        else:
            return False

    def die_frame(self):
        # create the frame to house the dice buttons
        die_frame = tk.Frame(self.window, bg=SF_COLOR, bd=5)
        die_frame.place(relx=0.0, rely=0.0, relwidth=.30, relheight=0.8)

        # create the dice buttons and place them in a list
        self.die_1 = ttk.Button(die_frame, text='Die 1')
        self.die_1.place(relx=0.15, rely=0.03, relwidth=.5, relheight=0.16)

        self.hold_d1 = ttk.Button(die_frame, text='Hold',
                                command=lambda:self.dice_hold(self.die_1))
        self.hold_d1.place(relx=0.7, rely=0.08, relwidth=.3, relheight=0.05)

        self.die_2 = ttk.Button(die_frame, text='Die 2')
        self.die_2.place(relx=0.15, rely=0.20, relwidth=.5, relheight=0.16)

        self.hold_d2 = ttk.Button(die_frame, text='Hold',
                                command=lambda:self.dice_hold(self.die_2))
        self.hold_d2.place(relx=0.7, rely=0.25, relwidth=.3, relheight=0.05)

        self.die_3 = ttk.Button(die_frame, text='Die 3')
        self.die_3.place(relx=0.15, rely=0.37, relwidth=.5, relheight=0.16)

        self.hold_d3 = ttk.Button(die_frame, text='Hold',
                                command=lambda:self.dice_hold(self.die_3))
        self.hold_d3.place(relx=0.7, rely=0.42, relwidth=.3, relheight=0.05)

        self.die_4 = ttk.Button(die_frame, text='Die 4')
        self.die_4.place(relx=0.15, rely=0.54, relwidth=.5, relheight=0.16)

        self.hold_d4 = ttk.Button(die_frame, text='Hold',
                                command=lambda:self.dice_hold(self.die_4))
        self.hold_d4.place(relx=0.7, rely=0.59, relwidth=.3, relheight=0.05)

        self.die_5 = ttk.Button(die_frame, text='Die 5')
        self.die_5.place(relx=0.15, rely=0.71, relwidth=.5, relheight=0.16)

        self.hold_d5 = ttk.Button(die_frame, text='Hold',
                                command=lambda:self.dice_hold(self.die_5))
        self.hold_d5.place(relx=0.7, rely=0.76, relwidth=.3, relheight=0.05)

        self.dice_buttons = [self.die_1, self.die_2, self.die_3,
                             self.die_4, self.die_5]

        self.hold_buttons = [self.hold_d1, self.hold_d2, self.hold_d3,
                             self.hold_d4, self.hold_d5]

    def scoring_frame(self):
        # create the frame to house the scoring options
        score_frame = tk.Frame(self.window, bd=5, bg=SF_COLOR)
        score_frame.place(relx=0.30, rely=0.0, relwidth=.3, relheight=0.8)

        # labels to display the upper/lower sections and their scoring options
        us_label = tk.Label(score_frame, text='Upper Section', font=SECTION_FONT, bg=SF_COLOR)
        us_label.place(relx=0.0, rely=0.0, relwidth=0.7, relheight=0.04)

        aces_label = tk.Label(score_frame, text='Add only Aces', font=FONT, bg=SF_COLOR)
        aces_label.place(relx=0.42, rely=0.05, relwidth=0.58, relheight=0.04)

        twos_label = tk.Label(score_frame, text='Add only Twos', font=FONT, bg=SF_COLOR)
        twos_label.place(relx=0.42, rely=0.1, relwidth=0.58, relheight=0.04)

        threes_label = tk.Label(score_frame, text='Add only Threes', font=FONT, bg=SF_COLOR)
        threes_label.place(relx=0.38, rely=0.15, relwidth=0.64, relheight=0.04)

        fours_label = tk.Label(score_frame, text='Add only Fours', font=FONT, bg=SF_COLOR)
        fours_label.place(relx=0.41, rely=0.2, relwidth=0.59, relheight=0.04)

        fives_label = tk.Label(score_frame, text='Add only Fives', font=FONT, bg=SF_COLOR)
        fives_label.place(relx=0.42, rely=0.25, relwidth=0.58, relheight=0.04)

        sixes_label = tk.Label(score_frame, text='Add only Sixes', font=FONT, bg=SF_COLOR)
        sixes_label.place(relx=0.42, rely=0.3, relwidth=0.58, relheight=0.04)

        total_msg = '                           Total'
        total_label = tk.Label(score_frame, text='Total', font=FONT, bg=SF_COLOR)
        total_label.place(relx=0.05, rely=0.35, relwidth=.95, relheight=0.04)

        bonus_msg = '     62 + scores a 35 Bonus'
        bonus_label = tk.Label(score_frame, text=bonus_msg, font=FONT, bg=SF_COLOR)
        bonus_label.place(relx=0.05, rely=0.35, relwidth=.95, relheight=0.04)

        totalUS_msg = '     Total of Upper Section'
        totalUS_label = tk.Label(score_frame, text=totalUS_msg, font=FONT, bg=SF_COLOR)
        totalUS_label.place(relx=0.05, rely=0.4, relwidth=.95, relheight=0.04)

        ls_label = tk.Label(score_frame, text='Lower Section',font=SECTION_FONT, bg=SF_COLOR)
        ls_label.place(relx=0.0, rely=0.5, relwidth=0.7, relheight=0.05)

        threeOfKind_msg1 = '3 of a kind:'
        threeOfKind_label1 = tk.Label(score_frame, text=threeOfKind_msg1, font=FONT, bg=SF_COLOR)
        threeOfKind_label1.place(relx=0.02, rely=0.55, relwidth=.4, relheight=0.04)

        threeOfKind_msg2 = 'Total of all dice'
        threeOfKind_label2 = tk.Label(score_frame, text=threeOfKind_msg2, font=FONT, bg=SF_COLOR)
        threeOfKind_label2.place(relx=0.4, rely=0.55, relwidth=.59, relheight=0.04)

        fourOfKind_msg = '4 of a kind:'
        fourOfKind_label = tk.Label(score_frame, text=fourOfKind_msg, font=FONT, bg=SF_COLOR)
        fourOfKind_label.place(relx=0.02, rely=0.6, relwidth=.4, relheight=0.04)

        fourOfKind_msg = 'Total of all dice'
        fourOfKind_label = tk.Label(score_frame, text=fourOfKind_msg, font=FONT, bg=SF_COLOR)
        fourOfKind_label.place(relx=0.4, rely=0.6, relwidth=.59, relheight=0.04)

        fullHouse_msg = 'Full House                    25'
        fullHouse_label = tk.Label(score_frame, text=fullHouse_msg,
                                   font=FONT, bg=SF_COLOR, justify=tk.RIGHT)
        fullHouse_label.place(relx=0.05, rely=0.65, relwidth=.95, relheight=0.04)

        lowStrt_msg = 'Low Straight                 30'
        lowStrt_label = tk.Label(score_frame, text=lowStrt_msg, font=FONT, bg=SF_COLOR)
        lowStrt_label.place(relx=0.05, rely=0.7, relwidth=.95, relheight=0.04)

        highStrt_msg = 'High Straight               40'
        highStrt_label = tk.Label(score_frame, text=highStrt_msg, font=FONT, bg=SF_COLOR)
        highStrt_label.place(relx=0.05, rely=0.75, relwidth=.95, relheight=0.04)

        highStrt_msg = 'Yahtzee                         50'
        highStrt_label = tk.Label(score_frame, text=highStrt_msg, font=FONT, bg=SF_COLOR)
        highStrt_label.place(relx=0.05, rely=0.8, relwidth=.95, relheight=0.04)

        highStrt_msg = 'Chance:  Total of all dice'
        highStrt_label = tk.Label(score_frame, text=highStrt_msg, font=FONT, bg=SF_COLOR)
        highStrt_label.place(relx=0.05, rely=0.85, relwidth=.95, relheight=0.04)

        highStrt_msg = 'Yahtzee Bonus           100'
        highStrt_label = tk.Label(score_frame, text=highStrt_msg, font=FONT, bg=SF_COLOR)
        highStrt_label.place(relx=0.05, rely=0.9, relwidth=.95, relheight=0.04)

        highStrt_msg = '    Total of Lower Section'
        highStrt_label = tk.Label(score_frame, text=highStrt_msg, font=FONT, bg=SF_COLOR)
        highStrt_label.place(relx=0.05, rely=0.95, relwidth=.95, relheight=0.04)

    def playOne_frame(self):
        # create a frame to house player ones scores
        p1_frame = tk.Frame(self.window, bg=P1_COLOR)
        p1_frame.place(relx=0.60, rely=0.0, relwidth=.2, relheight=0.8)

        # player label and buttons to choose their preferred score for a turn
        self.p1_lbl = tk.Label(p1_frame, text='Player 1', font=SECTION_FONT, bg=P1_COLOR)
        self.p1_lbl.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.04)

        self.p1_aces_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(0))
        self.p1_aces_butn.place(relx=0.3, rely=0.05, relwidth=.3, relheight=0.04)

        self.p1_twos_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(1))
        self.p1_twos_butn.place(relx=0.3, rely=0.1, relwidth=0.3, relheight=0.04)

        self.p1_threes_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(2))
        self.p1_threes_butn.place(relx=0.3, rely=0.15, relwidth=0.3, relheight=0.04)

        self.p1_fours_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(3))
        self.p1_fours_butn.place(relx=0.3, rely=0.2, relwidth=0.3, relheight=0.04)

        self.p1_fives_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(4))
        self.p1_fives_butn.place(relx=0.3, rely=0.25, relwidth=0.3, relheight=0.04)

        self.p1_sixes_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(5))
        self.p1_sixes_butn.place(relx=0.3, rely=0.3, relwidth=0.3, relheight=0.04)

        self.p1_bonus_lbl = tk.Label(p1_frame, text='0')
        self.p1_bonus_lbl.place(relx=0.3, rely=0.35, relwidth=0.3, relheight=0.04)

        self.p1_upTotal_lbl = tk.Label(p1_frame, text='0')
        self.p1_upTotal_lbl.place(relx=0.3, rely=0.4, relwidth=0.3, relheight=0.04)

        self.p1_3ofaKind_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(6))
        self.p1_3ofaKind_butn.place(relx=0.3, rely=0.55, relwidth=0.3, relheight=0.04)

        self.p1_4ofaKind_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(7))
        self.p1_4ofaKind_butn.place(relx=0.3, rely=0.6, relwidth=0.3, relheight=0.04)

        self.p1_fullHouse_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(8))
        self.p1_fullHouse_butn.place(relx=0.3, rely=0.65, relwidth=0.3, relheight=0.04)

        self.p1_lowStrt_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(9))
        self.p1_lowStrt_butn.place(relx=0.3, rely=0.7, relwidth=0.3, relheight=0.04)

        self.p1_highStrt_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(10))
        self.p1_highStrt_butn.place(relx=0.3, rely=0.75, relwidth=0.3, relheight=0.04)

        self.p1_yahtzee_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(11))
        self.p1_yahtzee_butn.place(relx=0.3, rely=0.8, relwidth=0.3, relheight=0.04)

        self.p1_chance_butn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(12))
        self.p1_chance_butn.place(relx=0.3, rely=0.85, relwidth=0.3, relheight=0.04)

        self.p1_yzBonus_btn = tk.Button(p1_frame, state=tk.DISABLED, command=lambda: self.next_turn(13))
        self.p1_yzBonus_btn.place(relx=0.3, rely=0.9, relwidth=0.3, relheight=0.04)

        self.p1_loTotal_lbl = tk.Label(p1_frame, text='0')
        self.p1_loTotal_lbl.place(relx=0.3, rely=0.95, relwidth=0.3, relheight=0.04)

        self.p1_buttons = [self.p1_aces_butn, self.p1_twos_butn, self.p1_threes_butn,
                           self.p1_fours_butn, self.p1_fives_butn, self.p1_sixes_butn,
                           self.p1_3ofaKind_butn, self.p1_4ofaKind_butn, self.p1_fullHouse_butn,
                           self.p1_lowStrt_butn, self.p1_highStrt_butn, self.p1_yahtzee_butn,
                           self.p1_chance_butn, self.p1_yzBonus_btn]

    def playTwo_frame(self):
        # create a frame to house player two's scores
        p2_frame = tk.Frame(self.window, bg=P2_COLOR)
        p2_frame.place(relx=0.8, rely=0.0, relwidth=.2, relheight=0.8)

        self.p2_buttons = []

        # player label and buttons to choose their preferred score for a turn
        self.p2_lbl = tk.Label(p2_frame, text='Player 2', font=SECTION_FONT, bg=P2_COLOR)
        self.p2_lbl.place(relx=0.0, rely=0.0, relwidth=1, relheight=0.04)

        self.p2_aces_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(0))
        self.p2_aces_butn.place(relx=0.3, rely=0.05, relwidth=.3, relheight=0.04)

        self.p2_twos_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(1))
        self.p2_twos_butn.place(relx=0.3, rely=0.1, relwidth=0.3, relheight=0.04)

        self.p2_threes_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(2))
        self.p2_threes_butn.place(relx=0.3, rely=0.15, relwidth=0.3, relheight=0.04)

        self.p2_fours_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(3))
        self.p2_fours_butn.place(relx=0.3, rely=0.2, relwidth=0.3, relheight=0.04)

        self.p2_fives_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(4))
        self.p2_fives_butn.place(relx=0.3, rely=0.25, relwidth=0.3, relheight=0.04)

        self.p2_sixes_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(5))
        self.p2_sixes_butn.place(relx=0.3, rely=0.3, relwidth=0.3, relheight=0.04)

        self.p2_bonus_lbl = tk.Label(p2_frame, text='0')
        self.p2_bonus_lbl.place(relx=0.3, rely=0.35, relwidth=0.3, relheight=0.04)

        self.p2_upTotal_lbl = tk.Label(p2_frame, text='0')
        self.p2_upTotal_lbl.place(relx=0.3, rely=0.4, relwidth=0.3, relheight=0.04)

        self.p2_3ofaKind_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(6))
        self.p2_3ofaKind_butn.place(relx=0.3, rely=0.55, relwidth=0.3, relheight=0.04)

        self.p2_4ofaKind_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(7))
        self.p2_4ofaKind_butn.place(relx=0.3, rely=0.6, relwidth=0.3, relheight=0.04)

        self.p2_fullHouse_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(8))
        self.p2_fullHouse_butn.place(relx=0.3, rely=0.65, relwidth=0.3, relheight=0.04)

        self.p2_lowStrt_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(9))
        self.p2_lowStrt_butn.place(relx=0.3, rely=0.7, relwidth=0.3, relheight=0.04)

        self.p2_highStrt_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(10))
        self.p2_highStrt_butn.place(relx=0.3, rely=0.75, relwidth=0.3, relheight=0.04)

        self.p2_yahtzee_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(11))
        self.p2_yahtzee_butn.place(relx=0.3, rely=0.8, relwidth=0.3, relheight=0.04)

        self.p2_chance_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(12))
        self.p2_chance_butn.place(relx=0.3, rely=0.85, relwidth=0.3, relheight=0.04)

        self.p2_yzBonus_butn = tk.Button(p2_frame, state=tk.DISABLED, command=lambda: self.next_turn(13))
        self.p2_yzBonus_butn.place(relx=0.3, rely=0.9, relwidth=0.3, relheight=0.04)

        self.p2_loTotal_lbl = tk.Label(p2_frame, text='0')
        self.p2_loTotal_lbl.place(relx=0.3, rely=0.95, relwidth=0.3, relheight=0.04)

        self.p2_buttons = [self.p2_aces_butn, self.p2_twos_butn, self.p2_threes_butn,
                           self.p2_fours_butn, self.p2_fives_butn, self.p2_sixes_butn,
                           self.p2_3ofaKind_butn, self.p2_4ofaKind_butn, self.p2_fullHouse_butn,
                           self.p2_lowStrt_butn, self.p2_highStrt_butn, self.p2_yahtzee_butn,
                           self.p2_chance_butn, self.p2_yzBonus_butn]

    def bottom_frame(self):
        # frame to house game playing buttons
        bot_frame = tk.Frame(self.window, bg=BTM_COLOR)
        bot_frame.place(relx=0.0, rely=0.8, relwidth=1.0, relheight=0.2)

        # game playing buttons and Yahtzee label
        self.player_label = tk.Label(bot_frame, font=SECTION_FONT, bg=BTM_COLOR)
        self.player_label.place(relx=0.02, rely=0.0, relwidth=0.1, relheight=0.4)

        self.roll_label = tk.Label(bot_frame, font=SECTION_FONT, bg=BTM_COLOR)
        self.roll_label.place(relx=0.13, rely=.0, relwidth=0.6, relheight=0.4)

        self.roll_button = tk.Button(bot_frame, command=self.roll)
        self.roll_button.place(relx=0.05, rely=0.35, relwidth=0.2, relheight=0.2)

        self.start_button = tk.Button(bot_frame, text='Start', command=self.start)
        self.start_button.place(relx=0.05, rely=0.6, relwidth=0.09, relheight=0.2)

        self.score_button = tk.Button(bot_frame, text='Score', command=self.scoring)
        self.score_button.place(relx=0.16, rely=0.6, relwidth=0.09, relheight=0.2)

        self.yahtzee_label = tk.Label(bot_frame, text='Yahtzee', font=Y_FONT, bg=BTM_COLOR)
        self.yahtzee_label.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.5)

        self.total_label = tk.Label(bot_frame, text='Game Totals', font=SECTION_FONT, bg=BTM_COLOR)
        self.total_label.place(relx=0.45, rely=0.05, relwidth=0.15, relheight=0.1)

        self.p1_total_label = tk.Label(bot_frame, text='0', font=SECTION_FONT)
        self.p1_total_label.place(relx=0.64, rely=0.05, relwidth=0.1, relheight=0.1)

        self.p2_total_label = tk.Label(bot_frame, text='0', font=SECTION_FONT)
        self.p2_total_label.place(relx=0.84, rely=0.05, relwidth=0.1, relheight=0.1)

        self.newGame_button = tk.Button(bot_frame, text='New Game', command=self.new_game)
        self.newGame_button.place(relx=0.75, rely=0.35, relwidth=0.2, relheight=0.2)

        self.quitGame_button = tk.Button(bot_frame, text='End Game', command=quit)
        self.quitGame_button.place(relx=0.75, rely=0.6, relwidth=.2, relheight=0.2)

    def game_board(self):
        # put the board together
        self.die_frame()
        self.scoring_frame()
        self.playOne_frame()
        self.playTwo_frame()
        self.bottom_frame()

    def new_game(self):
        # reset all game variables
        self.game_board()

        self.reset()

        self.player_label.configure(text='Player 1')
        self.start_button.configure(state=tk.NORMAL)
        self.roll_button.configure(state=tk.DISABLED)
        self.score_button.configure(state=tk.DISABLED)

########################################################################################################################
########################################################################################################################

root = tk.Tk()

game = Yahtzee(root)

root.mainloop()
