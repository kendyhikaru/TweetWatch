import requests
import logging
from typing import Dict, List, Optional
import json

class AnthropicHandler:
    """Handler for interacting with Anthropic's Claude API"""
    
    def __init__(self, config: Dict, logger: logging.Logger):
        """Initialize Anthropic handler with configuration"""
        self.logger = logger
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'claude-3-opus-20240229')
        self.max_tokens = config.get('max_tokens', 1000)
        self.temperature = config.get('temperature', 0)
        self.base_url = "https://api.anthropic.com/v1"
        
        if not self.api_key:
            self.logger.error("Anthropic API key not found in configuration")
            raise ValueError("Anthropic API key not found in configuration")
            
    def _make_request(self, endpoint: str, data: Dict) -> Dict:
        """Send request to Anthropic API"""
        try:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            response = requests.post(
                f"{self.base_url}/{endpoint}",
                headers=headers,
                json=data
            )
            
            if response.status_code != 200:
                self.logger.error(f"API error: {response.status_code} - {response.text}")
                return None
                
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error calling API: {str(e)}")
            return None
            
    def analyze_tweet(self, tweet_content: str) -> Optional[Dict]:
        """Analyze a tweet using Claude"""
        try:
            # Print full tweet content
            print("\n" + "="*50)
            print("Tweet content:")
            print(tweet_content)
            print("="*50 + "\n")
            
            # Build prompt for Claude
            prompt = f"""Please analyze the following tweet and return the result in JSON format:
            Tweet: {tweet_content}
            
            Analysis requirements:
            - Write a short title about the Tweet, no more than 20 words.
            - Classify the content topic into one of: web_exploit, binary_exploit, moblie_exploit, cloud_exploit, malware
            - Classify the information type into one of: news, paper, presentation, tool
            - Target: return the attack target, one of: user, server, cloud
            - If topic is not none:
                - Product name: return the affected product name
                - Company name: return the company owning the product, if opensource return "opensource", if none return "none"
                - Product popularity: return product popularity from 1 to 5 where:
                    - 1: Very few people know about it
                    - 2: Few people know about it
                    - 3: Average. Belongs to small and medium companies/solutions
                    - 4: Many people know about it, belongs to large companies but not main products. If opensource, popular product
                    - 5: Very many people know about it, belongs to large companies, popular products. If opensource, extremely popular
                - Vulnerability type: return specific vulnerability name like: SQL Injection, Remote Code Execution, etc.
                - Has exploit: return true or false
                - Exploit URL: return exploit access URL
                - Summary: If Exploit URL is avaiable, access link and summary, return a summary of the tweet content, no more than 100 words. 
            - Conclusion: return true or false for warning if:
                - Not news
                - Popular product, level 3 or above
                - Serious vulnerability allowing control takeover
                - In-depth analysis of vulnerability, finding method, exploitation method
            
            Note:
            - If tweet doesn't belong to any topic, return topic as none
            - If tweet doesn't belong to any info type, return topic as none
            - Don't provide any other information, include reason or anything else. I want only JSON format.
            Return JSON with the following format if topic is not none:
            {{
                "title": "title",
                "topic": "topic",
                "info_type": "info_type",
                "target": "target",
                "product_popularity": product_popularity,
                "has_exploit": true of false,
                "exploit_url": "exploit_url",
                "product_name": "product_name",
                "company_name": "company_name",
                "exploit_type": "exploit_type",
                "tweet_url": "tweet_url",
                "is_warning": true of false,
                "summary": "summary"
            }}
            Return JSON with the following format if topic is none:
            {{
                "topic": none
            }}
            """
            
            # Call Claude API
            data = {
                "model": self.model,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = self._make_request("messages", data)
            if not response:
                return {"topic": None}
                
            # Extract and process response
            content = response.get('content', [{}])[0].get('text', '')
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                self.logger.error(f"Could not parse JSON from response: {content}")
                return {"topic": None}
                
        except Exception as e:
            self.logger.error(f"Error analyzing tweet: {str(e)}")
            return {"topic": None}
            
    def list_models(self) -> List[str]:
        """List available Claude models"""
        try:
            headers = {
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01"
            }
            
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers
            )
            
            if response.status_code != 200:
                self.logger.error(f"API error: {response.status_code} - {response.text}")
                return []
                
            models = response.json()
            self.logger.info("Available models:")
            for model in models.get('data', []):
                self.logger.info(f"- {model['id']}")
                
            return [model['id'] for model in models.get('data', [])]
            
        except Exception as e:
            self.logger.error(f"Error listing models: {str(e)}")
            return []
            