from app import app
import onetimepass as otp
import time
import Messages

All_Messages = Messages.Messages()
All_Messages.add_user('alon' , 'UGPQCD3EQHRJEZMG')
All_Messages.add_user('yuval', 'YK3RVQE5H4W5XIZ4')

my_secret = "UGPQCD3EQHRJEZMG"

@app.route('/')
@app.route('/index')
def index():
    Ans = ""
    for user in All_Messages.get_users():
        Ans += "<p>" + str(user) + "</p>"
        otp_window = All_Messages.get_otp_window(str(user))
        Ans += "<p>" + str(otp_window) + "</p>"

    return Ans

@app.route('/read/<string:user_name>/<string:next_token>')
def ReadMyMessages(user_name, next_token):
    assert (str(user_name) in All_Messages.get_users())
    Ans = ""
    my_mess = All_Messages.get_messages(str(user_name))
    for m in my_mess:
        Ans += "<p>" + str(m) + "</p>"
    return Ans

@app.route('/publish/<string:gotten_token>/<string:user_name>/<string:message>')
def Publish(gotten_token, user_name , message):
    assert(str(user_name) in All_Messages.get_users())
    time_on_server = time.time()
    otp_window = All_Messages.get_otp_window(str(user_name))
    if str(gotten_token) in otp_window:
        All_Messages.add_message(str(user_name), str(message), str(gotten_token), time_on_server)
        return "Accepted!!"
    else:
        return "Rejected! token {a} not in window {b}".format(a=str(gotten_token), b=str(otp_window))

@app.route('/user/<string:username>')
def show_user_alon(username):
    # show the user profile for that user
    if username.lower()=="alon" :
        return("Alon is the key")

    else:
        return ('User ' + username + ", come back when your alon")

'''
@app.route('/token/<string:token>')
def check_token(token):
    my_token = otp.get_totp(my_secret)

    IntLen          = 30 #dont change
    window_bi_size  = 3

    page_answer     = ""

    #accepted_tokens = [otp.get_totp(my_secret, clock=time.time()-d, as_string=True ) \
    #                   for d in range(-IntLen*window_bi_size,IntLen*window_bi_size+1,IntLen)]

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
'''