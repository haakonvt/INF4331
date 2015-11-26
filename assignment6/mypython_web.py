from flask import Flask, request, render_template, url_for
from feedline import feedline
import re

app = Flask(__name__)

@app.route('/')
def my_form():
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
    current_output = feedline(request.form['text'])
    current_output = re.sub('\n','<br>',current_output) # Change \n to <br>
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
    </html>""" %(current_output)
    return html


if __name__ == '__main__':
    app.run(debug=True)
