from typing import List, Dict, Any, Optional, Union
import faiss
import torch
import pickle
from sentence_transformers import SentenceTransformer
from transformers import (
    AutoTokenizer,  
    AutoModelForSequenceClassification,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class EnhancedLectureRAG:
    def __init__(
        self, 
        embedder_name: str = 'BAAI/bge-large-en-v1.5', 
        chunk_size: int = 1000,
        retrieval_strategy: str = 'hybrid',
        reranking_model: Optional[str] = 'cross-encoder/ms-marco-MiniLM-L-6-v2'
    ):
        """
        Advanced Retrieval-Augmented Generation system with flexible strategies.
        
        Args:
            embedder_name (str): Embedding model for text representation.
            chunk_size (int): Text chunk size for processing.
            retrieval_strategy (str): Retrieval method ('semantic', 'keyword', 'hybrid').
            reranking_model (str, optional): Model for re-ranking retrieved results.
        """
        # Model components
        self.text_embedder = None
        self.reranking_tokenizer = None
        self.reranking_model = None
        
        # Indexing and retrieval components
        self.vector_index = None
        self.keyword_index = {}
        self.chunks = []
        
        # Configuration parameters
        self.embedder_name = embedder_name
        self.chunk_size = chunk_size
        self.retrieval_strategy = retrieval_strategy
        
        # Initialize models and strategy
        self._load_models(reranking_model)
    
    def _load_models(self, reranking_model: Optional[str] = None):
        """
        Load embedding and reranking models with flexible configuration.
        """
        try:
            # Text embedding model
            self.text_embedder = SentenceTransformer(
                self.embedder_name, 
                device='cuda' if torch.cuda.is_available() else 'cpu'
            )
            
            # Optional reranking model
            if reranking_model:
                self.reranking_tokenizer = AutoTokenizer.from_pretrained(reranking_model)
                self.reranking_model = AutoModelForSequenceClassification.from_pretrained(reranking_model)
                
                # Move to GPU if available
                if torch.cuda.is_available():
                    self.reranking_model = self.reranking_model.cuda()
        
        except Exception as e:
            print(f"Model loading failed: {e}")
            raise
    
    def _retrieve_semantic(
        self, 
        query: str, 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Pure semantic retrieval using vector embeddings.
        """
        query_embedding = self.text_embedder.encode([query])
        distances, indices = self.vector_index.search(query_embedding, top_k)
        
        return [
            {
                'chunk': self.chunks[idx],
                'semantic_score': 1 / (1 + distances[0][i])
            } for i, idx in enumerate(indices[0])
        ]
    
    def _retrieve_keyword(
        self, 
        query: str, 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Keyword-based retrieval using simple matching.
        """
        # Basic keyword matching 
        return [
            {
                'chunk': chunk,
                'keyword_score': sum(1 for word in query.lower().split() if word in chunk.lower())
            } 
            for chunk in self.chunks
        ][:top_k]
    
    def advanced_retrieval(
        self, 
        query: str, 
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Hybrid retrieval strategy with multiple approaches.
        """
        # Semantic retrieval as base
        semantic_results = self._retrieve_semantic(query, top_k * 2)
        return semantic_results
        # keyword_results = self._retrieve_keyword(query, top_k * 2)
        
        # # Combine and re-rank results
        # hybrid_results = []
        # for sem_result in semantic_results:
        #     for kw_result in keyword_results:
        #         if sem_result['chunk'] == kw_result['chunk']:
        #             combined_score = (
        #                 sem_result['semantic_score'] * 0.7 + 
        #                 kw_result['keyword_score'] * 0.3
        #             )
        #             hybrid_results.append({
        #                 **sem_result,
        #                 'hybrid_score': combined_score
        #             })
        
        # # Sort by hybrid score
        # hybrid_results.sort(key=lambda x: x['hybrid_score'], reverse=True)
        
        # # Optional reranking
        # return self._rerank_results(query, hybrid_results[:top_k])
    
    def _rerank_results(
        self, 
        query: str, 
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Advanced result re-ranking with improved error handling.
        """
        # If no reranking model, return original results
        if not self.reranking_model:
            print("Warning: No reranking model available. Returning original results.")
            return results
        
        reranked_results = []
        try:
            for result in results:
                # Prepare input for reranking model
                inputs = self.reranking_tokenizer(
                    query, 
                    result['chunk'], 
                    return_tensors='pt', 
                    truncation=True, 
                    max_length=512
                )
                
                # Move inputs to GPU if available
                if torch.cuda.is_available():
                    inputs = {k: v.cuda() for k, v in inputs.items()}
                
                # Get reranking score with error handling
                with torch.no_grad():
                    outputs = self.reranking_model(**inputs)
                    # Safely extract score
                    score = torch.softmax(outputs.logits, dim=1)[0][1].item()
                    
                    result['reranked_score'] = score
                    reranked_results.append(result)
        
        except Exception as e:
            print(f"Error in reranking: {e}")
            # Fallback to original results if reranking fails
            return results
        
        # Sort by reranked score if results exist
        return sorted(reranked_results, key=lambda x: x['reranked_score'], reverse=True) if reranked_results else results
    
    def build_vector_database(
        self,
        documents: Union[str, List[str]],
        database_path: str,
        append: bool = False,
    ) -> None:
        if not self.text_embedder:
            self._load_models()

        if isinstance(documents, str):
            documents = [documents]

        processed_chunks = []
        for doc in documents:
            chunks = self.advanced_text_splitter(doc, chunk_size=self.chunk_size)
            processed_chunks.extend(chunks)

        embeddings = self.text_embedder.encode(processed_chunks)

        # Load existing database or create new one
        if not os.path.exists(database_path):
            dimension = embeddings.shape[1]
            self.vector_index = faiss.IndexFlatIP(dimension)
            print("Created a new FAISS index.")            
            self.vector_index.add(embeddings)
            self.chunks.extend(processed_chunks)
        else:
            with open(database_path, "rb") as f:
                existing_data = pickle.load(f)
                self.vector_index = existing_data["vector_index"]
                self.chunks = existing_data["chunks"]
                print("Loaded existing database.")
            if append:
                self.vector_index.add(embeddings)
                self.chunks.extend(processed_chunks)

        # Save updated database
        with open(database_path, "wb") as f:
            pickle.dump({"vector_index": self.vector_index, "chunks": self.chunks}, f)
            print("Vector database saved.")
        print(f"Number of chunks: {len(self.chunks)}")
        print(f"Vector index dimension: {self.vector_index.d}")
        print(f"Vector index size: {self.vector_index.ntotal}")
    
    def advanced_text_splitter(
        self, 
        text: str, 
        chunk_size: int = 1000, 
        chunk_overlap: int = 100
    ) -> List[str]:
        """
        Advanced text splitting with multiple strategies.
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return splitter.split_text(text)

def make_a_rag(subject, topic):
    rag_system = EnhancedLectureRAG(
        embedder_name='multi-qa-MiniLM-L6-cos-v1',
        retrieval_strategy='hybrid',
        reranking_model=None
    )
    # Load documents and build vector database
    with open(os.path.join("src","data", "raw", subject, topic, "transcription_text.txt")) as file:
        lecture = file.readlines()
    
    database_path = os.path.join("src","data", "raw", subject, "vector_db.pkl")
    rag_system.build_vector_database(lecture, database_path=database_path, append=False)
    
    return rag_system
   


# Example Usage
def main(subject="Natural Language Processing", topic="Vectorization"):
    # Initialize Advanced RAG System
    rag_system = EnhancedLectureRAG(
        embedder_name='multi-qa-MiniLM-L6-cos-v1',
        retrieval_strategy='hybrid',
        reranking_model='cross-encoder/ms-marco-MiniLM-L-6-v2'
    )
    import os
    # Load documents and build vector database
    with open(os.path.join("src","data", "raw", subject, topic, "transcription_text.txt")) as file:
        lecture = file.readlines()
    
    database_path = os.path.join("src","data", "raw", subject, "vector_db.pkl")
    rag_system.build_vector_database(lecture, database_path=database_path, append=False)
   
    # Perform semantic retrieval
    query = "What is Singular Value Decomposition?"
    retrieved_results = rag_system.advanced_retrieval(query)
    
    return retrieved_results

if __name__ == "__main__":
    print(main())