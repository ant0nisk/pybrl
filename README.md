
# pybrl 

[![Twitter URL](https://img.shields.io/twitter/url/http/shields.io.svg?style=social)](https://twitter.com/intent/tweet?text=Contribute%20on%20pybrl:%20The%20open-source%20Braille%20translator%20on%20Github!%20https://github.com/ant0nisk/pybrl)

![Unicode Supported](https://img.shields.io/badge/license-GPL-blue.svg) ![Python: 3.5 Compatible](https://img.shields.io/badge/python-3.5-brightgreen.svg) ![Python: 3.9 Compatible](https://img.shields.io/badge/python-3.9-brightgreen.svg)

![Unicode Supported](https://img.shields.io/badge/unicode-supported-blue.svg) 

pybrl is an Open-Source Grade-2 Braille Translation system written entirely in Python. It is flexible and any new language can be imported in 10-minutes.


![pybrl logo](https://raw.githubusercontent.com/ant0nisk/pybrl/master/GithubContent/logo_200.png)


## How to use?
The usage of pybrl is super simple:

```python
In [1]: import pybrl as brl

In [2]: brl.translate("Hello World")   # Test for English
Out[2]: 
[[u'000001', u'110010', u'100010', u'111000', u'111000', u'101010'],
 [u'000001', u'010111', u'101010', u'111010', u'111000', u'100110']]

In [3]: example = _

In [4]: brl.translate("English with Ελληνικά") # Test with multiple languages
Out[4]: 
[[u'000001', u'100010', u'101110', u'110110', u'111000', u'010100', u'100101'],
 [u'011111'], [u'000010',  u'100010',  u'111000',  u'111000',  u'001110',  u'101110',  u'010100',  u'101000',  u'000010',  u'000101']]

In [5]: brl.toUnicodeSymbols(example, flatten=True)
Out[5]: u'\u2820 \u2813 \u2811 \u2807 \u2807 \u2815 \u2820 \u283a \u2815 \u2817 \u2807 \u2819'

In [6]: print _
⠠⠓⠑⠇⠇⠕ ⠠⠺⠕⠗⠇⠙

```

It has automatic language detection, and recognizes different languages as you translate.

## Install Dependencies
Open the directory of the project in the Terminal and run:
`pip install -r requirements.txt`

(You will probably need to add `sudo` in the beginning of that command. Do so if you get Permission errors.)

## How to import a new Language?
Each Language file is located under the `languages` directory. It has 3 dictionaries:

1) `alphabet` contains all the alphabet characters and combinations which have separate shorthand braille symbols *(such as `ar`, `ch`, etc...)*.

2) `contractions` contains complete words which can be abbreviated into simpler combinations of braille cells. For instance, `child` can be represented by the same symbol as `ch` in English.

3) `specialCharacters` contains braille indicators and special symbols such as `@` or `[`. 
Indicators are built-in with *special variable* representations like `%capital` or `$emph`. 
There is a difference between the `%` and the `$` variables: The `%` are automatically handled by the translation system *(i.e. if a letter is capital)*, but the `$` cannot because they are usually font-related *(i.e.: italic letters)*.

Check out the `languages/english.py` file for example.
For more details please refer to the `docs/Language File Structure.txt` file.

## System Semantics
If the language supports Grade-2 translation, the program supports it. 

Moreover, the output of the translation is a list which has the following format:

`[[u'110000', u'111010', u'111000']]   # This means "braille" in Grade-2 Translation`

Each list represents one word, and each string in that sublist is a Braille cell. The following image shows the corresponding position in the cell:


![cell representation](https://raw.github.com/ant0nisk/pybrl/master/GithubContent/cell_repr.png)

If a cell character is a 1, then the corresponding dot in the cell is filled:

  
![cell representation example](https://raw.github.com/ant0nisk/pybrl/master/GithubContent/cell_repr_example.png)


Note that in the language files, the following cell representation is valid:

`'000010001110'`

which can be used if a character or symbol uses more than one cell to be represented in Braille *(in this example it uses 2 cells)*. 

The translator will automatically split the cells into segments of 6 characters, so the output of the system is consistent.

## Jupyter Notebooks for example usage:
In the `docs/Samples` directory, I have some Jupyter Notebooks with example usage of `pybrl`. Going through them is a great way to learn the tool and how it works.

* [Translate PDF files and create new ones using `pybrl` and LaTeX](docs/Samples/pdf_translation/Notebook.ipynb)
* [Learn how data is formated within `pybrl`](docs/Samples/nemeth_integration/Notebook.ipynb)

## TODO
See the `docs/TODO.txt` file for an updated list.

## Contributors Needed
##### What is missing?
- The Nemeth code is not integrated yet. Specifically it needs: 
   - Convert the keys in `nemeth.dict` file to be used within pybrl.
   - Complete the Logic that handles the Nemeth code translation

- A solid way to convert files such as PDFs or Word Documents into a plain format that can be used in the program. Thoughts on how to do this so far:

  1) Convert the Document pages into Images.

  2) Use/Integrate tools such as [PDFMiner](https://github.com/euske/pdfminer) to extract text and images *(it is useful that it provides information about the position of the text)*

  3) Use an OCR-based method to analyze Equations. There will be exclusive preprocessing of the Equations to first convert it into MathML *(which can already be parsed by pybrl)*.

##### How to contribute if you are a Developer?
If you want to contribute in this project, please do so by opening a Pull request.

If you are motivated and want to help developing this project, please send me an email at antonis.katzourakis (I use gmail). 

##### How can you help if you are not a Developer?
1) Add a new Language File:
  Check out the existing language files (under the `languages` directory) and read the instructions in the **How to import a new Language** part of this README. You will find a sample language file to start in the `docs` directory.

2) Add more Contractions in the Language Files:
  You can edit the language files, and add more contractions in the corresponding dictionary. 
  Right now, only a few are listed, but there are many more that will be added. 
 Check it out and see how easy it is in the `languages/english.py` file.


