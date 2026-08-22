from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
    flash,
    session
)

import os

from dotenv import load_dotenv

from werkzeug.utils import secure_filename

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from reportlab.pdfgen import canvas

import easyocr

from authlib.integrations.flask_client import OAuth

from database import init_db

from models import (
    db,
    User,
    Prediction
)
from training.predict import (
    predict_personality,
    get_level,
    descriptions,
    generate_summary
)
import random
import smtplib
from email.mime.text import MIMEText
from werkzeug.security import generate_password_hash
# ==========================================
# APPLICATION SETUP
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = Flask(__name__)
oauth = OAuth(app)

app.secret_key = os.getenv(
    "SECRET_KEY"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "static",
    "uploads"
)

app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER

if not os.path.exists(
    UPLOAD_FOLDER
):
    os.makedirs(
        UPLOAD_FOLDER
    )

init_db(app)

reader = easyocr.Reader(['en'])

def send_otp_email(receiver_email, otp, purpose="Verification"):

    if purpose == "register":
        subject = "Personality AI - Email Verification OTP"

        body = f"""
Hello,

Welcome to Personality AI!

Your Email Verification OTP is:

{otp}

This OTP is valid for 5 minutes.

Regards,
Personality AI Team
"""

    else:

        subject = "Personality AI - Password Reset OTP"

        body = f"""
Hello,

Your Password Reset OTP is:

{otp}

This OTP is valid for 5 minutes.

Regards,
Personality AI Team
"""

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = receiver_email

    try:

        server = smtplib.SMTP("smtp.gmail.com",587)

        server.starttls()

        server.login(EMAIL_USER,EMAIL_PASS)

        server.send_message(msg)

        server.quit()

        return True

    except Exception as e:

        print("EMAIL ERROR :",e)

        return False
# ==========================================
# GOOGLE OAUTH
# ==========================================

google = oauth.register(

    name="google",

    client_id=os.getenv("GOOGLE_CLIENT_ID"),

    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),

    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",

    client_kwargs={
        "scope": "openid email profile"
    }

)
# ==========================================
# DASHBOARD
# ==========================================

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # ==========================================
    # Logged-in User
    # ==========================================

    user = User.query.get(session["user_id"])

    # ==========================================
    # Latest Prediction
    # ==========================================

    latest = Prediction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Prediction.created_at.desc()
    ).first()

    if latest is None:

        flash(
            "No prediction found. Please analyze your personality first."
        )

        return redirect(url_for("analyze"))

    # ==========================================
    # Rebuild Prediction Dictionary
    # ==========================================

    prediction = {

        "Openness": {

            "score": latest.openness,

            "level": get_level(latest.openness),

            "description":
            descriptions["Openness"][
                get_level(latest.openness)
            ]

        },

        "Conscientiousness": {

            "score": latest.conscientiousness,

            "level": get_level(
                latest.conscientiousness
            ),

            "description":
            descriptions["Conscientiousness"][
                get_level(latest.conscientiousness)
            ]

        },

        "Extraversion": {

            "score": latest.extraversion,

            "level": get_level(
                latest.extraversion
            ),

            "description":
            descriptions["Extraversion"][
                get_level(latest.extraversion)
            ]

        },

        "Agreeableness": {

            "score": latest.agreeableness,

            "level": get_level(
                latest.agreeableness
            ),

            "description":
            descriptions["Agreeableness"][
                get_level(latest.agreeableness)
            ]

        },

        "Neuroticism": {

            "score": latest.neuroticism,

            "level": get_level(
                latest.neuroticism
            ),

            "description":
            descriptions["Neuroticism"][
                get_level(latest.neuroticism)
            ]

        }

    }

    # ==========================================
    # AI Summary
    # ==========================================

    prediction["summary"] = generate_summary(
        prediction
    )

    # ==========================================
    # Highest / Lowest Trait
    # ==========================================

    traits = {

        "Openness": latest.openness,

        "Conscientiousness":
        latest.conscientiousness,

        "Extraversion":
        latest.extraversion,

        "Agreeableness":
        latest.agreeableness,

        "Neuroticism":
        latest.neuroticism

    }

    highest_trait = max(
        traits,
        key=traits.get
    )

    lowest_trait = min(
        traits,
        key=traits.get
    )

    highest_score = round(
        traits[highest_trait],
        2
    )

    lowest_score = round(
        traits[lowest_trait],
        2
    )

    # ==========================================
    # Overall Score
    # ==========================================

    overall_score = round(

        (

            latest.openness +

            latest.conscientiousness +

            latest.extraversion +

            latest.agreeableness +

            latest.neuroticism

        ) / 5,

        2

    )

    # ==========================================
    # Render Dashboard
    # ==========================================

    return render_template(

    "dashboard.html",

    user=user,

    result=latest,

    prediction=prediction,

    highest_trait=highest_trait,
    highest_score=highest_score,

    lowest_trait=lowest_trait,
    lowest_score=lowest_score,

    overall_score=overall_score

)
# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!")

    return redirect(url_for("home"))



