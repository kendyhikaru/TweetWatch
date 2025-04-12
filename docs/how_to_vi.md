# Hành trình xây dựng trợ lý bảo mật của tôi

Là một chuyên gia bảo mật, tôi luôn cảm thấy bị ngập trong một đại dương thông tin. Mỗi ngày, hàng trăm tweet về lỗ hổng mới, exploit mới, và các nghiên cứu bảo mật được đăng tải. Ban đầu, tôi cố gắng theo dõi thủ công - mở X (Twitter) liên tục, đọc từng tweet một, cố gắng đánh giá độ quan trọng và quyết định xem có cần hành động ngay không. Nhưng rồi tôi nhận ra điều này không khả thi.

Có những buổi sáng tỉnh dậy và thấy cả thế giới đang bàn tán về một lỗ hổng nghiêm trọng mà tôi chưa biết. Tôi tự hỏi: "Làm sao để không bỏ lỡ những thông tin quan trọng? Làm sao để có thể nghỉ ngơi mà vẫn theo dõi được mọi thứ?"

Và thế là ý tưởng về một trợ lý ảo ra đời. Một trợ lý có thể thay tôi theo dõi các chuyên gia bảo mật 24/7, phân tích từng tweet và chỉ đánh thức tôi khi thực sự cần thiết.

## Gặp gỡ Claude - Trợ lý phân tích của tôi

Sau khi thử nghiệm nhiều cách tiếp cận khác nhau, tôi quyết định chọn Claude làm "bộ não" cho trợ lý của mình. Claude không chỉ là một AI thông thường - nó có khả năng hiểu ngữ cảnh và đánh giá thông tin một cách tinh tế. Tôi đã dành hàng tuần để "huấn luyện" Claude cách phân tích tweet: phân biệt giữa một lỗ hổng nghiêm trọng và một tin tức thông thường, đánh giá mức độ phổ biến của sản phẩm bị ảnh hưởng, và quan trọng nhất là biết khi nào cần báo động.

## Telegram - Kênh thông báo đáng tin cậy

Sau khi có Claude phân tích, tôi cần một kênh thông báo hiệu quả. Email quá chậm, SMS thì tốn kém. Telegram trở thành lựa chọn hoàn hảo - nhanh, ổn định và có khả năng định dạng tin nhắn đẹp mắt. Mỗi khi Claude phát hiện điều gì đó quan trọng, một tin nhắn được gửi ngay đến điện thoại của tôi, được định dạng rõ ràng với HTML để tôi có thể nhanh chóng nắm bắt thông tin quan trọng.

Giờ đây, tôi có thể yên tâm tập trung vào công việc hoặc nghỉ ngơi, biết rằng có một đội ngũ "nhân viên ảo" đang làm việc không ngừng nghỉ. Họ theo dõi, phân tích và chỉ thông báo khi thực sự cần thiết. Đó chính xác là những gì tôi cần - một trợ lý thông minh, đáng tin cậy và luôn hoạt động 24/7.

## Lựa chọn công nghệ - Thách thức và giải pháp

Việc thu thập dữ liệu từ X (Twitter) là một thách thức lớn. Tôi đã thử nghiệm qua nhiều phương pháp:

### Twitter API - Chi phí cao và hạn chế
Ban đầu, tôi thử nghiệm Twitter API chính thức. Nó cung cấp dữ liệu đáng tin cậy và realtime, nhưng chi phí quá cao cho việc theo dõi liên tục. Với mức giá $100/tháng cho API cơ bản và giới hạn số lượng request, đây không phải là giải pháp khả thi cho một dự án cá nhân.

### RSS Feed - Không còn được hỗ trợ
RSS từng là một giải pháp tuyệt vời để theo dõi Twitter. Đơn giản, nhẹ nhàng và hoàn toàn miễn phí. Tuy nhiên, Twitter đã ngừng hỗ trợ RSS feed từ năm 2023, khiến phương án này không còn khả thi.

### Nitter API - Bất ổn định
Nitter - một frontend thay thế cho Twitter, cung cấp API miễn phí và RSS feed. Tôi đã thử nghiệm nhưng gặp nhiều vấn đề:
- Nhiều instance thường xuyên bị chặn
- Tốc độ không ổn định
- Dữ liệu đôi khi bị thiếu hoặc không cập nhật kịp thời

