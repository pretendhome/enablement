# Calibration Exemplars — RIU-026: Hybrid Similarity (Enums + Embeddings)

## Dimension 1: Hybrid Scoring

### Insufficient
"We have implemented a hybrid similarity system that combines enum-based exact matching with embedding-based semantic matching. The scoring does not appropriately weight exact matches vs semantic similarity."

This submission implements a hybrid similarity system but does not appropriately weight exact matches vs semantic similarity. It is superficial and does not provide a robust solution.

### Basic
"We have implemented a hybrid similarity system that combines enum-based exact matching with embedding-based semantic matching. The scoring includes basic weighting but is not well-tuned."

This submission implements a hybrid similarity system with basic weighting but lacks tuning. It is not comprehensive.

### Competent
"We have implemented a hybrid similarity system that combines enum-based exact matching with embedding-based semantic matching. The scoring appropriately weights exact matches vs semantic similarity with tunable parameters."

This submission implements a hybrid similarity system with appropriate weighting and tunable parameters. It provides a robust solution.

### Expert
"We have implemented a hybrid similarity system that combines enum-based exact matching with embedding-based semantic matching. The scoring appropriately weights exact matches vs semantic similarity with tunable parameters. Additionally, we have included mechanisms for updating the scoring based on feedback and performance data, ensuring continuous improvement."

This submission goes beyond competent by including mechanisms for updating the scoring based on feedback and performance data. It demonstrates a deep understanding of hybrid scoring and its continuous improvement.

## Dimension 2: Performance

### Insufficient
"We have implemented a hybrid similarity system. The retrieval does not meet the latency budget and does not include tiering between fast and semantic paths."

This submission implements a hybrid similarity system but does not meet the latency budget or include tiering. It is superficial and does not provide a robust solution.

### Basic
"We have implemented a hybrid similarity system. The retrieval meets the latency budget for some queries but not all. The tiering between fast and semantic paths is basic."

This submission implements a hybrid similarity system that meets the latency budget for some queries but lacks comprehensive tiering. It is not robust.

### Competent
"We have implemented a hybrid similarity system. The retrieval meets the latency budget with appropriate tiering between fast and semantic paths."

This submission implements a hybrid similarity system that meets the latency budget with appropriate tiering. It provides a robust solution.

### Expert
"We have implemented a hybrid similarity system. The retrieval meets the latency budget with appropriate tiering between fast and semantic paths. Additionally, we have included mechanisms for updating the performance strategies based on feedback and performance data, ensuring continuous improvement."

This submission goes beyond competent by including mechanisms for updating the performance strategies based on feedback and performance data. It demonstrates a deep understanding of performance and its continuous improvement.

## Dimension 3: Service Evaluation

### Insufficient
"We have evaluated vector database services. The evaluation is basic and does not include production-relevant benchmarks or cost analysis."

This submission evaluates vector database services but lacks production-relevant benchmarks and cost analysis. It is superficial and does not provide a comprehensive solution.

### Basic
"We have evaluated vector database services. The evaluation includes some production-relevant benchmarks but lacks comprehensive cost analysis."

This submission evaluates vector database services with some production-relevant benchmarks but lacks comprehensive cost analysis. It is not comprehensive.

### Competent
"We have evaluated vector database services with production-relevant benchmarks and cost analysis."

This submission evaluates vector database services with production-relevant benchmarks and cost analysis. It provides a comprehensive solution.

### Expert
"We have evaluated vector database services with production-relevant benchmarks and cost analysis. Additionally, we have included mechanisms for updating the service evaluation based on feedback and performance data, ensuring continuous improvement."

This submission goes beyond competent by including mechanisms for updating the service evaluation based on feedback and performance data. It demonstrates a deep understanding of service evaluation and its continuous improvement.

## Dimension 4: Edge Case Handling

### Insufficient
"We have implemented a hybrid similarity system. The system does not handle edge cases where enum matching and embedding matching disagree."

This submission implements a hybrid similarity system but does not handle edge cases where enum matching and embedding matching disagree. It is superficial and does not provide a robust solution.

### Basic
"We have implemented a hybrid similarity system. The system includes basic handling for edge cases where enum matching and embedding matching disagree."

This submission implements a hybrid similarity system with basic handling for edge cases but lacks comprehensive resolution rules. It is not robust.

### Competent
"We have implemented a hybrid similarity system. The system handles edge cases where enum matching and embedding matching disagree with clear resolution rules."

This submission implements a hybrid similarity system that handles edge cases with clear resolution rules. It provides a robust solution.

### Expert
"We have implemented a hybrid similarity system. The system handles edge cases where enum matching and embedding matching disagree with clear resolution rules. Additionally, we have included mechanisms for updating the edge case handling based on feedback and performance data, ensuring continuous improvement."

This submission goes beyond competent by including mechanisms for updating the edge case handling based on feedback and performance data. It demonstrates a deep understanding of edge case handling and its continuous improvement.