# ==========================================
# HOME
# ==========================================

# ==========================================
# HOME
# ==========================================

@app.route("/")
def home():
    return render_template("home.html")

# ================= ABOUT =================

@app.route("/about")
def about():
    return render_template("about.html")


# ================= ANALYZE =================

# ==========================================
# ANALYZE
# ==========================================

@app.route("/analyze", methods=["GET", "POST"])
def analyze():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        user_id = session["user_id"]

        analysis_type = request.form.get("analysis_type")

        # ==========================================
        # Username Analysis (API Not Connected)
        # ==========================================

        if analysis_type == "username":

            flash(
                "Username Analysis is currently unavailable because the X API is not connected yet. Please use Manual Posts Analysis."
            )

            return redirect(url_for("analyze"))

        # ==========================================
        # Manual Posts Analysis
        # ==========================================

        username = "Manual Posts"

        posts = request.form.get("posts", "")

        image = request.files.get("post_image")

        text_to_analyze = posts

        # OCR

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            image.save(image_path)

            result = reader.readtext(image_path)

            ocr_text = ""

            for item in result:
                ocr_text += item[1] + " "

            text_to_analyze = ocr_text

        text_to_analyze = text_to_analyze.strip()

        if text_to_analyze == "":

            flash("Please enter text or upload an image.")

            return redirect(url_for("analyze"))

        # ==========================================
        # AI Prediction
        # ==========================================

        prediction = predict_personality(text_to_analyze)

        # Save only scores in database

        new_prediction = Prediction(

            user_id=user_id,

            username=username,

            input_text=text_to_analyze,

            openness=prediction["Openness"]["score"],

            conscientiousness=prediction["Conscientiousness"]["score"],

            extraversion=prediction["Extraversion"]["score"],

            agreeableness=prediction["Agreeableness"]["score"],

            neuroticism=prediction["Neuroticism"]["score"]

        )

        db.session.add(new_prediction)

        db.session.commit()

        # Save full prediction in session

        session["prediction"] = prediction

        session["analysis_done"] = True

        flash("Analysis Completed Successfully!")

        return redirect(url_for("dashboard"))

    return render_template("analyze.html")
# ==========================================
# HISTORY
# ==========================================

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(url_for("login"))

    history_data = Prediction.query.filter_by(

        user_id=session["user_id"]

    ).order_by(

        Prediction.created_at.desc()

    ).all()

    return render_template(

        "history.html",

        history=history_data

    )
# ==========================================
# DELETE HISTORY
# ==========================================

@app.route("/delete_history/<int:prediction_id>", methods=["POST"])
def delete_history(prediction_id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    prediction = Prediction.query.filter_by(
        id=prediction_id,
        user_id=session["user_id"]
    ).first()

    if prediction:

        db.session.delete(prediction)
        db.session.commit()

        flash("History deleted successfully.")

    else:

        flash("Prediction not found.")

    return redirect(url_for("history"))
# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Password check
        if password != confirm_password:

            flash("Passwords do not match!", "danger")
            return redirect(url_for("register"))

        # Email already exists?
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:

            flash("Email already registered!", "danger")
            return redirect(url_for("register"))

        # Generate OTP
        otp = str(random.randint(100000, 999999))

        # Store temporary data in session
        session["register_name"] = name
        session["register_email"] = email
        session["register_password"] = generate_password_hash(password)
        session["register_otp"] = otp

        # Send OTP
        try:

            success = send_otp_email(
                email,
                otp,
                "register"
            )

            print("OTP SEND STATUS :", success)

        except Exception as e:

            print("REGISTER EMAIL ERROR :", e)

            success = False

        if success:

            flash("OTP sent to your email.", "success")
            return redirect(url_for("verify_register_otp"))

        else:

            flash("Failed to send OTP.", "danger")
            return redirect(url_for("register"))

    return render_template("register.html")

# ==========================================
# VERIFY REGISTER OTP
# ==========================================

@app.route("/verify-register-otp", methods=["GET", "POST"])
def verify_register_otp():

    # User direct page open karu naye
    if "register_otp" not in session:

        flash("Please register first!", "warning")

        return redirect(url_for("register"))

    if request.method == "POST":

        entered_otp = request.form.get("otp", "").strip()

        # OTP check
        if entered_otp != session["register_otp"]:

            flash("Invalid OTP!", "danger")

            return redirect(url_for("verify_register_otp"))

        try:

            # User create
            new_user = User(
                name=session["register_name"],
                email=session["register_email"],
                password=session["register_password"]
            )

            db.session.add(new_user)
            db.session.commit()

            # Session clear
            session.pop("register_name", None)
            session.pop("register_email", None)
            session.pop("register_password", None)
            session.pop("register_otp", None)

            flash("Registration Successful! Please Login.", "success")

            return redirect(url_for("login"))

        except Exception as e:

            db.session.rollback()

            print("====================================")
            print("REGISTER ERROR:")
            print(e)
            print("====================================")

            flash("Registration Failed!", "danger")

            return redirect(url_for("register"))

    return render_template("verify_register_otp.html")
# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].strip().lower()
        password = request.form["password"]

        print("\n========== LOGIN ==========")
        print("Email :", email)

        user = User.query.filter_by(email=email).first()

        if user:

            print("User Found :", user.name)
            print("Stored Hash :", user.password)

            if check_password_hash(user.password, password):

                print("✅ Password Matched")

                session["user_id"] = user.id
                session["user_name"] = user.name
                session["analysis_done"] = False

                flash("Login Successful!", "success")

                return redirect(url_for("analyze"))

            else:

                print("❌ Wrong Password")

                flash("Invalid Email or Password", "danger")

                return redirect(url_for("login"))

        else:

            print("❌ User Not Found")

            flash("Email not registered!", "danger")

            return redirect(url_for("register"))

    return render_template("login.html")
# ==========================================
# PROFILE
# ==========================================
# ==========================================
# PROFILE
# ==========================================

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    latest = Prediction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Prediction.created_at.desc()
    ).first()

    return render_template(
        "profile.html",
        user=user,
        latest=latest
    )
    