### Giải pháp cuối cùng - Selenium với Nitter
Sau nhiều thử nghiệm, tôi quyết định kết hợp Selenium với Nitter. Selenium cho phép tự động hóa trình duyệt thực tế, trong khi Nitter giúp truy cập dữ liệu Twitter mà không cần API chính thức.

Thách thức lớn nhất là vượt qua Cloudflare - hệ thống bảo vệ chống bot của Nitter. Selenium thông thường thường bị phát hiện và chặn. Giải pháp là sử dụng undetected-chromedriver, một biến thể của Selenium được thiết kế đặc biệt để vượt qua các cơ chế phát hiện bot.

Đây là đoạn code tôi sử dụng để xử lý vấn đề này:
```
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Add options to bypass Cloudflare
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Add real user agent
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36')
        
        self.driver = webdriver.Chrome(options=options)
        
        # Add JavaScript to hide automation signs
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.logger.info("WebDriver started successfully")
        return True
    except Exception as e:
        self.logger.error(f"Error starting WebDriver: {str(e)}")
        return False
```


### Anthropic API - Tương tác trực tiếp qua HTTP

Khi làm việc với Anthropic API, tôi đã thử nghiệm hai cách tiếp cận:

#### Python Library - Nhiều vấn đề phát sinh
Ban đầu tôi sử dụng thư viện Python chính thức của Anthropic. Tuy nhiên gặp một số vấn đề:
- Phiên bản thư viện thường không cập nhật kịp với API mới
- Xử lý lỗi không linh hoạt
- Khó kiểm soát các tham số request
- Đôi khi gặp lỗi không rõ nguyên nhân

#### HTTP Request - Giải pháp ổn định
Cuối cùng tôi chọn tương tác trực tiếp với API thông qua HTTP request:
- Kiểm soát hoàn toàn request/response
- Dễ dàng debug và xử lý lỗi
- Linh hoạt trong việc tùy chỉnh tham số
- Không phụ thuộc vào phiên bản thư viện


### Xây dựng Prompt cho Claude

Khi xây dựng prompt để phân tích tweet, tôi tập trung vào các yếu tố sau:

#### 1. Cấu trúc thông tin cần phân tích
- Tiêu đề ngắn gọn về nội dung tweet
- Phân loại chủ đề (web_exploit, binary_exploit, malware,...)
- Loại thông tin (tin tức, paper, công cụ,...)
- Đối tượng bị tấn công (user, server, cloud)
- Thông tin về sản phẩm/lỗ hổng (tên sản phẩm, công ty, mức độ phổ biến,...)
- Thông tin về exploit (có/không, URL, tóm tắt)

#### 2. Định dạng kết quả
- Sử dụng JSON để dễ dàng xử lý
- Các trường thông tin được định nghĩa rõ ràng
- Có xử lý cho cả trường hợp tweet không liên quan

#### 3. Hướng dẫn chi tiết
- Cách phân loại và đánh giá các thông tin
- Tiêu chí để xác định mức độ cảnh báo
- Giới hạn độ dài cho các trường thông tin

Dưới đây là ví dụ về prompt tôi sử dụng:

```
"""Please analyze the following tweet and return the result in JSON format:
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
        "summay": "summary"
    }}
    Return JSON with the following format if topic is none:
    {{
        "topic": none
    }}
    """
```


Ví dụ về JSON response khi tweet có chứa thông tin về lỗ hổng:

{
    "title": "Critical RCE vulnerability found in Apache Struts 2",
    "topic": "web_exploit", 
    "info_type": "news",
    "target": "server",
    "product_popularity": 5,
    "has_exploit": true,
    "exploit_url": "https://github.com/example/CVE-2023-1234",
    "product_name": "Apache Struts 2",
    "company_name": "opensource",
    "exploit_type": "Remote Code Execution",
    "tweet_url": "https://twitter.com/security_alert/status/123456789",
    "is_warning": true,
    "summary": "Critical RCE vulnerability discovered in Apache Struts 2 affecting versions 2.0.0-2.5.30. Attackers can execute arbitrary code by sending specially crafted requests. Patch available in version 2.5.31."
}


## Gửi thông báo qua Telegram

Sau khi có kết quả phân tích từ Claude, chúng ta cần một cơ chế để thông báo ngay cho người dùng khi phát hiện vấn đề nghiêm trọng. Telegram là một lựa chọn tuyệt vời cho việc này vì nhiều lý do:

