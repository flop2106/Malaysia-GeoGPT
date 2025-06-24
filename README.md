# Malaysia GeoGPT

Malaysia GeoGPT is a research assistant chatbot built with Python focused on Malaysian geology. It scrapes academic paper abstracts from Universiti Malaya (UM) and Universiti Teknologi PETRONAS (UTP), embeds them using OpenAI models and stores the vectors in SQLite for quick retrieval. Ask natural-language questions and the bot returns the most relevant snippets so you can jump straight to analysis.

## Features
- **Automated scraping** of UM & UTP RSS feeds for geology papers
- **OpenAI embeddings** stored in a SQLite vector store with cosine similarity search
- **Flask chat API** that summarizes retrieved abstracts using a RAG-style approach
- **Kafka message queue** connects scraping and embedding steps for stability

## Architecture
1. **Web scraper** → collects abstracts from UM & UTP
2. **Kafka queue** → hands data to the embedding worker
3. **Embedding layer** → generates vector embeddings with OpenAI
4. **SQLite + cosine similarity** → provides vector search
5. **Flask chat API** → serves answers (frontend coming soon)

### Why message queue instead of pub/sub?
Using Kafka consumer groups introduced rebalancing delays and offset issues. By assigning partitions directly and using a queue style, ingestion is steady without rebalancing overhead.

## Roadmap
- Swap SQLite for Postgres + pgvector
- Replace OpenAI with HuggingFace when credits run out
- Expand sources: full papers, Wikipedia, Geoscience Malaysia
- Launch a simple frontend and public demo

Malaysia GeoGPT aims to remove the grunt work of locating papers so researchers can focus on geological interpretation and insight.


Built with OpenAI, SQLite and Kafka.