## How this project started?
A mathematician friend of mine works at a school which is located in a remote village in Crete, Greece. A student of hers is blind. Since the facilities of the school are limited, I was trying to find an affordable Braille printer for him. The programs that the specific school has are really limited. If Greek and Math are combined into one piece of text, the Braille that is printed is unreadable. On top of that, the printer that is available is quite old and thus has a lot of problems. I soon figured out that most machines cost 2000$ or more. I decided to build a printer for him. Having almost no experience with Braille, I researched on how it works and how these printers work. However, I first needed to find a complete translation program, which supports at least English, Greek and Mathematics. Most programs *(either commercial or non-commercial)* that are available right now are either not complete, or expensive *(usually they are both)*. 

The first days of this project were a reality-check: *We take things for granted and these people are not taken into account for many things in this world.* I don't want to go into detail about the handling of blind students in Greece, but I will only mention that they are completely unable to do the National exams on the last grade of Highschool, because the Ministry of Education in Greece forbids the translation of the exams into Braille. Moreover, the Math books that these students get, have all the exercises omitted, on the justification that "they need to be done under a teacher's supervision". This is just not the way to go.

This is just an example why the world needs a complete Braille translation program and affordable Braille printers. 

## Where does this project go?
This program will be integrated on an open-source Braille printer.
I haven't started designing it yet, since the correct translation of documents is most important. The main idea is that any document will be translated on the printer, giving the ability of the blind to translate any digital document themselves.

## Notes: 
 - The Language detection works great, but it can fail on similar languages (i.e. German and Dutch). However, such languages usually share the same Braille alphabet, so there is really low chance of failure. **Remember** to check if the translated text is correct though - I hadn't any occurrencies of bad translations, but I cannot guarantee that.
 - Math is not ready yet. There is a lot of work to do there...

## Unit tests
In the `tests` directory, I include unit tests for different functionalities of pybrl. You can run them individually or all of them by:

```bash
python test_all.py
```

## License
pybrl is licensed under GNU-GPL. You can find a copy of the license in this repository. [What does that mean?]( http://choosealicense.com/licenses/gpl-3.0/)
