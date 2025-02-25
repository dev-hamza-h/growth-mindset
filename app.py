import streamlit as st
import sqlite3
from PIL import Image
import time
import random
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

# Set page configuration
st.set_page_config(
    page_title="Growth Mindset Challenge",
    page_icon="🌱",
    layout="centered",
)


# Custom CSS for animations
st.markdown(
    """
    <style>
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(50px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .animated {
            animation: fadeInUp 1s ease-in-out;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize SQLite database
conn = sqlite3.connect("growth_mindset.db")
c = conn.cursor()

# Create tables if they don't exist
c.execute(
    """CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS progress
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, progress INTEGER, date TEXT)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS reflections
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, reflection TEXT, date TEXT)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS habits
             (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, habit TEXT, date TEXT)"""
)
conn.commit()

# Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Boost Your Mindset",
        "Progress Monitor",
        "Sign Up",
        "Login",
    ],
)


# User Authentication
def login(username, password):
    c.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    )
    return c.fetchone()


def sign_up(username, password):
    c.execute(
        "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
    )
    conn.commit()


# Home Page
if page == "Home":
    st.markdown(
        "<h1 class='animated' style='color: green;'>Welcome to the Growth Mindset Challenge! 🌱</h1>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 1])

    # Load text first
    with col1:
        st.markdown(
            """
        <div class='animated'>
            <h3>What is a Growth Mindset?</h3>
            <p>A growth mindset is the belief that your abilities and intelligence can be developed through hard work, perseverance, and learning from mistakes.
            This concept was popularized by psychologist Carol Dweck. Instead of seeing skills as fixed, it teaches us that every challenge is an opportunity to improve.</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
    <div class='animated'>
        <h3>Why Adopt a Growth Mindset?</h3>
        <ul>
            <li><b>Embrace Challenges:</b> See obstacles as opportunities to learn.</li>
            <li><b>Learn from Mistakes:</b> Mistakes are a natural part of learning.</li>
            <li><b>Persist Through Difficulties:</b> Hard work and persistence lead to growth.</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class='animated'>
        <h3>How Can You Practice a Growth Mindset?</h3>
        <ul>
            <li><b>Set Learning Goals:</b> Focus on skill development rather than just grades.</li>
            <li><b>Reflect on Your Learning:</b> Learn from both successes and challenges.</li>
            <li><b>Seek Feedback:</b> Use constructive criticism for self-improvement.</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div class='animated'>
        <p>By adopting a growth mindset, you empower yourself to overcome challenges, innovate, and continuously improve. 
        Every step, whether forward or backward, is part of the learning process. 
        Embrace your potential and never stop striving to be better.</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Show spinner and load image separately
    with col2:
        with st.spinner("Loading image..."):
            time.sleep(1)
            try:
                image = Image.open("rb_39405.png")
                st.image(
                    image,
                    caption="Embrace the power of growth!",
                    use_container_width=True,
                )
            except FileNotFoundError:
                st.error("Image file not found. Please check the path.")


