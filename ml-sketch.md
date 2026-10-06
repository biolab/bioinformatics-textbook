# Machine Learning on Sequence Data

## Introduction

- In the previous chapter we used data on sequences for construction of phylogenetic trees.
- Phylogenetic trees can visually present relations, evolution, and diversification of species, and are indeed core methods to do so in bioinformatics.
- The primary data to assess similarities between observed entities is through sequence alignment, which also provides the instrument to explore the function of characteristic subsequences (motifs) and explanations in the form of where the sequences stayed untouched and which parts were more prone to mutations.
- While the sequences are today primary source of information for phylogeny analysis, other information, like morphological traits, can be a source of characterizing taxa and assessing similarity.
- There is more: we can use this type of data for other models that compare the traits quantitatively or visually (e.g. clustering), predict their qualitative or quantitative characteristics (e.g. classification or regression), and relate them to any type of phenotype (... state if there is anything more to say here). Lately, all these are done through modelling by machine learning. And interestingly, to fully close the circle, machine learning techniques can be used to address the raw data directly, giving rise to numerical characterization of sequences (profiling), that can also be used for phylogeny instead of using classical techniques for sequence alignment.
- There is much in this field, but our journey will be short, as we are only hinting about different approaches and possibilities. Let us start with an example, though.

## Data

- For an example, we have collected mitochondrial 12S rRNA gene sequences from different species. The 12S rRNA gene is part of the DNA found inside mitochondria, the tiny structures in cells that produce energy. This gene helps build the small part of the mitochondrial ribosome, which is needed to make proteins. Because this gene changes very slowly over time, biologists can compare it between different species to study how they are related.
- The 12S gene evolves slowly enough to compare across distant species but fast enough to distinguish close ones, and it is often used in phylogeny analysis.
- The mitochondrial genome is especially useful for this kind of work because it is small, passed down only from the mother, and does not mix or shuffle like regular (nuclear) DNA. This makes it easier to follow how species have evolved and to build family trees showing their shared ancestry.
- We gathered the data on about fifteen mammals, including humans, chimpanzees, gorillas, orangutans, mice, rats, dogs, cats, cows, pigs, and horses. The collection also includes several birds such as chickens, pigeons, ducks, turkeys, ravens, and sparrows, as well as a variety of fish including zebrafish, salmon, trout, cod, tuna, and carp. In addition, we included some reptiles such as turtles, pythons, alligators, and anoles, and a few amphibians such as frogs, newts, and axolotls.
- We stored the data in a FASTA file, of which we are here showing only few heading lines and showing only the start of the sequence. The 12S sequences for these organisms vary in length, with average length around 965, with min length of 928 for axolotl and maximal length of 1283 for European anchovy.

```
>Homo_sapiens|taxid:9606|acc:NC_013993.1|common_name:human|type:mammal
AATAGGTTTGGTCCTAGCCTTTCTATTAGCTCTTAGTAAGATTACACATGCAAGCAT (894 more)
>Pan_troglodytes|taxid:9598|acc:NC_001643.1|common_name:chimp|type:mammal
AACAGGTTTGGTCCTAGCCTTTCTATTAGCTCTTAGTAAGATTACACATGCAAGCAT (889 more)
>Sus_scrofa|taxid:9823|acc:NC_039090.1|common_name:pig|type:mammal
CACAGGTTTGGTCCTGGCCTTTCTATTAGTTCTTAATAAAATTACACATGCAAGTAT (898 more)
>Salmo_salar|taxid:8030|acc:NC_001960.1|common_name:atlantic_salmon|type:fish
CAAAGGCTTGGTCCTGACTTTACTATCAGCTCTAACTGAACTTACACATGCAAGTCT (886 more)
>Passer_domesticus|taxid:9157|acc:NC_040875.1|common_name:sparrow|type:bird
AAAGACTTAGTCCTAACCTTACTGTTGGTTTTTGCTAGATTTATACATGCAAGTATC (920 more)
>Lithobates_catesbeianus|taxid:8407|acc:NC_042226.1|common_name:bullfrog|type:amphibian
TAAAGGTTTGGTCCTGGCCTTATTATCAACTGTTTCCCAACTTACACATGCAAGTCT
(871 more)
```

- We consider the sequence data of the mitochondrial 12S rRNA gene. It is a short, conserved part of the mitochondrial genome that helps make ribosomes inside mitochondria.

## Sequence Alignment and Distance Estimation

We aligned the sequences using the Needleman–Wunsch global alignment algorithm, and scored the alignments using affine gap penalty scoring with 1 for a match, −1 for a mismatch, −2 for gap opening, and −0.5 for gap extension. We computed distances by normalizing each pairwise alignment score ($S(a,b)$) by the larger of the two self scores ($S(a,a)$) and ($S(b,b)$), and defining the distance as

$$
\text{distance}(a,b) = 1 - \frac{S(a,b)}{\max(S(a,a), S(b,b))},
$$

so that identical sequences have a distance of 0 and more divergent sequences have larger positive values.

This produces the distance matrix of the type:

