import json
import logging
import requests
import re
from typing import Dict, Optional

class GeminiHandler:
    def __init__(self, gemini_config: Dict, logger: Optional[logging.Logger] = None):
        """
        Khởi tạo GeminiHandler với API key và logger
        
        Args:
            api_key (str): API key của Gemini
            logger (Optional[logging.Logger]): Logger object, nếu None sẽ tạo logger mới
        """
        self.api_key = gemini_config.get('api_key')
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json"
        }
        
        if logger:
            self.logger = logger
        else:
            self.logger = logging.getLogger(__name__)
            self.logger.setLevel(logging.INFO)
            
            # Tạo handler cho console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # Tạo formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            
            # Thêm handler vào logger
            self.logger.addHandler(console_handler)
    
    def analyze_tweet(self, tweet_content: str, topic: str = None) -> Dict:
        """
        Phân tích nội dung tweet sử dụng Gemini API
        
        Args:
            tweet_content (str): Nội dung tweet cần phân tích
            topic (str, optional): Chủ đề cần phân tích. Mặc định là None
            
        Returns:
            Dict: Kết quả phân tích dưới dạng dictionary
        """
        try:
            # Xây dựng prompt
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
            
            # Gửi request đến Gemini API
            data = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            response = requests.post(
                url,
                headers=self.headers,
                json=data
            )
            
            if response.status_code != 200:
                self.logger.error(f"Error calling Gemini API: {response.status_code} - {response.text}")
                return {"topic": None}
            
            # Parse response
            response_data = response.json()
            if "candidates" not in response_data or not response_data["candidates"]:
                self.logger.error("No response from Gemini API")
                return {"topic": None}
            
            # Lấy nội dung từ response
            content = response_data["candidates"][0]["content"]["parts"][0]["text"]
            
            # Xử lý markdown code block nếu có
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                content = json_match.group(1)
            
            # Parse JSON từ nội dung
            try:
                result = json.loads(content)
                self.logger.info(f"Successfully analyzed tweet: {result}")
                return result
            except json.JSONDecodeError as e:
                self.logger.error(f"Error parsing JSON from Gemini response: {str(e)}")
                return {"topic": None}
                
        except Exception as e:
            self.logger.error(f"Error analyzing tweet: {str(e)}")
            return {"topic": None} 