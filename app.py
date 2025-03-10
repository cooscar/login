from flask import Flask, request, render_template, flash, redirect
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"


if not os.path.exists("submissions"):
    os.makedirs("submissions")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/page2")
def page2():
    return render_template("page2.html")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("email")
    password = request.form.get("password")

    if not name:
        flash("Error: email cannot be empty.", "error")
        return redirect("/")

    filename = f"submissions/{name}.txt"

    if os.path.exists(filename):
        flash("Error: email already in use. Please choose another one.", "error")
        return redirect("/")

    with open(filename, "w") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Password: {password}\n")

    flash("Sign-up submitted successfully!", "success")
    return redirect("/")


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("email")
    password = request.form.get("password")
    
    filename = f"submissions/{name}.txt"

    if not os.path.exists(filename):
        flash("Error: Email not found. Please sign up first.", "error")
        return redirect("/page2")

    with open(filename, "r") as file:
        lines = file.readlines()
        stored_name = lines[0].strip().split(": ")[1]  
        stored_password = lines[1].strip().split(": ")[1]  

    if name == stored_name and password == stored_password:
        flash("Login successful!", "success")
        return redirect("/")  
    else:
        flash("Error: Incorrect password.", "error")
        return redirect("/page2")  

if __name__ == "__main__":
    app.run(debug=True)
