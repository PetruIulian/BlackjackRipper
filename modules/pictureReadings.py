import cv2
import easyocr

def aplicare_filtru(cards_region):
    # Adăugați aici logica de filtrare specifică imaginilor cărților de joc
    # Exemplu simplu: conversie la alb-negru
    cards_region = cv2.cvtColor(cards_region, cv2.COLOR_BGR2GRAY)
    return cards_region

def read_and_process_cards(img_path):
    # Citirea imaginii
    image = cv2.imread(img_path)

    # Definirea regiunilor de interes pentru cărțile jucătorului și ale dealerului
    my_cards = image[200:400, 250:450]
    dealer_cards = image[200:400, 800:1000]

    # Aplicarea filtrului la regiunile de interes
    my_cards_filtered = aplicare_filtru(my_cards)
    dealer_cards_filtered = aplicare_filtru(dealer_cards)

    # Afișarea imaginilor filtrate
    cv2.imshow("Cărțile Jucătorului", my_cards_filtered)
    cv2.imshow("Cărțile Dealerului", dealer_cards_filtered)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Initializarea cititorului EasyOCR
    reader = easyocr.Reader(['en'])

    # Funcția pentru a citi cărțile
    def read_cards(cards_region):
        # Utilizarea EasyOCR pentru a citi textul
        cards_text = reader.readtext(cards_region, detail=0)
        return cards_text

    # Citirea cărților pentru jucător și dealer
    my_cards_text = read_cards(my_cards_filtered)
    dealer_cards_text = read_cards(dealer_cards_filtered)

    return my_cards_text, dealer_cards_text