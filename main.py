from flask import Flask, render_template, request
import requests
from postlick import Postclick
import smtplib

def send_msg(msg):
    fromaddr = 'ENTER YOUR EMAIL '
    toaddrs = 'ENTER RECEIVER EMAIL'
    username = 'ENTER YOUR EMAIL '
    password = 'ENTER YOUR PASSWORD '
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


app = Flask(__name__)

blog_post_url = 'https://api.npoint.io/deaf557de3ea833c4e57'
blog_post = requests.get(blog_post_url).json()

list_of_users = []

post_list = []
for n in blog_post:
    blog_stuff = Postclick(n["id"], n["title"], n["subtitle"], n["body"])
    post_list.append(blog_stuff)


@app.route("/")
def home():
    blogs = blog_post
    return render_template('index.html', posts=blogs)


@app.route("/index.html")
def come_home():
    blogs = blog_post
    return render_template('index.html', posts=blogs)


@app.route("/contact.html", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        data = request.form
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        message = data["message"]
        msg_contact = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
        send_msg(msg_contact)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


@app.route("/about.html")
def about():
    return render_template('about.html')


@app.route("/post.html/<int:blog_p>")
def get_post(blog_p):
    requested_post = None
    for g in post_list:
        if g.id == blog_p:
            requested_post = g
    return render_template('post.html', post=requested_post)


#
# @app.route("/form_entry", methods=['POST', 'GET'])
# def form_entry():
#     data = request.form
#     print(data["name"])
#     print(data["email"])
#     print(data["phone"])
#     print(data["message"])
#     return "<h1>Successfully sent your message</h1>"


if __name__ == "__main__":
    app.run(debug=True)
