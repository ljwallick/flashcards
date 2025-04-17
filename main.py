from fmanager import fmanager

def main():
    manager = fmanager()
    helper = {'commands': getHelp().commands, 'help': getHelp().help, 'cd': getHelp().cd, 'dir': getHelp().dir, 'new': getHelp().new, 'edit': getHelp().edit, 'del': getHelp().delete, 'delmany': getHelp().delmany, 'empty': getHelp().empty, 'view': getHelp().view, 'study': getHelp().study, 'bkup': getHelp().bkup}
    s = input("Enter custom separator:\n(Default is '/' and cannot choose '.')\n") or '/'
    if s.lower() in 'abcdefghijklmnopqrstuvwxyz.[]{}() ' or len(s) > 1:
        s = '/'
        print("Choice overridden. Reverting to '/'")
    manager.s = s
    print("Type 'help commands' to view commands and 'exit' to quit.")
    while True:
        command = input(f"Root:{s}{s.join(manager.current_dir)}>").split(' ')
        commandKW = command[0] # KW = KeyWord
        if command[0].lower() == 'exit':
            break
        elif commandKW not in helper:
            print(f"Error. Unknown command '{commandKW}'")
            continue
        
        if commandKW == 'help':
            if len(command) == 1:
                print("Syntax Error.\n- Required: <command>")
            elif command[1] not in helper:
                print(f"Error. Unknown command '{command[1]}'")
            elif len(command) > 2:
                print("Syntax Error.\n- help <command>")
            print(f"{command[1]} help:")
            helper[command[1]]()
            continue
        
        elif commandKW == 'cd':
            if len(command) == 1:
                print("Syntax Error.\n- Required: <target>")
                continue
            new_dir = ' '.join(command[1:]).split(s)
            manager.change_directory(new_dir.pop(0), new_dir)
        elif commandKW == 'dir':
            if len(command) > 1:
                print("Syntax Error.\n- This function requires no arguments.")
                continue
            manager.view_contents()
        elif commandKW == 'new':
            if len(command) == 1:
                print("Syntax Error.\n- Required: <type>")
                continue
            manager.new(command[1].lower())
        elif commandKW == 'edit':
            if len(command) == 1:
                print("Syntax Error.\n- Required: <name>")
                continue
            manager.edit(' '.join(command[1:]))
        elif commandKW == 'del':
            if len(command) == 1:
                print("Syntax Error.\n- Required: <name>")
                continue
            manager.delete(' '.join(command[1:]))
        elif commandKW == 'delmany':
            if len(command) > 1:
                print("Syntax Error.\n- This function requires no arguments.")
                continue
            manager.delmany()
        elif commandKW == 'empty':
            manager.empty((' '.join(command[1:])) if len(command) > 1 else None)
        elif commandKW == 'view':
            if len(command) == 1:
                print("Syntax Error.\n- Required: <card>")
                continue
            manager.view(command[1:])
        elif commandKW == 'study':
            manager.study((' '.join(command[1:])) if len(command) > 1 else None)
        elif commandKW == 'bkup':
            if len(command) == 1:
                manager.bkup('save')
                continue
            elif len(command) > 2:
                print("Syntax Error.\n- bkup <mode>") # <directory>
                continue
            manager.bkup(command[1].lower()) # ' '.join(command[2:]).split(s) if len(command) > 2 else [None]


class getHelp():
    def commands(self):
        print("""    Commands:
     |  help: This one's obvious...
     |  cd: Changes directory to a given target.
     |  dir: Shows every element in the current directory.
     |  new: Creates a new Folder, Deck, or Card.
     |  del: Deletes a Folder, Deck, or Card.
     |  delmany: Allows deletion of multiple items quickly.
     |  empty: Empties the current or selected directory.
     |  view: Displays the contents of a card.
     |  study: Lets the user practice the flashcards in current or target deck.
     |  bkup: Backs up your data or loads your backup.
     """)

    def help(self):
        print("""    A vacuous one, aren't you?
    """)

    def cd(self):
        print("""    Changes directory to a given target.

    Syntax: cd <target>
     |  target: Directory you wish to change to.
     |  - You can go down multiple paths using '/' between each.
     |  - To avoid typing whole directories, just type enough to distiguish it from others.
    """)

    def dir(self):
        print("""    Shows every element in the current directory.
    
    Syntax: dir
    """)

    def new(self):
        print("""    Creates a new Folder, Deck, or Card.

    Syntax: new <type>
     |  type: Type of object being created (Folder, Deck, Card).
     |  - Append an 's' to create multiple (eg. Folders).
    """)
    
    def edit(self):
        print("""    Edits a Folder, Deck, or Card.
              
    Syntax: edit <name>
     |  name: Name of Folder, Deck, or Card being edited.
    """)
        
    def delete(self):
        print("""    Deletes a Folder, Deck, or Card.

    Syntax: del <name>
     |  name: Name of Folder, Deck, or Card being deleted.
    """)
        
    def delmany(self):
        print("""    Allows deletion of multiple items quickly.

    Syntax: delmany
     |  Enter item names followed by 'Enter'.
     |  - Deletes them one at a time, as inputted.
    """)
    
    def empty(self):
        print("""    Empties the current or selected directory.

    Syntax: empty <directory(opt)>
     |  directory: Empties the target directory instead.
    """)

    def view(self):
        print("""    Displays the contents of a card.

    Syntax: view <name> <hint(opt)>
     |  name: name of the card.
     |
     |  hint: Displays the card's hint.
     |  - Can be shortened to 'h'.
    """)
        
    def study(self):
        """    Lets the user practice the flashcards in current or target deck.
        
        Syntax: study <deck(opt)>
         |  deck: Selects a deck to practice instead of current directory."""
        
    def bkup(self):
        print("""    Backs up your data or loads your backup.
    
    Syntax: bkup <mode>
     |  mode: Decides between loading or saving data.
     |  - 'save' will save your data to a backup.
     |  - 'load' will load your data from a backup.
    """)

main()