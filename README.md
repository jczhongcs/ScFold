# 1.Introduction
In the realm of protein design, the efficient construction of protein sequences that accurately fold according to predefined structure has emerged as a significant area of research. 
Research on long-chain proteins has made significant advancements, however, the design of short-chain proteins also warrants considerable attention. Key objectives in this field include enhancing model recovery rates, improving generalization, and reducing perplexity. In this study, we present ScFold, a novel model that features an innovative node module. 
This module utilizes spatial reduction and positional encoding mechanisms, which enhance the extraction of structural features, thereby improving recovery rates.Experiments reveal that ScFold achieves a recovery rate of 52.22$\%$ on the CATH4.2 dataset, with good performance on single chains, reaching a recovery rate of 41.6$\%$. Additionally, perplexity for short and single chains is reduced to below 6. 
ScFold also demonstrates enhanced recovery rates of 59.32$\%$ and 61.59$\%$ on the TS50 and TS500 datasets, respectively.
# 2.Overall Framework
We illustrates the entire ScFold framework, where the input is the protein structure and the output is the protein sequence expected to fold into the input structure. We introduce a novel node module within the model, 
featuring parallel attention mechanisms, complemented by edge and global modules to enable multi-scale learning of residue features. 
Compared to previous graph models, ScFold can generate amino acid sequences from the protein structure in a single pass, achieving a higher recovery rate. 
