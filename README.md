# Flashcards-CTk
A CustomTkinter implementation of a term memorisation and testing system.

## Requirements
CustomTkinter and Tkinter. Run:
```
pip install customtkinter tk
```

## Design
This app is built with CustomTkinter. "Flashcards" are stored in JSON files. There are a few different options:
- **Test:** Randomly go through terms for you to test yourself with. Flip the "card" to see if you are right.
- **Create new:** As the name suggests, create a new "flashcard" set.

## How parts were implemented
### Test
Each word is given a score, starting at 0. If greater than 0, a random integer is selected between 0 and the score. If this integer is 0, the word is displayed to the user.

Getting the term correct increases this score by 1, and getting it wrong decreases it by 1 to a minimum to 0.

The purpose of this is to encourage the user to practice more on the terms they are weaker with.
