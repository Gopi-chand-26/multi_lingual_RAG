import logging
from typing import List, Dict, Optional
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage, SystemMessage
from config import GROQ_API_KEY, LLM_MODEL, SUPPORTED_LANGUAGES
from utils.document_processor import DocumentProcessor
from utils.vector_store import MultilingualVectorStore
from utils.translation_service import TranslationService

logger = logging.getLogger(__name__)

class MultilingualRAGEngine:
    def __init__(self):
        self.document_processor = DocumentProcessor()
        self.vector_store = MultilingualVectorStore()
        self.translation_service = TranslationService()
        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=LLM_MODEL,
            temperature=0.1
        )
    
    def process_and_index_document(self, file_path: str) -> Dict:
        """Process a document and add it to the vector store."""
        try:
            # Process the document
            document_data = self.document_processor.process_document(file_path)
            
            # Add to vector store
            success = self.vector_store.add_documents([document_data])
            
            if success:
                return {
                    'success': True,
                    'message': f"Document processed and indexed successfully",
                    'data': {
                        'file_name': document_data['file_name'],
                        'language': document_data['language'],
                        'chunk_count': document_data['chunk_count'],
                        'file_size': document_data['file_size']
                    }
                }
            else:
                return {
                    'success': False,
                    'message': "Failed to index document"
                }
                
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            return {
                'success': False,
                'message': f"Error processing document: {str(e)}"
            }
    
    def search_and_generate_response(self, query: str, target_language: str = 'en', 
                                   search_language: str = 'all', top_k: int = 5) -> Dict:
        """Search for relevant documents and generate a response in the target language."""
        try:
            # Detect query language
            query_language = self.translation_service.detect_language(query)
            
            # Search for relevant documents
            if search_language == 'all':
                search_results = self.vector_store.search_multilingual(query, target_language, top_k)
            else:
                search_results = self.vector_store.search_documents(query, search_language, top_k)
            
            if not search_results:
                # Provide a helpful response when no documents are found
                no_docs_message = {
                    'en': "I couldn't find any relevant information in the uploaded documents for your query. Please try uploading documents that contain the information you're looking for, or rephrase your question.",
                    'es': "No pude encontrar información relevante en los documentos cargados para tu consulta. Por favor, intenta cargar documentos que contengan la información que buscas, o reformula tu pregunta.",
                    'fr': "Je n'ai pas trouvé d'informations pertinentes dans les documents téléchargés pour votre requête. Veuillez essayer de télécharger des documents contenant les informations que vous recherchez, ou reformuler votre question.",
                    'de': "Ich konnte in den hochgeladenen Dokumenten keine relevanten Informationen für Ihre Anfrage finden. Bitte versuchen Sie, Dokumente hochzuladen, die die gesuchten Informationen enthalten, oder formulieren Sie Ihre Frage um.",
                    'ja': "アップロードされた文書から、あなたの質問に関連する情報を見つけることができませんでした。探している情報を含む文書をアップロードするか、質問を言い換えてください。",
                    'ko': "업로드된 문서에서 귀하의 질문과 관련된 정보를 찾을 수 없었습니다. 찾고 있는 정보가 포함된 문서를 업로드하거나 질문을 다시 작성해 주세요.",
                    'zh': "我在上传的文档中找不到与您的问题相关的信息。请尝试上传包含您要查找信息的文档，或重新表述您的问题。",
                    'ar': "لم أتمكن من العثور على معلومات ذات صلة في المستندات المرفوعة لاستفسارك. يرجى محاولة رفع مستندات تحتوي على المعلومات التي تبحث عنها، أو إعادة صياغة سؤالك.",
                    'hi': "मैं आपके प्रश्न के लिए अपलोड किए गए दस्तावेजों में कोई प्रासंगिक जानकारी नहीं पा सका। कृपया उन दस्तावेजों को अपलोड करने का प्रयास करें जिनमें आप जिस जानकारी की तलाश कर रहे हैं, या अपने प्रश्न को पुनः तैयार करें।",
                    'ru': "Я не смог найти релевантную информацию в загруженных документах для вашего запроса. Пожалуйста, попробуйте загрузить документы, содержащие информацию, которую вы ищете, или переформулируйте ваш вопрос."
                }
                
                return {
                    'success': True,
                    'response': no_docs_message.get(target_language, no_docs_message['en']),
                    'sources': [],
                    'query_language': query_language,
                    'target_language': target_language,
                    'context_length': 0,
                    'no_documents_found': True
                }
            
            # Prepare context from search results
            context_parts = []
            sources = []
            
            for result in search_results:
                content = result['content']
                metadata = result['metadata']
                
                # Translate content if needed
                if metadata.get('language') != target_language:
                    content = self.translation_service.translate_text(
                        content, target_language, metadata.get('language', 'auto')
                    )
                
                context_parts.append(content)
                sources.append({
                    'file_name': metadata.get('file_name', 'Unknown'),
                    'language': metadata.get('language', 'Unknown'),
                    'similarity': 1 - result.get('distance', 0) if result.get('distance') else 0
                })
            
            context = "\n\n".join(context_parts)
            
            # Create multilingual prompt
            prompt = self.translation_service.create_multilingual_prompt(
                query, target_language, query_language
            )
            
            # Generate response using LLM
            messages = [
                SystemMessage(content=f"""You are a multilingual AI assistant. Use the following context to answer the user's question in {SUPPORTED_LANGUAGES.get(target_language, target_language)}.

Context:
{context}

Guidelines:
- Provide accurate and comprehensive answers based on the context
- Maintain cultural sensitivity and appropriate language style
- If the context doesn't contain enough information, say so clearly
- Cite sources when possible
- Be concise but thorough"""),
                HumanMessage(content=prompt)
            ]
            
            response = self.llm.invoke(messages)
            
            return {
                'success': True,
                'response': response.content,
                'sources': sources,
                'query_language': query_language,
                'target_language': target_language,
                'context_length': len(context)
            }
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return {
                'success': False,
                'message': f"Error generating response: {str(e)}",
                'response': None,
                'sources': []
            }
    
    def get_system_stats(self) -> Dict:
        """Get system statistics."""
        try:
            vector_stats = self.vector_store.get_collection_stats()
            translation_stats = self.translation_service.get_cache_stats()
            
            return {
                'vector_store': vector_stats,
                'translation_cache': translation_stats,
                'supported_languages': list(SUPPORTED_LANGUAGES.keys())
            }
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {}
    
    def clear_system_data(self) -> Dict:
        """Clear all system data."""
        try:
            # Clear vector store
            self.vector_store.clear_collection()
            
            # Clear translation cache
            self.translation_service.clear_cache()
            
            return {
                'success': True,
                'message': "System data cleared successfully"
            }
        except Exception as e:
            logger.error(f"Error clearing system data: {e}")
            return {
                'success': False,
                'message': f"Error clearing system data: {str(e)}"
            }