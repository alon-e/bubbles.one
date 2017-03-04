from app import app
import onetimepass as otp
import time
import Messages
import HTMLer
from flask import request

All_Messages = Messages.Messages()
All_Messages.add_user('alon' , 'RPPYE6LOX57FEJIS', 'nola')
All_Messages.add_user('yuval', 'SPC4ABXI23HDGSZQ', 'y23')
All_Messages.add_user('bar'  , 'TKYQVOG4I2ZHIGP2', 'bar')


#my_secret = "UGPQCD3EQHRJEZMG"

net_names = []

@app.route('/get/<string:net_list>', methods=['GET', 'POST'])
def get_form(net_list):
    global net_names
    if request.method == 'GET':
        ns = str(net_list)
        nl = ns.split(';')
        net_names = nl
        return HTMLer.getSendMessPHP(nl)
    elif request.method == 'POST':
        pass
        #return "321312"
    else:
        pass

@app.route('/send', methods=['GET', 'POST'])
def send_form():
    global net_names
    #print "here"
    if request.method == 'POST':
        mtext   = str(request.form['mtext'])
        print "here1"
        i=0
        ch_list=[]
        print str(net_names)
        for nn in net_names:
            #print nn
            try:
                ch = str(request.form['cb_list'+str(i)]) #Eq 1 if chbox checked, excepts on unchecked
            except:
                ch = "NO"

            #print ch
            if (ch!="NO"):
                ch_list += [nn]

            i += 1

        for c in ch_list:
            cs = c.split(".")
            assert(len(cs) == 2)  #token.user -- maybe token.user.bubble.one
            (token,user) = c.split(".")
            ans = Publish(user, token, mtext)
            print ans

        return "going to send: '" + mtext + "' to:" + str(ch_list)

    #return str(info)


@app.route('/')
@app.route('/index')
def index():
    return "Hello and welcome to bubble.one server (Hackaton demonstration)"

@app.route('/help')
def help_page():
    Ans  = ""
    Ans += "<p>" + "Hello and welcome to bubble.one server (Hackaton demonstration)" + "</p>"
    Ans += "<p>" + "You can use: tick, read/user/pass, read_all, publish/user/token/message " + "</p>"
    Ans += "<p>" + "You can also try: send, get " + "</p>"
    return Ans

@app.route('/tick')
def tick():
    Ans = ""
    for user in All_Messages.get_users():
        Ans += "<p>" + str(user) + "</p>"
        otp_window = All_Messages.get_otp_window(str(user))
        Ans += "<p>" + str(otp_window) + "</p>"

    return Ans

@app.route('/read_all')
def ReadAllUserMessages():
    ans = ""
    for u in All_Messages.get_users():
        ans +=  ReadMyMessages(u,All_Messages.Passwords[u])

    return ans

@app.route('/read/<string:user_name>/<string:password>')
def ReadMyMessages(user_name, password):
    Ans   = ""
    Wrong = "Sorry, wrong username\password"

    if not(str(user_name) in All_Messages.get_users()):
        return Wrong
    if (str(All_Messages.Passwords[str(user_name)]) != str(password)):
        return Wrong

    my_mess = All_Messages.get_messages(str(user_name), str(password))
    if (my_mess==All_Messages.WrongPassword):
        return my_mess #print wrong password
    else:
        Ans += "<p>" + "Hello {u}, You have {NoM} messages:".format(u=str(user_name), NoM=len(my_mess)) + "</p>"
        for m in my_mess:
            Ans += "<p>" + str(m) + "</p>"
        return Ans

@app.route('/publish/<string:user_name>/<string:gotten_token>/<string:message>')
def Publish(user_name, gotten_token, message):
    assert(str(user_name) in All_Messages.get_users())
    time_on_server = time.time()
    otp_window = All_Messages.get_otp_window(str(user_name))
    if str(gotten_token) in otp_window:
        All_Messages.add_message(str(user_name), str(message), str(gotten_token), time_on_server)
        return "Accepted!!"
    else:
        return "<p>" + "Rejected! user_name\\token not valid!" + "</p>"
        #return "Rejected! token {a} not in window {b}".format(a=str(gotten_token), b=str(otp_window))

'''
@app.route('/user/<string:username>')
def show_user_alon(username):
    # show the user profile for that user
    if username.lower()=="alon" :
        return("Alon is the key")

    else:
        return ('User ' + username + ", come back when your alon")


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