from modules.dialogs import startScreen, ask
from modules.strategyParse import parseStrategy
from modules.pictureReadings import read_and_process_cards
if __name__ == "__main__":
    startScreen()
    ans = ask("Do you want to start?", {"a": "Yes", "b": "No"})
    if ans == "a":
        img_path = "files/screenshot.png"
        my_cards_text, dealer_cards_text = read_and_process_cards(img_path)

    # Afișarea rezultatelor
        print(f"Cărțile jucătorului: {my_cards_text}")
        print(f"Cărțile dealerului: {dealer_cards_text}")
    else:
        print("Bye!")
    