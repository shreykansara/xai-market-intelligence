# Stage 3: 11-D Strategic Vector Projection & DB Export Engine

Takes filtered news records from Stage 2, computes intermediate 768-D contextual text embeddings, projects them into **11-D PESTLE & Porter's 5 Forces scores** via our pre-trained Linear Projection Matrix model ($\mathbf{W} \in \mathbb{R}^{768 \times 11}, \mathbf{b} \in \mathbb{R}^{11}$), **DISCARDS the heavy 768-D text embedding vector**, and outputs only the clean **11-D strategic vector + metadata** ready for database ingestion!

## Key Features

1. **Microsecond Projection**: Uses matrix multiplication ($\mathbf{y} = \text{clip}(\mathbf{x} \cdot \mathbf{W} + \mathbf{b}, 0.05, 0.95)$) to generate 11-D vectors instantly without LLM bottlenecks.
2. **768-D Embedding Strip**: Discards heavy text vectors to save **80%+ storage space** while retaining full strategic business signal.
3. **Strategic Impact Thresholding**: Filters out stories with low impact scores ($\text{impact} < 0.25$).

## Usage

```bash
# Process Stage 2 filtered news into clean 11-D strategic vectors
python enrich_and_store.py --input ../stage2_filter/filtered_news_202608.csv --output enriched_11d_news_202608.csv
```

## Output Schema

* `id`: Unique record identifier (`gdelt_YYYYMMDD_e...`).
* `date`: News publication date (`YYYY-MM-DD`).
* `headline`: Clean article headline.
* `strategic_embedding`: **11-Dimensional Strategic Vector** `[Political, Economic, Social, Technological, Legal, Environmental, Threat of New Entrants, Buyer Power, Supplier Power, Threat of Substitutes, Competitive Rivalry]`.
* `source_link`: Source article URL.
* `location_affected`: Location tag (`LPU`, `Kapurthala`, `Punjab`, `India`, `World`).
* `impact_score`: Strategic business impact score (`0.00` to `1.00`).
