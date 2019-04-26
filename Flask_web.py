from flask import Flask, render_template, request, url_for
import os
from nltk_process import *
#from prep_functions import *

artist=''
song=''
app = Flask(__name__)
album_folder = os.path.join('static','images')
file = 'static/images/'
im1= file+'Eminem0.jpg'
im2= file+'Eminem1.jpg'
im3= file+'Eminem2.jpg'

@app.route("/")
def home():
    #if request.method=='POST':
    #result = request.p
    #data = start()

    return render_template('index.html', ui1=im1, ui2=im2, ui3=im3 )

@app.route("/", methods=['POST','GET'])
def get():


    artist = request.form['artist']
    song = request.form['song']
    song = int(song)
    #data_ = request.form['area']

    #lines = start(artist, song)

    lines=[]
    lines = start(artist,song)
    print(lines)
    no=0
    for i in lines:

        img_name = artist+str(no)+'.jpg'
        no+=1

    full_file = file+img_name


    lines = '\n'.join(lines)
    #lines = figure(lines)



#lines.format(request.form['area'])


    return  render_template('index.html',data= lines, user_image=full_file, ui1=im1, ui2=im2, ui3=im3)



if __name__ =='__main__':
    app.run(debug=True)






