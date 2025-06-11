"""
GPT-4 question answering utilities.
"""
import openai
from typing import List, Union, Tuple
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)
openai.api_key = settings.OPENAI_API_KEY

def get_gpt4_answer(question: str, context: Union[str, List[str]]) -> Tuple[str, str]:
    """
    Get an answer from GPT-4 using the provided context (str or list of chunks).
    Args:
        question: User's question
        context: Relevant context from the PDF (str or list of chunks)
    Returns:
        Tuple of (answer, context_used)
    """
    try:
        # Handle chunk joining if context is a list
        if isinstance(context, list):
            context_used = "\n\n".join(context)
        else:
            context_used = context
        logger.info(f"Generating answer for question: {question[:100]}... Context length: {len(context_used)}")

        prompt = (
            "Based on the following context, please answer the question. "
            "If the answer cannot be found in the context, say so.\n\n"
            f"Context:\n{context_used}\n\nQuestion: {question}\n\nAnswer:"
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            answer = response.choices[0].message['content'].strip()
            logger.info("Successfully generated answer")
            return answer, context_used
        except openai.error.OpenAIError as oe:
            logger.error(f"OpenAI API error: {oe}")
            raise RuntimeError(f"OpenAI API error: {oe}")
        except Exception as e:
            logger.error(f"Unexpected error during OpenAI call: {e}")
            raise RuntimeError(f"Unexpected error during OpenAI call: {e}")
    except Exception as e:
        logger.error(f"Error in get_gpt4_answer: {str(e)}")
        raise 