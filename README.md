# Connect 4

## Technologie:
python3.11
## Narzędzia:
- tensorflow
- numpy (ML)
- pygame (GUI)
## Opis projektu:
Gra w klasyczną wersję `Connect Four` z desktopowym GUI. Będziemy grali przeciwko algorytmowi opartemu o rozwiązania ML. Do wyboru będą dwa modele:
1. model, w którym odpowiedzą będzie ruch 0-6 (classification model),
2. model, w którym odpowiedzią będzie ewaluacja każdego ruchu (regression model).

Danymi wejściowymi, będzie plansza gry oraz informacja o tym, kto wykonuje następny ruch. Możliwe, że do modeli zostaną dostarczone dodatkowe informacje w zależności od potrzeb.
Dane treningowe/ewaluacyjne zostaną wygenerowane przez jeden z dostępnych silników do gry w `Connect Four`.
