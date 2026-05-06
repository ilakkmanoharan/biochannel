White Paper 1: Single-Cell RNA Sequencing (scRNA-seq)
Quantifying Cellular State Through Transcriptomic Measurements
Abstract
Single-cell RNA sequencing (scRNA-seq) enables the measurement of gene expression at the resolution of individual cells. This technology reveals the heterogeneity of cellular populations, captures transient biological states, and allows reconstruction of dynamic processes such as differentiation, stress response, and disease progression.
1. Biological Basis
Cells regulate function through gene expression—the process by which DNA is transcribed into RNA and translated into proteins. Messenger RNA (mRNA) abundance reflects the regulatory state of the cell.
However, gene expression is:
Stochastic (noisy) due to transcriptional bursting
Context-dependent (environment, signaling inputs)
High-dimensional (thousands of genes per cell)
Thus, each cell can be viewed as a point in a high-dimensional gene expression space.
2. Measurement Principles
scRNA-seq involves:
Isolation of individual cells
Reverse transcription of RNA → cDNA
Amplification and sequencing
Mapping reads to genes
Output:
A gene expression matrix
Rows: genes
Columns: cells
Values: counts (UMIs or reads)
3. Statistical Properties of the Data
scRNA-seq data exhibits:
Sparsity (dropout events): many zero counts due to detection limits
Overdispersion: variance exceeds mean (negative binomial distribution)
Technical noise: sequencing depth, amplification bias
These properties require specialized statistical models.
4. Biological Interpretation
Each cell’s expression profile reflects:
Cell type identity
Functional state
Response to stimuli
Position along a biological trajectory
Clustering reveals:
Distinct cell populations
Subpopulations under stress or disease
5. Dynamics and Trajectories
Cells transition between states over time. scRNA-seq captures snapshots that can be ordered using:
Pseudotime inference
Manifold learning
This enables reconstruction of:
Differentiation pathways
Stress responses
Adaptive decision processes
6. Scientific Significance
scRNA-seq allows:
Discovery of new cell types
Mapping of developmental processes
Understanding of cellular heterogeneity in disease
It transforms biology from population averages to single-cell resolution systems science.