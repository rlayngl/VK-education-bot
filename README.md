# VK Education FAQ Bot

An automated assistant designed to support students on the **VK Education** platform. This bot streamlines communication by providing instant answers to the most frequent questions regarding the website, courses, and educational process.

### Features
*   **24/7 Automated Support:** Instant responses to common student inquiries.
*   **Knowledge Base:** Managed via a structured `faq.json` file for easy updates.
*   **Seamless Integration:** Built using VK Callback API for real-time message processing.
*   **Secure:** Implements environment variables for sensitive API tokens.

### Tech Stack
*   **Language:** Python 3.x
*   **API Wrapper:** `vk_api`
*   **Web Framework:** `Flask` (for handling Callback API webhooks)
*   **Configuration:** `python-dotenv`
*   **Deployment:** Ready for **Render** (via `render.yaml`)

### Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com
   cd repository-name
   ```

2. **Set up Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```text
   VK_TOKEN=your_group_access_token
   CONFIRMATION_TOKEN=your_server_confirmation_code
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Bot:**
   ```bash
   python app.py
   ```

### Project Structure
*   `app.py` – Main server handling incoming requests from VK.
*   `bot.py` – Core logic for interacting with the VK API.
*   `faq.json` – Database containing questions and predefined answers.
*   `render.yaml` – Configuration for quick deployment on Render.com.

---
Developed as part of the **VK Education** practice/educational program by Alexandr Vyssotskiy.
