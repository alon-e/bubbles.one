
def getSendMessPHP(nl):
    Ans  = ''
    Ans += '<form action="/send" method="post">\n'
    i=0
    for n in nl:
        Ans += '<input type="checkbox" class="form" name="cb_list' + str(i) + '" value="' + str(n) + '" />' + str(n) + '<br />\n'
        #Ans += '<input type="checkbox" class="form" name="cb_list[]" value="' + str(i) + '" />' + str(n) + '<br />\n'
        #debug: print Ans
        i+=1
    Ans += 'Enter Your Message: <input type="text" name="mtext"><br>\n'
    Ans += '<input type="submit" value="Submit">\n'
    Ans += '</form>'
    return Ans

def getSimpleMessPHP():
    Ans  = ''
    Ans += '<form action="/action_page.php">\n'
    #Ans += '<input type="checkbox" name="formDoor[]" value="A" />Acorn Building<br />\n'
    Ans += 'Enter Your Message: <input type="text" name="mtext"><br>\n'
    Ans += '<input type="submit" value="Submit">\n'
    Ans += '</form>'
    return Ans