# ==========================================
# EDIT PROFILE
# ==========================================

@app.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:

        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    if request.method == "POST":

        user.name = request.form["name"]

        image = request.files.get("photo")

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            image.save(

                os.path.join(

                    app.config["UPLOAD_FOLDER"],

                    filename

                )

            )

            user.profile_photo = filename

        db.session.commit()

        flash("Profile Updated Successfully!")

        return redirect(url_for("profile"))

    return render_template(

        "edit_profile.html",

        user=user

    )
# ==========================================
# DOWNLOAD REPORT
# ==========================================

@app.route("/download_report")
def download_report():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.get(session["user_id"])

    result = Prediction.query.filter_by(
        user_id=session["user_id"]
    ).order_by(
        Prediction.created_at.desc()
    ).first()

    if result is None:

        flash("No report found!")

        return redirect(url_for("dashboard"))

    # --------------------------------------
    # Rebuild Prediction
    # --------------------------------------

    prediction = {

        "Openness": {
            "score": result.openness,
            "level": get_level(result.openness),
            "description": descriptions["Openness"][get_level(result.openness)]
        },

        "Conscientiousness": {
            "score": result.conscientiousness,
            "level": get_level(result.conscientiousness),
            "description": descriptions["Conscientiousness"][get_level(result.conscientiousness)]
        },

        "Extraversion": {
            "score": result.extraversion,
            "level": get_level(result.extraversion),
            "description": descriptions["Extraversion"][get_level(result.extraversion)]
        },

        "Agreeableness": {
            "score": result.agreeableness,
            "level": get_level(result.agreeableness),
            "description": descriptions["Agreeableness"][get_level(result.agreeableness)]
        },

        "Neuroticism": {
            "score": result.neuroticism,
            "level": get_level(result.neuroticism),
            "description": descriptions["Neuroticism"][get_level(result.neuroticism)]
        }

    }

    prediction["summary"] = generate_summary(prediction)

    traits = {

        "Openness": result.openness,
        "Conscientiousness": result.conscientiousness,
        "Extraversion": result.extraversion,
        "Agreeableness": result.agreeableness,
        "Neuroticism": result.neuroticism

    }

    highest_trait = max(traits, key=traits.get)
    lowest_trait = min(traits, key=traits.get)

    overall_score = round(sum(traits.values()) / 5, 2)

    # --------------------------------------
    # Create PDF
    # --------------------------------------

    pdf_name = "Personality_Report.pdf"

    c = canvas.Canvas(pdf_name)

    width, height = 595, 842

    y = 810

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "AI Personality Prediction Report")

    y -= 40

    c.setFont("Helvetica", 12)

    c.drawString(50, y, f"Name : {user.name}")
    y -= 20

    c.drawString(50, y, f"Username : {result.username}")
    y -= 20

    c.drawString(
        50,
        y,
        f"Generated On : {result.created_at.strftime('%d-%m-%Y %I:%M %p')}"
    )

    y -= 35

    c.setFont("Helvetica-Bold", 15)
    c.drawString(50, y, "OCEAN Personality Scores")

    y -= 25

    c.setFont("Helvetica", 12)

    for trait in prediction:

        if trait == "summary":
            continue

        c.drawString(
            60,
            y,
            f"{trait} : {prediction[trait]['score']}/5 ({prediction[trait]['level']})"
        )

        y -= 20

    y -= 10

    c.setFont("Helvetica-Bold", 15)

    c.drawString(50, y, "Analysis Insights")

    y -= 25

    c.setFont("Helvetica", 12)

    c.drawString(
        60,
        y,
        f"Highest Trait : {highest_trait} ({traits[highest_trait]}/5)"
    )

    y -= 20

    c.drawString(
        60,
        y,
        f"Lowest Trait : {lowest_trait} ({traits[lowest_trait]}/5)"
    )

    y -= 20

    c.drawString(
        60,
        y,
        f"Overall AI Score : {overall_score}/5"
    )

    y -= 35

    c.setFont("Helvetica-Bold", 15)

    c.drawString(50, y, "AI Personality Summary")

    y -= 25

    c.setFont("Helvetica", 11)

    text = c.beginText(60, y)
    text.setLeading(18)

    for line in prediction["summary"].split("."):

        line = line.strip()

        if line:
            text.textLine(line + ".")

    c.drawText(text)

    y = text.getY() - 20

    c.setFont("Helvetica-Bold", 15)

    c.drawString(50, y, "Trait Descriptions")

    y -= 25

    c.setFont("Helvetica", 10)

    for trait in prediction:

        if trait == "summary":
            continue

        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, y, trait)

        y -= 15

        c.setFont("Helvetica", 10)

        txt = c.beginText(60, y)
        txt.setLeading(14)

        words = prediction[trait]["description"].split()

        line = ""

        for word in words:

            if len(line + word) < 90:

                line += word + " "

            else:

                txt.textLine(line)

                line = word + " "

        txt.textLine(line)

        c.drawText(txt)

        y = txt.getY() - 20

        if y < 70:

            c.showPage()

            y = 800

    c.save()

    return send_file(
        pdf_name,
        as_attachment=True
    )
