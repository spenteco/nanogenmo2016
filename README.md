# nanogenmo2016

This is a variation on the Oulipo N+7 substitution scheme.  However, instead replacing nouns with with "next seventh" noun in the dictionary, I'm replacing nouns, proper nouns, adjectives and verbs (with a small number of exceptions) with one of several (usually one of 10 or 15) similar words derived from a word vector representation derived from the Project Gutenberg corpus.  I also try to coordinate substitutions in texts with substitutions in a corresponding set of summaries, and to maintain author name changes across texts.  Outputs are pdfs and "page flipper" web displays for both the texts and a catalog built from the collected summaries.

For the finished product, please see [the project page on my website (http://robineggsky.com/posts/momogenmo.html).

# Data preparation

A couple of years ago, I downloaded Project Gutenberg's english texts (~40,000) and removed most, but not all, of the PG header and footer boilerplate (a few vagrant lines remain).  If you'd like a copy of this data, please open an issue, and I'll see what I can do to make a copy available.

Code for deriving distances from word vectors can be found in the folder fasttext_related.  First, I ran clean_text_folder.py, which takes as input a folder of texts (~40,000 PG texts in my case) and outputs a single, very large file consisting of space-delimited part-of-speech tagged words; "I saw the cat.  I saw the the dog" is changed into "i_prp saw_vbn the_dt cat_nn i_prp saw_vbn the_dt cat_nn".  Then I ran [fastText](https://github.com/facebookresearch/fastText), Facebook's equivalent to the much more well known word2vec from Google.  I used all the default settings, except that I included only words which occurred 25 times or more.  The resulting vector file was also huge.  To compute distances from the vector file, I ran ComputeDistances.java, which ran for several days, and also resulted in a gigantic file, although one that I could actually load on the pathetic workstation I have at home (I have got to get a new computer!).

The last data preparation chore involved preparing my_digest.xml, which can be found in folder data/reference_data.  This file contains entries extracted from the not so terrible  OCR data from [The Reader's Digest of Books](https://archive.org/details/readersdigestofb008871mbp).  At the same time, I prepared a catalog which served as a cross-reference (see data/reference_data/129.catalog.ods, which a sample of the format).  This took quite a bit of time; however, it's rather soothing (copy, paste, repeat), and it was a welcome relief on election night.

You might note that data/reference_data/my_digest.xml contains way more entries than I'm actually using.  Until quite late in the month, this project was building 675 texts, which seemed like an awesome idea at the time, but which proved too much once I had built a web page for linking to the results.

# Running the code

Except for the one bit of java, it's all python.  To generate the texts:

> ./generate_novels.py

Occasionally, the author names and titles don't work quite right.  To identify problems:

> ./check_author_names.py
> ./check_titles.py

Lastly:

> ./assemble_digest.py
> ./create_index_table.py

Open pageflipper/index.html in Firefox, and you should be good to go.  To see the catalog, open pageflipper/catalog.html.

I've included enough data to build one text (Cowper's *The Task*) from the git repo.

The list of dependencies is quite long: fastText and Java (see "Data preparation", above); plus lxml, TextBlob, Mako templates, and ftfy.  The project also requires pdflatex, pdfnup, and pdftohtml).  The page flipper function is provided by [turn.js](http://www.turnjs.com/).

I've also included a number of shell scripts for rerunning parts of the process at different starting points.  generate_novels.py is pretty good about not doing anything it has already done, so rerunning part of the process for a text is a matter of deleting the files that need to be replaced.

The geekiest part of this is the process of building texts for the pageflipper.  Latex is created from the document, then the latex is converted to PDF.  XML is extracted from the PDF via pdftohtml, then the XML is converted to SVG, which actually becomes the backgrounds for the pages displayed in the pager flipper.  Why? Let latex to the bookish page layout stuff.

# Issues, do-overs, etc

I have encoding problems in my Gutenberg data, problems that I didn't realize were there.  ftfy fixed some of them, but not all of them.  This is my most substantial, long-term, and unresolved issue.

Greek--ancient greek, I think, although I don't have greek--was a complete pain in pdflatex, especially since I'm not willing to mark up texts by hand.  I think my problem is that fontenc commands aren't working like I expect them to.  No matter what I do, pdflatex keeps looking in the OT1 font set.  To get this done, I dropped problem texts from the collection, which I'm not happy about, since I ended up dropping Burton's *The Anatomy of Melancholy*, which promised to be a lot of fun.

I could go on and on about how the general lack of structure in PG texts makes nearly impossible the identification of chapter headings, the determination of appropriate page breaks, the differentiation of prose from verse, etc.

Lastly, I'm not sure this project's code is all that well organized.  I learned to organize code decades ago on IBM mainframes, and now I do most of my substantial work inside one framework or another, where the framework imposes organization.  But on something free-form like this, I'm clueless.  If someone knows where I can go to learn this, please drop me a line.



