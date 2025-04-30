# What is it, you ask?

I made a sorta *unique* flashcard program. I realized after making it that you can tell it sort of resembles Ankidroid's folder structure.<br>
<br>
Basically, you have commands, and can do a good amount of file management with them. Like cd, dir, new, del, etc.<br>
You can see all the commands by using the command: help commands<br>
Use *help \<cmd>* to view a more detailed help for a specific command.<br>
<br>
My favorite function is the *study* function, because of its functionality.<br>
Basically, it has a history or recent flashcards, and it cannot select one from that. If it does, it skips it.<br>
How long is this history variable? Well, it depends on how long the deck is AND how bad your worst card is.<br>
<br>
What that means is, I have a *weight* variable attached to each card. 1 is the best, while the worst would be equal to half the length of the deck. 
I then make a study deck that has each card appear its weight amount of times. Now there is a deck that has your best cards appearing less than you worse cards.<br>
<br>
Now, I take the length of that deck and divide it by the max weight of all the cards(your worst one). I set the history to that result. This lets you not get the same card multiple times in a row, allowing a more even distribution.<br>
<br>
That is my favorite function, but that doesn't mean i don't like the others. Go explore them, see which one is your favorite.