# ==========================================
# GOOGLE LOGIN
# ==========================================

@app.route("/google")
def google_login():

    redirect_uri = url_for(

        "authorize",

        _external=True

    )

    return google.authorize_redirect(

        redirect_uri
    )

# ==========================================
# FORGOT PASSWORD
# ==========================================

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        email = request.form["email"].strip().lower()

        user = User.query.filter_by(email=email).first()

        if not user:

            flash("Email not registered!")

            return redirect(url_for("forgot_password"))

        otp = str(random.randint(100000,999999))

        session["reset_otp"] = otp

        session["reset_email"] = email

        success = send_otp_email(
           email,
           otp,
           "forgot"
)
        if success:

            flash("OTP sent successfully!")

            return redirect(url_for("verify_otp"))

        else:

            flash("Failed to send OTP!")

            return redirect(url_for("forgot_password"))

    return render_template("forgot_password.html")
# ==========================================
# VERIFY OTP
# ==========================================

@app.route("/verify-otp", methods=["GET", "POST"])
def verify_otp():

    if request.method == "POST":

        entered_otp = request.form["otp"].strip()

        if entered_otp == session.get("reset_otp"):

            flash("OTP Verified Successfully!")

            return redirect(url_for("reset_password"))

        else:

            flash("Invalid OTP!")

            return redirect(url_for("verify_otp"))

    return render_template("verify_otp.html")
# ==========================================
# RESET PASSWORD
# ==========================================

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():

    if "reset_email" not in session:
        return redirect(url_for("forgot_password"))

    if request.method == "POST":

        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:

            flash("Passwords do not match!")

            return redirect(url_for("reset_password"))

        user = User.query.filter_by(
            email=session["reset_email"]
        ).first()

        if user:

            user.password = generate_password_hash(password)

            db.session.commit()
            print("\n===== PASSWORD UPDATED =====")
            print("Email :", user.email)
            print("Hash :", user.password)
            

        session.pop("reset_email", None)
        session.pop("reset_otp", None)

        flash("Password Reset Successfully!")

        return redirect(url_for("login"))

    return render_template("reset_password.html")
# ==========================================
# GOOGLE CALLBACK
# ==========================================

@app.route("/authorize")
def authorize():

    token = google.authorize_access_token()

    user_info = token["userinfo"]

    email = user_info["email"]

    name = user_info["name"]

    user = User.query.filter_by(

        email=email

    ).first()

    if not user:

        user = User(

            name=name,

            email=email,

            password="google_login"

        )

        db.session.add(user)

        db.session.commit()

    session["user_id"] = user.id

    session["user_name"] = user.name

    flash("Google Login Successful!")

    return redirect(

        url_for("dashboard")

    )
    
 # ================= RUN =================
if __name__ == "__main__":

   app.run(debug=True, use_reloader=False)