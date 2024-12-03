from flask import Flask,render_template,request
import random
from pymysql import connect
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
verifyotp = "0"

db_config = {
    'host' : 'localhost',
    'database' : 'royalshop',
    'user' : 'root',
    'password' : 'root'
}
app = Flask(__name__)

@app.route("/")
def landing():
    return render_template("home.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerdata",methods=["POST","GET"])
def registerdata():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        cpassword = request.form['confirm-password']
        if password == cpassword:
            otp = random.randint(111111,999999)
            global verifyotp
            verifyotp = str(otp)
            print(verifyotp)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            mailusername = "saivardhan@codegnan.com"
            mailpassword = "hyao dyqd lmlf bbgl"
            from_email = "saivardhan@codegnan.com"
            to_email = email
            subject = "OTP for Verification"
            body = f"The OTP for login is {verifyotp}"

            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['subject'] = subject
            msg.attach(MIMEText(body,'plain'))

            server = smtplib.SMTP(smtp_server,smtp_port)
            server.starttls()
            server.login(mailusername,mailpassword)
            server.send_message(msg)
            server.quit()
            return render_template("verifyemail.html",name=name,username=username,email=email,mobile=mobile,password=password)
        else:
            return "Make sure password and confirm password to be same"
    else:
        return "<h3 style='color:red'>Data got in wrong manner</h3>"
    
@app.route("/verifyemail",methods=["POST","GET"])
def verifyemail():
    if request.method == "POST":
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        otp = request.form['otp']
        if otp == verifyotp:
            try:
                conn = connect(**db_config)
                cursor = conn.cursor()
                q = "INSERT INTO USERS VALUES (%s,%s,%s,%s,%s)"
                cursor.execute(q,(name,username,email,mobile,password))
                conn.commit()
            except:
                return "Error Occured while storing data in database or Username alreary exists"
            else:
                return render_template("login.html")
        else:
            return "wrong otp"
    else:
        return "<h3 style='color:red'>Data got in wrong manner</h3>"
@app.route("/userlogin",methods = ["POST","GET"])
def userlogin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        try:
            conn = connect(**db_config)
            cursor = conn.cursor()
            q = "SELECT * FROM USERS WHERE USERNAME = (%s)"
            cursor.execute(q,(username))
            row = cursor.fetchone()
            if row == None:
                return "User Does not Exists, Create account first !"
            else:
                if row[4] != password:
                    return "Incorrect Password !"
                else:
                    return render_template("userhome.html",name=username)
        except:
            return "Error Occured while retriving the data"

    else:
        return "Data Occured in incorrect way"
if __name__ == "__main__":
    app.run(port=5021)