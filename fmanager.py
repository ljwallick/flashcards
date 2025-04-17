import json
import os
import random

class fmanager:
    def __init__(self, json_file="Flash Cards/cards.json"):
        self.s = '/'
        self.json_file = json_file
        self.json_bak = os.path.splitext(self.json_file)[0] + '_bak.json'
        self.load_data()
        self.current_dir = []  # Tracks the current directory path
        self.Types = ('Root', 'Folder', 'Deck', 'Card')

    def load_data(self):
        """Load flashcard data from the JSON file."""
        if not os.path.exists(self.json_file):
            self.data = {
                "Type": "Folder"
            }
            self.save_data()
        else:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)

    def save_data(self):
        """Save flashcard data to the JSON file."""
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)
    
    def load_backup(self):
        """Load flashcard data from the backup JSON file."""
        if not os.path.exists(self.json_bak):
            print('Error. No backup is available.')
            return False
        else:
            with open(self.json_bak, 'r', encoding='utf-8') as f:
                databak = json.load(f)
            return databak
    
    def save_backup(self):
        """Save flashcard data to the backup JSON file."""
        with open(self.json_bak, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def check_dir_exists(self, directory, bkup = False):
        """Checks if the specified directory exists."""
        if bkup:
            folder = self.load_backup()
        else:
            folder = self.data
        folder_path = []
        for dir_name in directory:
            if dir_name in folder:
                folder = folder[dir_name]
                folder_path += [dir_name]
            else:
                break
        else:
            return True
        return False

    # This function is unsusable at this time
    def bkup(self, mode): # directory
        """Back up your data or load your backup."""
        print("Failed to backup data.")
        return
        folder = self.get_current_folder()
        # test_dir = self.current_dir
        if mode not in ('save', 'load'):
            print("Invalid argument.\nValid modes are 'load', and 'save'.")
            return
        # if directory[0] == '.':
        #     if len(directory) == 1:
        #         print("Argument Error.\nDirectory needs a filename. Syntax: bkup save ./<folder name>")
        #         return
        #     test_dir += directory[1:]
        # if directory:
        #     path_cur = self.check_dir_exists(test_dir) # Checks if it's a valid directory in the current files
        #     path_bkup = self.check_dir_exists(test_dir, True) # Checks in backup files
        #     print(path_cur, path_bkup)
        #     
        #     if mode == 'save':
        #         if not path_cur:
        #             print("Path Error.\nPlease make sure this path exists.")
        #             return
        #         confirm = input('This will override the existing folder.\nAre you sure? (y/n) ')

        #     else:
        #         if not path_bkup:
        #             print("Path Error.\nPlease make sure this path exists.")
        #             return
        #         pass
        #         confirm = input('This will override the existing folder.\nAre you sure? (y/n) ')

        else:
            if mode == 'save':
                confirm = input('This will overwrite your existing backup.\nAre you sure? (y/n) ')
                if confirm != 'y':
                    print('Canceled.\n')
                    return
                self.save_backup()
                print("Backup Complete!\n")
            else:
                confirm = input('This will overwrite your current data.\nAre you sure? (y/n) ')
                if confirm != 'y':
                    print('Canceled.\n')
                databak = self.load_backup()
                if databak:
                    self.data = databak
                    self.save_data()
                    print('Restoration Complete!\n')
                else:
                    print("Error. Backup does not exist.\n")

    def change_directory(self, target_dir, target_dirs_left:list):
        """Change to any nested subfolder or go up a level."""
        if target_dir == '..':
            if self.current_dir:
                self.current_dir.pop()
            else:
                print("Already at the root directory.")
        else:
            folder = self.get_current_folder()
            folders = []
            if folder["Type"] == "Deck":
                print('Cannot change directory to a card.')
                return
            for i in folder.keys():
                if target_dir == i[0:len(target_dir)] and i != "Type":
                    folders.append(i)
            if len(folders) == 1:
                target_dir = folders[0]
            elif len(folders) > 1:
                print("Cannot change to multiple directories.")
                return
            if target_dir in folder and target_dir != 'Type':
                self.current_dir.append(target_dir)
            else:
                print(f"Folder '{target_dir}' does not exist in the current directory.")
                return

            if target_dirs_left:
                self.change_directory(target_dirs_left.pop(0), target_dirs_left)

    def view_contents(self):
        """View the contents of the current directory."""
        folder = self.get_current_folder()
        grouped = ([], [], [])
        print(f"Contents of Root:/{'/'.join(self.current_dir)}")
        for key, value in folder.items():
            if key != 'Type':
                if value["Type"] == 'Folder':
                    grouped[0].append(key)
                elif value["Type"] == 'Deck':
                    grouped[1].append(key)
                elif value["Type"] == 'Card':
                    grouped[2].append(key)
        grouped[0].sort(); grouped[1].sort(); grouped[2].sort()
        for group in range(3):
            for item in grouped[group]:
                if group == 0:
                    print(f"  [Folder] {item}")
                elif group == 1:
                    print(f"  [Deck] {item}")
                elif group == 2:
                    print(f"  [Card] {item}")
        print()

    def get_current_folder(self):
        """Retrieve the current folder based on the current directory path."""
        folder = self.data
        for dir_name in self.current_dir:
            if dir_name in folder:
                folder = folder[dir_name]
            else:
                return False
        return folder
    
    def new(self, Type:str):
        """Makes a new folder, deck, or card in the current directory."""

        if Type not in ('folder', 'folders', 'deck', 'decks', 'card', 'cards'):
            print('Invalid parameter.\n- Valid types are: Folder, Deck, Card.')
            return
        
        folder = self.get_current_folder()
        banned = ('/', '.', self.s) # Characters not allowed in names

        # If Type is a card
        if Type in ('card', 'cards'):
            if folder['Type'] != 'Deck':
                print('Cannot make new Card in current Folder.\nTry switching to Deck directory.')
                return
            elif Type == 'cards':
                print(f"Type '..' to exit.\nFollow the format: <term>{self.s}<answer>{self.s}<hint(opt)>.")
                while True:
                    card = input().split(self.s)
                    if '..' in card:
                        break
                    elif len(card) > 3 or len(card) < 2:
                        print(f'Syntax Error.\n<term>{self.s}<answer>{self.s}<hint(opt)>')
                        continue
                    if card[0] in folder:
                        print(f"Card '{card[0]}' already exists.")
                        continue
                    elif any([ i in banned for i in card[0] ]):
                        print(f"Card name cannot include '{"', '".join(banned)}'")
                        continue
                    else:
                        folder[card[0]] = {
                            "Type": "Card",
                            "answer": card[1],
                            "hint": card[2] if len(card) == 3 else None,
                            "weight": 3
                        }
            else:
                print("Type '..' to exit.")
                while True:
                    name = input('Name: ')
                    if name == '..': return
                    answer = input('Answer: ')
                    if answer == '..': return
                    hint = input('Hint(opt): ') or None
                    if hint == '..': return

                    if name in folder:
                        print(f"Card '{name}' already exists.")
                        continue
                    elif any([ True if i == j else False for i in name for j in banned ]):
                        print(f"Card name cannot include '{"', '".join(banned)}'")
                        continue
                    else:
                        folder[name] = {
                            "Type": "Card",
                            "answer": answer,
                            "hint": hint,
                            "weight": 3
                        }
                        break
        else:
            if folder['Type'] == 'Deck':
                print(f"Cannot make new '{Type.title()}' in current Deck.\nTry switching to Folder directory.")
                return
            elif Type in ('folders', 'decks'):
                print(f"Type '..' to exit.\nEnter each {Type.title()} name followed by 'Enter'.")
                while True:
                    name = input()
                    if name == '..':
                        break
                    if name in folder:
                        print(f"Directory '{name}' already exists.")
                        continue
                    elif any([ True if i == j else False for i in name for j in banned ]):
                        print(f"{Type.title()} name cannot include '{"', '".join(banned)}'")
                        continue
                    else:
                        folder[name] = {
                            "Type": Type[0:-1].title()
                        }
            else:
                print("Type '..' to exit.")
                while True:
                    name = input('Name: ')
                    if name == '..':
                        return
                    if name in folder:
                        print(f"Directory '{name}' already exists.")
                        continue
                    elif any([ True if i == j else False for i in name for j in banned ]):
                        print(f"{Type.title()} name cannot include '{"', '".join(banned)}'")
                    else:
                        folder[name] = {
                            "Type": Type.title()
                        }
                        break
        self.save_data()

    def edit(self, name:str):
        """Edit the selected item."""
        folder = self.get_current_folder()
        banned = ('/', '.', self.s)
        if name not in folder or name == 'Type':
            print('That item does not exist.')
            return
        print("Type '..' at any time to exit current loop.")
        if folder[name]["Type"] == 'Card':
            commands = ('name', 'answer', 'hint')
        elif folder[name]['Type'] in ('Folder', 'Deck'):
            commands = ('name', 'type')
        print(f"Editable values: {', '.join(commands)}.\n")

        while True:
            command = input('Select value to edit: ')
            if command.lower() == '..': break
            if command.lower() not in commands:
                print('Invalid command. Try again.')
                continue
            if command.lower() == 'name':
                while True:
                    new_name = input('Enter a new name: ')
                    if new_name == '..': break
                    elif any([ True if i == j else False for i in new_name for j in banned ]):
                        print(f"{name} name cannot include '{"', ".join(banned)}'.")
                        continue
                    elif new_name == name:
                        print('Cannot rename to its current name.')
                        continue
                    elif new_name in folder:
                        print('Name already exists.' if new_name != 'Type' else 'Invalid name.')
                        continue
                    folder[new_name] = folder.pop(name)
                    name = new_name
                    break
            elif command.lower() == 'type' and command.lower() in commands:
                if folder[name]["Type"] == 'Deck':
                    confirm = input("This will change all Cards inside into Folders. Are you sure? (y/n) ")
                    if confirm.lower() != 'y':
                        print('Type change cancelled.')
                    else:
                        for key in folder[name].keys():
                            if key == 'Type':
                                folder[name][key] = "Folder"
                            else:
                                folder[name][key] = {
                                    "Type": "Folder",
                                    'answer': {"Type": "Folder", folder[name][key]['answer']: {"Type": "Folder"}},
                                    'hint': {"Type": "Folder", folder[name][key]['hint']: {"Type": "Folder"}}
                                    }
                else:
                    confirm = input("This will change all Decks or Folders inside into Cards, making you add info to complete them and deleting any subfolders. Are you sure? (y/n) ")
                    if confirm.lower() != 'y':
                        print('Type change cancelled.')
                    else:
                        for key in folder[name].keys():
                            if key == "Type":
                                folder[name][key] = "Deck"
                            else:
                                print(f"Card: {key}")
                                answer = input("Answer: ")
                                hint = input("Hint(Enter to skip): ")
                                folder[name][key] = {
                                     "Type": "Card",
                                     "answer": answer,
                                     "hint": hint,
                                     "weight": 3
                                }
            elif command == "answer" and command.lower() in commands:
                while True:
                    new_answer = input('New answer: ')
                    if new_answer == '..': break
                    elif new_answer == folder[name]["answer"]:
                        print('Cannot change to same answer.')
                        continue
                    folder[name]["answer"] = new_answer
                    break
            elif command == "hint" and command.lower() in commands:
                while True:
                    new_hint = input('New hint: ')
                    if new_hint == '..': break
                    elif new_hint == folder[name]["hint"]:
                        print('Cannot change to same hint.')
                        continue
                    folder[name]["hint"] = new_hint
                    break
            else: print('Invalid value.')
        data = self.data
        self.load_data()
        if self.data == data: return
        confirm = input("You have made changes. Type 'revert' to undo them: ")
        if confirm.lower() == 'revert':
            print('Changes reverted.')
            return
        self.data = data
        self.save_data()
        return
    
    def delete(self, name):
        """Delete specified Folder, Deck, or Card."""
        folder = self.get_current_folder()
        if name not in folder or name == 'Type':
            print('That item does not exist.')
            return
        if len(folder[name]) > 1:
            if folder[name]["Type"] != 'Card':
                confirm = input(f"{name} and all of its contents will be permanently deleted.\nAre you sure? (y/n) ")
            else:
                confirm = input(f"{name} will be permanently deleted.\nAre you sure? (y/n) ")
            if confirm.lower() != 'y':
                print('Deletion canceled.')
                return
        del folder[name]
        self.save_data()

    def delmany(self):
        """Delete many items in quick succession without confirmations."""
        folder = self.get_current_folder()
        if folder["Type"] == 'Deck':
            confirm = input("All valid Cards will be permanently deleted without confirmation.\nContinue? (y/n) ")
        else:
            confirm = input("All valid directories and their contents will be permanently deleted without confirmation.\nContinue? (y/n) ")
        if confirm != 'y':
            print('Returning...\n')
            return
        print(f"\nType '..' to exit.\nEnter any valid names followed by 'Enter'.")
        while True:
            name = input()
            if name == '..':
                break
            if name not in folder and name != 'Type':
                print('That item does not exist.')
                continue
            del folder[name]
        print()
        self.save_data()

    def empty(self, path):
        """Empty current direcctory or selected path."""
        folder = self.get_current_folder()
        if path and (path not in folder or path == 'Type'):
            print('That directory does not exist.')
            return
        elif folder[path]["Type"] == 'Card':
            print('Cannot empty a Card.')
            return
        if path:
            confirm = input(f"All contents of {path} will be permanently deleted.\nAre you sure? (y/n) ")
            if confirm.lower() != 'y':
                print('Deletion canceled.\n')
                return
            Type = folder[path]["Type"]
            folder[path] = {
                "Type": Type
            }
        else:
            confirm = input(f"All contents in the current directory will be permanently deleted.\nAre you sure? (y/n) ")
            if confirm.lower() != 'y':
                print('Deletion canceled.\n')
                return
            Type = folder["Type"]
            folder.clear()
            folder["Type"] = Type
        print()
        self.save_data()
    
    def view(self, card:list):
        """Lets you view card details."""
        folder = self.get_current_folder()
        hint = ""
        if card[-1] in ('h', 'hint'):
            hint = card[-1]
            card.pop()
        card = ' '.join(card)
        if folder['Type'] != 'Deck':
            print('That is not a Card.')
            return
        elif card not in folder:
            print('That Card does not exist.')
            return
        elif hint and (hint not in ('h', 'hint')):
            print("Invalid parameter.\nHint does not show by default. Type 'h' or 'hint' to show.")
            return
        
        print(f" |  Term: {card}")
        print(f" |  Answer: {folder[card]['answer']}")
        if folder[card]['hint'] and hint:
            print(f" |  Hint: {folder[card]['hint']}")

    def study(self, deck):
        """Studies a deck"""
        folder = self.get_current_folder()
        self.study_errors(folder, deck) # Checks for errors
        # Get the cards from the deck
        if deck:
            study = { card: answer for card, answer in folder[deck].items() if card != 'Type' } # If card == 'Type', then it is not supposed to be used.
        else:
            study = { card: answer for card, answer in folder.items() if card != 'Type' }
        
        max_iterations = len(study)
        if max_iterations < 6:
            print("Not enough cards. Please add at least 6 to effectively study!")
            return
        iterations = input(f"How many cards do you want to practice in intervals? ")
        try:
            iterations = int(iterations)
        except:
            print("That is not a number.")
            confirm = input(f"Continuing with default '{(iterations:= int(max_iterations/2))}'. Is that okay? (y/n) ")
            if confirm != 'y':
                print('Exiting...')
                return
        else:
            if iterations < 2:
                print("Iterations too small!")
                confirm = input(f"Continuing with default '{(iterations:= int(max_iterations/2))}'. Is that okay? (y/n) ")
                if confirm != 'y':
                    print('Exiting...')
                    return
        cards, max_weight = self.make_cards(study)
        recents = []
        """
        This history variable is very cool. It takes the length of the 
        deck and the highest weight and makes the perfect history length.

        This would make it appear AT MOST its weight value every sweep through 
        the deck, letting you still get other cards.
        """
        history = max_iterations // max_weight
        self.practice_cards(study, cards, recents, iterations, max_iterations, history)

    def study_errors(self, folder, deck):
        """Checks is the folder is valid"""
        if folder["Type"] != 'Deck' and not deck:
            print("This is not a Deck.") # Cannot study a regular folder.
            return
        elif deck and folder[deck]["Type"] != 'Deck':
            print("That is not a Deck.")
            return
        elif deck and deck not in folder:
            print("That Deck does not exist.")
            return

    def make_cards(self, study:dict[str:str]) -> tuple[dict, int]:
        cards = []
        max_weight = 0
        for i in study.keys():
            cards += [i] * study[i]['weight'] # Multiplies the card by its weight to let you study your bad cards more often, and vice vera.
            max_weight = max(max_weight, study[i]['weight']) # Gets the highest 'weight' value from all the cards.
        return cards, max_weight

    def practice_cards(self, study:dict[str:str], cards:list[str], recents:list[str], iterations:int, max_iterations:int, history:int):
        while True:
            # I wanted to be able to edit the range directly, so when I skip a card, it won't change how many cards are shown.
            for _ in ( iters:= list(range(iterations)) ): 
                if not cards:
                    cards, _ = self.make_cards(study) # If all cards have been used, remake them.
                    print('REMADE CARDS!')
                
                random.shuffle(cards) # Shuffle cards every iteration to increase randomness.

                term = cards.pop()
                if term in recents:
                    iters.append(max(iters) + 1) # Adds another iteration to the end because we are skipping one.
                    cards.append(term) # Adding the skipped card back.
                    continue
                if len(recents) > history: # Removes oldest item from history if it has reached its maximum length.
                    recents.pop(0)
                
                answer:str = study[term]["answer"]
                recents.append(term) # Adds this term to recents to avoid immediate repeats.

                print(f' |  Term: {term}')
                user_answer = input(" |  - Your Answer: ")

                if user_answer.lower() == answer.lower():
                    print("Correct!\n")
                    study[term]["weight"] = max(1, study[term]["weight"] - 1)  # Decrease weight to make it appear less
                else:
                    print(f"Wrong! The correct answer is: {answer}\n")
                    study[term]["weight"] = min(max_iterations // 2, study[term]["weight"] + 1)  # Increase weight to make it appear more
                
            if input('Do you want to continue? (y/n) ') != 'y':
                print("Exiting...")
                break

        self.save_data()

        