|         | human   | chimp   | gorilla | orangutan | macaque |
|---------|---------|---------|---------|-----------|---------|
| human   | 0.000   | 0.093   | 0.095   | 0.170     | 0.317   |
| chimp   | 0.093   | 0.000   | 0.091   | 0.183     | 0.313   |
| gorilla | 0.095   | 0.091   | 0.000   | 0.164     | 0.316   |
| orangutan | 0.170 | 0.183   | 0.164   | 0.000     | 0.342   |
| macaque | 0.317   | 0.313   | 0.316   | 0.342     | 0.000   |

## Neighbor Joining

- We used ... to infer phylogeny tree. Fig... is one possible visualization of results, showing the procedure makes sense and the results are interpretable. We can see that human is close to ..., birds are indeed related to each other, mice is close to rat, and dolphin groups with mammals and not fish.

## Visualizing Distance Data

- There are a wealth of other visualization approaches that can start with distance data and have been recently (and not so recently) developed within the field of statistics and data science.
- Of these, the most prominent historically important approach is multi-dimensional scaling. (.. brief description)
- A possible problem of MDS is that by trying to preserve all the distances, its Frobenius norm actually focuses on preserving the relations between taxa that are far apart.
- If we are aiming in finding related groups, a newer, alternative approach is t-SNE, which ... In bioinformatics, another alternative is UMAP, recently much more used than t-SNE, but somehow unjustified as it has been shown that t-SNE scales better and that with appropriate setting it is in result very similar to UMAP.
- Fig. ... shows t-SNE visualization of our distance data obtained by alignment scoring.

## k-Mer-Based Profiling

- Let us now move away from alignment-based approaches.
- We will profile sequences with k-mers (show an example sequence and k-mers) and represent the sequences with frequencies.
- We can now use this presentation to measure sequence similarities. A common approach is to use cosine distances (different from Euclidean distances, this one escapes the curse of dimensionality), and then use any of the above techniques for phylogeny analysis or group discovery, say clustering.

## Predictive Modelling

- Apart from phylogeny analysis, we can use sequences for predictive modelling, where the two most prominent approaches are classification and regression. In classification, models learn to assign sequences to predefined categories, such as identifying genes versus non-coding regions, predicting protein families, or distinguishing pathogenic from non-pathogenic strains. In regression, models predict continuous biological properties, such as binding affinity, gene expression level, or enzyme stability, allowing quantitative estimation of functional or environmental adaptations from sequence variation.
- A side note: we could also start with distance matrices and do predictive modelling based on this (kNN, SVM), but we would then much restrain the methods we could use as most machine learning approaches start with feature-based presentation, and more importantly, we would actually like to expose the features that are most influential in our predictions: the result is not only a model but also understanding its structure and semantics possibly leading to new discoveries in molecular biology.
- An example with logistic regression and classification to organism groups (mammals, fish, birds).
- We can extend logistic regression to more complex models, using neural networks.

## Learning Representations from Sequences

- Instead of some label, we can use the characterized part of the sequence to predict its next symbol, or k-mer.
- We use neural network, with the last layer of softmax (essentially logistic regression).
- Since we are not really interested in prediction of sequences, we use the resulting model through sequence encoding at the penultimate layer. We hope that this encoding presents sufficient semantics for all other machine learning and clustering tasks.

### Motivation / Transition

- So far we used explicit features (alignment scores, k-mer frequencies).
- Modern machine learning can *learn* these features automatically from raw sequences.
- This is done by predicting missing or next symbols — an idea borrowed from natural language processing.

### Analogy to Text Data

- In text, words appearing in similar contexts have similar meanings.
- In DNA or protein sequences, subsequences (k-mers) that occur in similar biological contexts likely have similar roles or functions.

### word2vec Model

- Introduce briefly: predicts a word based on its context (CBOW) or predicts surrounding words from a word (Skip-gram).
- Produces low-dimensional vector embeddings that capture semantic relationships.
- Input: tokenization to k-mers.

### dna2vec and Bioseq Adaptations

- Extends word2vec to biological sequences by treating k-mers as "words."
- Embeddings capture sequence similarity, motif patterns, and functional context.
- Resulting vectors can be averaged or pooled to represent entire genes or genomes.

## More Advanced ML Models

### Motivation / Transition

- dna2vec learns fixed embeddings from local context (limited window).
- To capture longer-range dependencies and complex sequence patterns, we need models that process sequences directly.
- Neural networks provide flexible architectures for this.

### Convolutional Neural Networks (CNNs)

- Explain 1D convolutions on sequences: local filters detect motifs and short dependencies.
- Pooling layers summarize detected motifs across sequence length.
- Useful for motif discovery, promoter prediction, splice site detection, etc.
- Fast and parallelizable — good for fixed-length inputs.

### Recurrent Neural Networks (RNNs)

- Capture sequential order and longer dependencies.
- Introduce LSTM and GRU variants for handling long-term information.
- Applications: gene expression prediction, sequence classification, signal peptide detection.

### Attention and Transformers

- Attention mechanisms learn which parts of a sequence are most relevant for predicting others.
- Transformers (like DNABERT, ESM) learn context-dependent embeddings for every position.
- Pretrained models can be fine-tuned for specific bioinformatics tasks.

### Comparison / Summary

- CNNs → capture local motifs
- RNNs → capture sequence order and context
- Transformers → capture global context efficiently
- All enable *end-to-end learning* from raw sequence to prediction.
