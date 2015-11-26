from flask import Flask, request
from feedline import feedline
import re

# Create flask instance
app = Flask(__name__)

@app.route('/')
def my_form():
    """
    Returns (creates) html of flask webapp of main page: 127.0.0.1, port 5000
    """
    html = """
    <html>
       <head>
           <title>MyPython WebApp</title>
       </head>
       <body>
           <div id="container">
               <div class="title">
                   <h1>MyPython WebApp</h1>
               </div>
          </div>
          <div id="content">
            <form action="." method="POST">
              <input type="text" name="text">
              <input type="submit" name="my-form" value="Send">
            </form>
            </div>
       </body>
    </html>"""
    return html

@app.route('/', methods=['POST'])
def my_form_post():
    """
    Returns (creates) html of flask webapp when user has input some
    string to be validated by feedline(). Also, displays earlier input
    and output.
    """
    all_output = feedline(request.form['text'],True)
    all_output = re.sub('\n','<br>',all_output) # Change \n to <br>
    html = """
    <html>
       <head>
           <title>MyPython WebApp</title>
       </head>
       <body>
           <div id="container">
               <div class="title">
                   <h1>MyPython WebApp</h1>
               </div>
          </div>
          <p>%s
          </p>
          <div id="content">
            <form action="." method="POST">
              <input type="text" name="text">
              <input type="submit" name="my-form" value="Send">
            </form>
            </div>
       </body>
    </html>""" %(all_output)
    return html


if __name__ == '__main__':
    app.run()
