from app import app
import onetimepass as otp

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route('/user/<string:username>')
def show_user_profile(username):
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

    page_answer     = "aaa"

    accepted_tokens = [otp.get_totp(my_secret, clock=time.time()-d ) \
                       for d in range(-IntLen*window_bi_size,IntLen*window_bi_size+1,IntLen)]

    if (str(token)==str(my_token)):
        return ("Winner Winner chicken dinner!!!")
    else:
        return("given {a} calc {b}".format(a=token, b=my_token))
        #return("given: " + str(token) + "\ncalculated: " + str(my_token))

    #print "given %d calc %d" (token, my_token)