- API đơn giản, dễ tích hợp
- Hỗ trợ định dạng HTML giúp tin nhắn dễ đọc
- Thông báo push nhanh chóng tới điện thoại
- Hoàn toàn miễn phí cho mục đích cá nhân

Khi Claude phân tích và trả về is_warning là True, hệ thống sẽ tự động tạo một tin nhắn được định dạng đẹp mắt với các thông tin quan trọng như:

- Tiêu đề của vấn đề
- Sản phẩm và công ty bị ảnh hưởng
- Mức độ nghiêm trọng
- Link tới exploit nếu có
- Tóm tắt ngắn gọn vấn đề

Tin nhắn này sẽ được gửi ngay tới Telegram bot đã được cấu hình trước. Người dùng sẽ nhận được thông báo ngay lập tức trên điện thoại, giúp có thể phản ứng nhanh với các mối đe dọa bảo mật mới.

## Tự động hóa với Crontab

Để hệ thống có thể hoạt động liên tục 24/7, chúng ta cần một cơ chế để tự động chạy script định kỳ. Crontab trên Linux/Unix là một công cụ hoàn hảo cho việc này. Chúng ta có thể:

- Cấu hình script chạy mỗi 5-10 phút một lần
- Tự động khởi động lại nếu có lỗi
- Ghi log đầy đủ để theo dõi hoạt động
- Tiết kiệm tài nguyên khi không cần thiết

Việc cấu hình crontab rất đơn giản nhưng hiệu quả, giúp đảm bảo hệ thống luôn trong trạng thái hoạt động và sẵn sàng phát hiện các mối đe dọa mới.

![IMG](1.png)


## Tổng kết

Vậy là chúng ta đã cùng nhau xây dựng xong một hệ thống theo dõi bảo mật thú vị rồi! 🎉

Hệ thống của chúng ta như một chú robot nhỏ siêng năng, luôn theo dõi và phân tích các tweet về bảo mật 24/7. Hãy cùng điểm qua những gì chú robot này có thể làm nhé:

🕷️ **Thu thập thông tin**:
- Tự động "lướt" Nitter để đọc các tweet mới
- Lưu lại những gì đã đọc để không bị trùng lặp
- Có thể theo dõi nhiều tài khoản chuyên gia cùng lúc

🧠 **Phân tích thông minh**:
- Nhờ sự giúp đỡ của Claude AI để hiểu nội dung tweet
- Tự động phân loại xem tweet có quan trọng không
- Trích xuất những thông tin cần thiết một cách gọn gàng

📱 **Thông báo kịp thời**:
- Gửi tin nhắn Telegram ngay khi phát hiện điều gì đó quan trọng
- Tự đánh giá mức độ nguy hiểm của các lỗ hổng
- Giúp bạn không bỏ lỡ thông tin nào cả

⚙️ **Dễ dàng quản lý**:
- Ghi chép đầy đủ mọi hoạt động
- Tùy chỉnh linh hoạt qua file cấu hình
- Tự động xử lý khi gặp lỗi

Với chú robot này, việc theo dõi tin tức bảo mật trở nên dễ dàng và thú vị hơn rất nhiều! Bạn có thể yên tâm làm việc khác trong khi robot luôn canh chừng và báo ngay cho bạn khi có điều gì đáng chú ý. 

Hy vọng bài hướng dẫn này giúp bạn hiểu rõ hơn về cách xây dựng một hệ thống tự động thú vị như vậy! 🚀

## Lời cảm ơn đặc biệt

Tôi muốn gửi lời cảm ơn chân thành đến:

🤖 **Claude** - Trợ lý AI tuyệt vời từ Anthropic:
- Đã giúp tôi phân tích và đánh giá hàng nghìn tweet mỗi ngày
- Luôn đưa ra những nhận định chính xác và đáng tin cậy
- Là "bộ não" đáng tin cậy cho toàn bộ hệ thống

💻 **Cursor** - IDE thông minh:
- Đã hỗ trợ tôi viết code nhanh và hiệu quả hơn với các gợi ý thông minh
- Giúp tôi debug và tối ưu code dễ dàng
- Là người bạn đồng hành tin cậy trong suốt quá trình phát triển

Không có sự hỗ trợ của họ, việc xây dựng một hệ thống phức tạp như thế này sẽ khó khăn hơn rất nhiều. Cảm ơn các bạn đã giúp biến ý tưởng của tôi thành hiện thực! 🙏










