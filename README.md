# 📦 Information theory tools

## ℹ️ O projekcie

#### [🇬🇧 English version](#ℹ️-about-the-project)

Programy są realizacją zadań z przedmiotu `Teoria informacji i metody kompresji danych`, na VI semestrze studiów pierwszego stopnia na kierunku Informatyka na Politechnice Poznańskiej.

### ➡️ Lista programów

1. Przybliżanie języka naturalnego na poziomie liter
    * Uruchom poleceniem `> python 01_NLA_letters.py "corpus.txt" "liczba znaków na wyjściu" "output.txt"`.
    * Program przetwarza tekst z korpusu (zostawia tylko słowa składające się wyłącznie z małych liter alfabetu), a następnie pozwala wygenerować 5 różnych przybliżeń języka:
        * zerowego rzędu (bez żadnych prawdopodobieństw),
        * pierwszego rzędu (częstość liter zgodna z częstością w korpusie),
        * na podstawie źródła Markova 1 rzędu (prawdopodobieństwo każdej nowej litery zależy od jednej poprzedniej),
        * na podstawie źródła Markova 3 rzędu (prawdopodobieństwo każdej nowej litery zależy od trzech poprzednich),
        * na podstawie źródła Markova 5 rzędu (prawdopodobieństwo każdej nowej litery zależy od pięciu poprzednich).
    * Program podaje zawsze średnią długość słowa z korpusu oraz w wygenerowanym tekście. W zależności od metody dodaje również dodatkowe informacje.
    * Program zapisuje w pliku wyjściowym przybliżenie języka.
2. Przybliżanie języka naturalnego na poziomie słów
    * Uruchom poleceniem `> python 02_NLA_words.py "corpus.txt" "liczba znaków na wyjściu" "output.txt"`.
    * Program przetwarza tekst z korpusu (rozdziela na słowa), a następnie pozwala wygenerować 3 różne przybliżenia języka:
        * pierwszego rzędu (częstość słów zgodna z częstością w korpusie); dodatkowo podaje 50 najczęstszych słów z korpusu oraz ile % wszystkich słów stanowi 6000 i 30000 najczęstszych słów,
        * na podstawie źródła Markova 1 rzędu (prawdopodobieństwo każdego nowego słowa zależy od jednego poprzedniego),
        * na podstawie źródła Markova 2 rzędu (prawdopodobieństwo każdego nowego słowa zależy od dwóch poprzednich).
    * Program zapisuje w pliku wyjściowym przybliżenie języka.
3. Kompresje plików
    * Uruchom poleceniem `> python 03_compression.py`.
    * Program pozwala kompresować pliki trzema metodami:
        * kodowanie binarne o stałej długości słów,
        * kodowanie Huffmana,
        * kodowanie metodą LZW.
    * Program posiada interfejs tekstowy, w którym można wybrać następujące opcje:
        * wczytanie pliku przeznaczonego do kompresji (w txt lub w dowolnym formacie w metodzie LZW),
        * wczytanie skompresowanego pliku w formacie bin,
        * wczytanie pliku z kodem,
        * zakodowanie i odkodowanie pliku,
        * przygotowanie samego kodu,
        * zapisanie zakodowanego i odkodowanego pliku,
        * zapisanie kodu,
        * wyczyszczenie środowiska,
        * zmiana metody kodowania.

## ℹ️ About the project

#### [🇵🇱 Wersja polska](#ℹ️-o-projekcie)

The programs are implementations of assignments from the `Information Theory` course during the 6th semester of the Bachelor's degree in Computer Science at Poznan University of Technology.

### ➡️ List of programs

1. Natural language approximation at the character level
    * Run with:  
      `> python 01_NLA_letters.py "corpus.txt" "number of characters at the output" "output.txt"`
    * The program processes the text corpus (retains only words composed exclusively of lowercase alphabetic letters), and then allows generating 5 types of language approximations:
        * zero-order (no probabilities used),
        * first-order (character frequency matches that in the corpus),
        * based on a first-order Markov source (probability of each new character depends on the previous one),
        * based on a third-order Markov source (depends on the previous three characters),
        * based on a fifth-order Markov source (depends on the previous five characters).
    * The program always outputs the average word length in the corpus and in the generated text. Depending on the method, additional information may be included.
    * The language approximation is saved to the output file.

2. Natural language approximation at the word level
    * Run with:  
      `> python 02_NLA_words.py "corpus.txt" "number of characters at the output" "output.txt"`
    * The program processes the corpus (splits text into words), and allows generating 3 types of language approximations:
        * first-order (word frequency matches that in the corpus); additionally, it lists the 50 most frequent words and shows what percentage of all words is covered by the top 6000 and 30000 words,
        * based on a first-order Markov source (probability of each new word depends on the previous one),
        * based on a second-order Markov source (depends on the previous two words).
    * The language approximation is saved to the output file.

3. File compression
    * Run with:  
      `> python 03_compression.py`
    * The program allows compressing files using three methods:
        * fixed-length binary coding,
        * Huffman coding,
        * LZW coding.
    * It features a text-based interface where you can:
        * load a file to compress (in txt or any format for LZW),
        * load a compressed file in `.bin` format,
        * load a file containing a code,
        * encode and decode a file,
        * prepare a code only,
        * save the encoded and decoded file,
        * save the code,
        * clear the environment,
        * change the coding method.
