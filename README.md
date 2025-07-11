# Ebenezer Marcus Quiz Portal

Welcome to the **Ebenezer Marcus Quiz Portal** – an intuitive web application designed for students and teachers to manage, attend, and create quizzes seamlessly.

<p align="center">
  <img src="statics/logo.png" alt="Ebenezer Marcus Logo" width="200">
</p>

## 🚀 Features

- **Student & Teacher Login:** Secure login pages for both roles.
- **Dashboard:** Personalized dashboards for students and teachers.
- **Quiz Management:** Teachers can create, edit, and manage quizzes; students can take quizzes and view results.
- **Firebase Backend:** Real-time and secure data using Firebase Realtime Database.
- **Responsive UI:** Built with [Streamlit](https://streamlit.io/) for a fast, interactive experience.
- **Sidebar Control:** Custom sidebar hiding for a focused test environment.

---

## 🏗️ Project Structure

```
├── app.py                  # Main Streamlit app entrypoint
├── firebase_ini.py         # Firebase initialization and reference utilities
├── side_bar_disabler.py    # Sidebar hiding logic for Streamlit
├── requirements.txt        # Python dependencies
├── serviceAccountKey.json  # Firebase service account key (DO NOT SHARE PUBLICLY)
├── statics/
│   └── logo.png            # App logo
├── pages/
│   ├── Student_Login.py
│   ├── Teacher_Login.py
│   ├── Student_dashboard.py
│   └── ...                 # Additional pages
└── test.py                 # Quick test script
```

---

## ⚡ Quick Start

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/ebenezer-marcus-quiz-portal.git
   cd ebenezer-marcus-quiz-portal
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Firebase credentials:**
   - Place your `serviceAccountKey.json` in the project root.

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

5. **Open in your browser:**
   - Navigate to `http://localhost:8501` to view the portal.

---

## 🛠️ Customization

- **Logo:** Replace `statics/logo.png` with your institution's logo.
- **Quiz Content:** Build out quiz logic and dashboards in the `pages/` directory.
- **Sidebar:** Easily enable or disable the sidebar via `side_bar_disabler.py`.

---

## 🔒 Security

- **Do not expose `serviceAccountKey.json` publicly.**  
- Set up environment variables or use secret managers in production.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## 📄 License

This project is for educational use. For commercial use, please contact the repository owner.

---

## 🙏 Acknowledgements

- [Streamlit](https://streamlit.io/)
- [Firebase](https://firebase.google.com/)
- All contributors and testers!

---

> **Made with ❤️ for Ebenezer Marcus Institutions**
