# Introduction to Bioinformatics

This is a textbook that accompanies a master's course Introduction to Bioinformatics tought by Blaž Zupan and Tomaž Curk and assited by Pavlin Poličar and Martin Špendl at University of Ljubljana.

## Chapter files

[`main.tex`](main.tex): front matter

[`c-molbio.tex`](c-molbio.tex): Introduction to Molecular Biology  
  - Overview of concepts of life, cells, proteins, amino acids, and metabolism.  
  - Sets up key questions and introduces the central dogma as the unifying framework.

[`c-history.tex`](c-history.tex): Central Dogma of Molecular Biology  
  - Explains DNA→RNA→Protein information flow and why it matters.  
  - In short, revies history of discoveries that led to modern molecular biology.

[`c-genome.tex`](c-genome.tex): Genomes and Some Simple Sequence Patterns  
  - Introduces DNA sequences and some simple methods to assess their basic statistical properties.
  - Uses viral genomes to illustrate practical mining sequence features with Python programming.

[`c-genes.tex`](c-genes.tex): Where Are the Genes?  
  - Covers reading frames, gene structure, ORFs, and gene prediction basics.  
  - Compares simple statistical models to real gene architectures and discusses scoring and evaluation.
  - Introduces permutation-based analysis.

[`c-alignment-m.tex`](c-alignment-m.tex): Sequence Alignment Methods  
  - Introduces alignment scoring, dynamic programming, and algorithms for global and local alignment.
  - Extends to alignment with affine gap penalties and multiple sequence alignment.
  - Discusses protein-specific scoring and inference of scoring tables.

[`c-alignment-t.tex`](c-alignment-t.tex): Sequence Alignment Tools  
  - Discusses about various applications of alignment tools.
  - Introduces BLAST and CLUSTAL and provides basic understanding of methods behind these techniques.
  - Shows some typical examples of use.

## Helper files

[`split-to-chapters.py`](split-to-chapters.py) splits main.pdf to chapters, creatings one pdf file for each chapter.

[`copy-to-server`](copy-to-server) is a bash script that copies pdfs of each chapter to the file server