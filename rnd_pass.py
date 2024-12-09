import string
from colorama import Fore, Style, init, Back
import random
from nltk.corpus import words                 # is a large collection of natural language datasets, we've used it for accessing english words

lett = string.ascii_letters
nums = ['1','2','3','4','5','6','7','8','9','0']
syms = ['#','!','$','%','&','-','_','@','?']
final_pass = []


def selector_menu():                                                   # options menu for password customization

    lett_bool = 0
    wrd_bool = 0
    wrd_cnt = 0
    num_bool = 0
    sym_bool = 0
    print("Welcome to random password generator !")
    print("Before generation of your random password, please select the options below: ")

    pass_bool = str(input("Do you want to customize your password ? ( Y / N ) : "))
    while (pass_bool.lower() != 'y' and pass_bool.lower() != 'n'):                               # to check whether the input provided is either 'y' or 'n'
        print("Please give appropriate response.")
        pass_bool = str(input("Do you want to customize your password ? ( Y / N ) : "))

    if pass_bool.lower() == 'y' :
        pass_len = int(input("Enter the length you want your password to be: "))

        lett_char = str(input("Do you want Characters in your password ? ( Y / N ) : "))
        while (lett_char.lower() != 'y' and lett_char.lower() != 'n'):
            print("Please give appropriate response.")
            lett_char = str(input("Do you want Characters in your password ? ( Y / N ) : "))
        if lett_char.lower() == 'y': 
            lett_bool = 1
        
        num_char = str(input("Do you want Numbers in your password ? ( Y / N ) : "))
        while num_char.lower() != 'y' and num_char.lower() != 'n':
            print("Please give appropriate response.")
            num_char = str(input("Do you want Numbers in your password ? ( Y / N ) : "))
        if num_char.lower() == 'y': 
            num_bool = 1
        
        sym_char = str(input("Do you want Symbols in your password ? ( Y / N ) : "))
        while sym_char.lower() != 'y' and sym_char.lower() != 'n':
            print("Please give appropriate response.")
            sym_char = str(input("Do you want Symbols in your password ? ( Y / N ) : "))
        if sym_char.lower() == 'y': 
            sym_bool = 1

        if pass_len > 3:
            word_char = str(input("Do you want Words in your password ? ( Y / N ) : "))
            while word_char.lower() != 'y' and word_char.lower() != 'n':
                print("Please give appropriate response.")
                word_char = str(input("Do you want Words in your password ? ( Y / N ) : "))
            if word_char.lower() == 'y': 
                wrd_bool = 1
                wrd_cnt = int(input("How many words do you want in your password : "))
                if (lett_bool + num_bool + sym_bool > 0):
                    while wrd_cnt >= (pass_len/2)-1:
                        print("Please give appropriate response.")
                        wrd_cnt = int(input("How many words do you want in your password : "))
                else:
                    while wrd_cnt >= (pass_len-1):
                        print("Please give appropriate response.")
                        wrd_cnt = int(input("How many words do you want in your password : "))
        
        


    else:                                                               # if you dont need any customizations
        pass_len = random.randint(6,30)
        lett_bool = random.randint(0,1)
        wrd_bool = random.randint(0,1)
        if wrd_bool == 1:
            wrd_cnt = random.randint(1, round(pass_len/2) - 2)
        num_bool = random.randint(0,1)
        sym_bool = random.randint(0,1)

    if pass_len == 0 or (lett_bool == 0 and wrd_bool == 0 and num_bool == 0 and sym_bool == 0):
        print("I dont think you want a password.")

    pass_generator(pass_len, lett_bool, wrd_bool, wrd_cnt, num_bool, sym_bool)


def pass_generator(pass_len, lett_bool, wrd_bool, wrd_cnt,  num_bool, sym_bool):                    # the main random password generator 

    bool_active = num_bool + sym_bool + lett_bool
#==============================================================================================================================
    total_len = pass_len
    curr_len = 0
    overflow = 0 #if word length is less then half the password length
    done = 0
    temp_count = 0
    pass_list = []
    word_list = []
    if wrd_cnt > 0 :
        if bool_active > 0:
            segment = round(pass_len * (1 / wrd_cnt))                       #to find words starting from half the given length
        else:
            segment = pass_len
        if segment > 24:                                                    #max length word is 24 characters, hence here to prevent infinite looping 
            segment = 24
            overflow = 1
        for i in range(0, 1 + round(pass_len)):
            while segment > 0 :
                filtered_word = [word for word in words.words() if (len(word) == segment)]                 #finds and adds words
                if overflow == 1:
                    for x in range(0,5):
                        word_list.append(random.choice(filtered_word))
                    word_list = random.choice(word_list)
                    
                    segment = 0
                else:
                    word_list.append(random.choice(filtered_word))
                    segment -= 1

        while done == 0 and overflow == 0:                               
            temp_list = random.sample(word_list, wrd_cnt)
            for x in temp_list:
                temp_count += len(x) 
            if bool_active > 0:                                                                              # checks for active settings
                if (temp_count > round(pass_len * 0.5)) and (temp_count < round(pass_len * 0.7)):             #words in password to take 50% - 70% space in the entire length
                    word_list.clear()
                    word_list = temp_list
                    done = 1
                    break
            else:
                if temp_count == pass_len:
                    word_list.clear()
                    word_list = temp_list
                    done = 1
                    break

            temp_count = 0
        
        if overflow == 0:
            for items in word_list:
                curr_len += len(items)
                if random.randint(0,2) == 1:
                    items = items.capitalize()
                pass_list.append(items) 
        else:
            if random.randint(0,2) == 1:
                word_list =  word_list.capitalize()
            pass_list.append(word_list) 

    else:
        wrd_cnt = 1
        segment = round(pass_len * (1 / wrd_cnt))
    
    
#===============================================================================================================================================

    remaning_len = total_len - curr_len
    sym_selected = ""
    num_selected = ""
    char_selected = ""
    
    if bool_active > 1:                                                               #almost equally assigns the ramaning 30% - 50% password length to numbers, characters and symbold 
        while remaning_len >= 1:                                                          #assigns them till the entire password length is finished
            if num_bool and remaning_len > 0:
                num_selected = random.sample(nums, random.randint(1, (2 + (remaning_len * round(1/bool_active)))))
                pass_list += num_selected
                remaning_len -= len(num_selected)

            if sym_bool and remaning_len > 0:
                sym_selected = random.sample(syms, random.randint(1, (2 + (remaning_len * round(1/bool_active)))))
                pass_list += sym_selected
                remaning_len -= len(sym_selected)

            if lett_bool and remaning_len > 0:
                char_selected = random.sample(lett, random.randint(1, (1 + (remaning_len * round(1/bool_active)))))
                pass_list += char_selected
                remaning_len -= len(char_selected)

   elif bool_active == 1:                   #if only one setting is active then assigns remaining spaces to the applied setting
        if num_bool:
            for i in range(0,remaning_len):
                num_selected += random.choice(nums)
            pass_list += num_selected

        if sym_bool:
            for i in range(0,remaning_len):
                sym_selected += random.choice(syms)
            pass_list += sym_selected

        if lett_bool:
            for i in range(0,remaning_len):
                char_selected += random.choice(lett)
            pass_list += char_selected

    random.shuffle(pass_list)
    global final_pass 
    final_pass = "".join(pass_list)

selector_menu()
print("Your password is:  " + Back.WHITE + Fore.BLACK + " " + final_pass + " " + Back.RESET + Fore.RESET)            
print("Password length = ", len(final_pass))
