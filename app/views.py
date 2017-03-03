from app import app
import onetimepass as otp
import time

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/user/<string:username>')
def show_user_alon(username):
    # show the user profile for that user
    if username.lower()=="alon" :
        return("Winner!!!")

    else:
        return ('User ' + username + " not important")

@app.route('/token/<string:token>')
def check_token(token):
    my_secret = 'UGPQCD3EQHRJEZMG'
    my_token = otp.get_totp(my_secret)

    IntLen          = 30 #dont change
    window_bi_size  = 3

    page_answer     = ""

    accepted_tokens = [otp.get_totp(my_secret, clock=time.time()-d, as_string=True ) \
                       for d in range(-IntLen*window_bi_size,IntLen*window_bi_size+1,IntLen)]

    page_answer += "\r\n"
    page_answer += str(accepted_tokens)

    if (str(token) in accepted_tokens):
        page_answer += "\r\nWinner Winner chicken dinner!!!"
        return page_answer
        #return ("Winner Winner chicken dinner!!!")
    else:
        return page_answer
        #return("given {a} calc {b}".format(a=token, b=my_token))
        #return("given: " + str(token) + "\ncalculated: " + str(my_token))

    #print "given %d calc %d" (token, my_token)
