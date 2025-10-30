"""
AI-based analyzer using LLMs for intelligent code comparison.
"""

from typing import Optional
from app.models.schemas import ComparisonResult, AnalysisMethod
from app.core.config import settings
from app.services.analyzer.code_analyzer import CodeAnalyzer


class AIAnalyzer:
    """AI-based analyzer using Claude or OpenAI for semantic analysis."""

    def __init__(self):
        """Initialize the AI analyzer."""
        self.code_analyzer = CodeAnalyzer()
        self.anthropic_client = None
        self.openai_client = None

        # Initialize AI clients if API keys are available
        if settings.anthropic_api_key:
            try:
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(api_key=settings.anthropic_api_key)
            except ImportError:
                pass

        if settings.openai_api_key:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=settings.openai_api_key)
            except ImportError:
                pass

    def analyze(
        self,
        pre_code: str,
        post_code: str,
        ai_model: str = "claude"
    ) -> ComparisonResult:
        """
        Analyze PRE and POST programs using AI-assisted analysis.

        Args:
            pre_code: PRE conversion COBOL code
            post_code: POST conversion COBOL code
            ai_model: AI model to use ("claude" or "openai")

        Returns:
            Comparison result with AI insights
        """
        # First get code-based analysis
        result = self.code_analyzer.analyze(pre_code, post_code)

        # Add AI insights if available
        ai_insights = self._get_ai_insights(pre_code, post_code, ai_model)
        result.ai_insights = ai_insights
        result.analysis_method = AnalysisMethod.AI_BASED

        return result

    def _get_ai_insights(
        self,
        pre_code: str,
        post_code: str,
        ai_model: str
    ) -> Optional[str]:
        """
        Get AI insights about the transformation.

        Args:
            pre_code: PRE conversion code
            post_code: POST conversion code
            ai_model: AI model to use

        Returns:
            AI-generated insights or None if unavailable
        """
        prompt = self._create_analysis_prompt(pre_code, post_code)

        if ai_model == "claude" and self.anthropic_client:
            return self._analyze_with_claude(prompt)
        elif ai_model == "openai" and self.openai_client:
            return self._analyze_with_openai(prompt)
        else:
            return "AI analysis unavailable: No API key configured"

    def _create_analysis_prompt(self, pre_code: str, post_code: str) -> str:
        """
        Create analysis prompt for the AI model.

        Args:
            pre_code: PRE conversion code
            post_code: POST conversion code

        Returns:
            Formatted prompt
        """
        return f"""Analyze the following COBOL code transformation from REPEAT GROUPS to SCR100 grid logic.

PRE CONVERSION CODE (using REPEAT GROUPS):
```cobol
{pre_code[:2000]}
```

POST CONVERSION CODE (using SCR100):
```cobol
{post_code[:2000]}
```

Please provide:
1. Key transformation patterns you observe
2. How REPEAT GROUP logic maps to SCR100 calls
3. Changes in data structures (SP2-RX- fields to GRID structures)
4. Changes in procedural logic (PERFORM VARYING to SCR100 operations)
5. Potential edge cases or considerations for similar conversions

Be concise and focus on actionable insights for building a conversion tool."""

    def _analyze_with_claude(self, prompt: str) -> str:
        """
        Analyze using Claude API.

        Args:
            prompt: Analysis prompt

        Returns:
            AI response
        """
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        except Exception as e:
            return f"Claude analysis failed: {str(e)}"

    def _analyze_with_openai(self, prompt: str) -> str:
        """
        Analyze using OpenAI API.

        Args:
            prompt: Analysis prompt

        Returns:
            AI response
        """
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a COBOL expert specializing in legacy code modernization."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"OpenAI analysis failed: {str(e)}"

    def is_available(self, ai_model: str = "claude") -> bool:
        """
        Check if AI analysis is available.

        Args:
            ai_model: AI model to check

        Returns:
            True if available
        """
        if ai_model == "claude":
            return self.anthropic_client is not None
        elif ai_model == "openai":
            return self.openai_client is not None
        return False