# Boost Your Mindset Page
if page == "Boost Your Mindset":
    # custom CSS to ensure the heading stays visible
    st.markdown(
        """
        <style>
        .stHeadingContainer {
            position: sticky;
            top: 0;
            background-color: white;
            z-index: 1000;
            padding: 10px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    # Add content to the first column
    with col1:
        st.markdown(
            "<h1 style='color: green;'>🌟 Growth Mindset Booster</h1>",
            unsafe_allow_html=True,
        )

    # Motivational Quotes
    quotes = [
        "🌱 Growth begins the moment you step out of your comfort zone!",
        "💡 Every setback is a setup for a comeback!",
        "🔥 Keep striving – your dedication will lead to greatness!",
        "🚀 The journey of improvement starts with a single step!",
        "🌟 Progress, no matter how small, is still progress!",
    ]

    # Add content to the second column
    with col2:
        st.subheader("💭 Your Daily Motivation")
        st.info(random.choice(quotes))

    # Learning Goal
    goal = st.text_area("Set Your Learning Goal:")

    # Achieved Goal Date
    achieved_date = st.date_input("When did you achieve your goal?")
    if achieved_date:
        st.success(
            f"🎉 Bravo! You reached your goal on **{achieved_date}**. Keep going! 🏆"
        )

    # Growth Mindset Tips
    tips = st.radio(
        "Pick a tip to boost your mindset:",
        [
            "🚀 Keep pushing forward, consistency is key!",
            "🔄 Mistakes help you grow – embrace them!",
            "💬 Feedback is a tool for improvement, use it wisely.",
            "🏋️ Challenge yourself beyond limits every day!",
            "🧠 Effort makes your brain stronger and sharper!",
        ],
    )
    st.success(f"**Tip Selected:** {tips}")

    # Feedback on Progress
    feedback = st.selectbox(
        "How do you feel about your journey?",
        ["Feeling Amazing!", "Still Working on It", "Need More Motivation"],
    )
    st.write(f"💬 **Your Response:** {feedback}")

    # Celebration Button
    celebrate = st.button("🚀 Celebrate Your Effort!")
    if celebrate:
        st.snow()
    st.success("Every step you take matters. Keep up the great work! 🎉")

    # Function to generate PDF
    def generate_pdf(goal, achieved_date, tips, feedback):
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        pdf.setTitle("Growth Mindset Progress")

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, 750, "🌟 Growth Mindset Progress 🌟")

        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 700, f"Learning Goal: {goal}")
        pdf.drawString(100, 670, f"Achieved Date: {achieved_date}")
        pdf.drawString(100, 640, f"Selected Tip: {tips}")
        pdf.drawString(100, 610, f"Journey Feedback: {feedback}")

        pdf.drawString(100, 570, "🎉 Keep pushing forward and stay motivated! 🚀")

        pdf.save()
        buffer.seek(0)
        return buffer

    # Download PDF Button
    if st.button("📥 Download Your Progress as PDF"):
        if goal and achieved_date:
            pdf_file = generate_pdf(goal, achieved_date, tips, feedback)
            st.download_button(
                label="📥 Click to Download PDF",
                data=pdf_file,
                file_name="growth_mindset_progress.pdf",
                mime="application/pdf",
            )
        else:
            st.warning("⚠️ Please fill in all fields before downloading.")


# Progress Monitor
elif page == "Progress Monitor":
    st.markdown(
        "<h1 style='color: green;'>Progress Monitor 📊</h1>",
        unsafe_allow_html=True,
    )
    
    st.write("### Track your daily progress and stay motivated! 🚀")
    
    progress = st.slider("📈 How much progress have you made today?", 0, 100, 50)
    
    if st.button("💾 Save Progress"):
        if "user_id" in st.session_state:
            c.execute(
                'INSERT INTO progress (user_id, progress, date) VALUES (?, ?, DATE("now"))',
                (st.session_state["user_id"], progress),
            )
            conn.commit()
            
            st.success(f"✅ Progress saved successfully: {progress}%")
            
            # Display motivational message
            if progress < 30:
                st.warning("Keep pushing! 💪 Small steps lead to big achievements.")
            elif progress < 70:
                st.info("You're doing great! Stay consistent. ✨")
            else:
                st.success("Amazing progress! Keep up the fantastic work! 🎉")
        else:
            st.error("🚨 Please log in to save your progress.")


# Sign Up Page
elif page == "Sign Up":
    st.markdown(
        "<h1 style='color: green;'>Sign Up</h1>",
        unsafe_allow_html=True,
    )
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        sign_up(username, password)
        st.success("You have successfully signed up! Please log in.")


# Login Page
elif page == "Login":
    st.markdown(
        "<h1 style='color: green;'>Log in</h1>",
        unsafe_allow_html=True,
    )
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = login(username, password)
        if user:
            st.session_state["user_id"] = user[0]
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password.")
