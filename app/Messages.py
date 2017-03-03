import onetimepass as otp
import time

class Messages:
    def __init__(self):
        self.ByUsers       = {}  # user(string) -- Messages(list)
        self.PrivateKeys   = {}  # user(string) -- PrivateKey(string)
        self.Passwords     = {}  # user(string) -- Password(string)

        self.WrongPassword = "WRONG PASSWORD"

    def add_user(self, user_name, private_key, password): #adding existing user will delete all messages
        assert(len(str(user_name))<12)          #Convention
        self.ByUsers[str(user_name)]     = []
        self.PrivateKeys[str(user_name)] = str(private_key)
        self.Passwords[str(user_name)]   = str(password)

    def add_message(self, user_name, text, token, time): #Add Publisher user_name
        assert(self.ByUsers.has_key(str(user_name)))
        old_m_list = self.ByUsers[str(user_name)]
        new_entry = {}
        new_entry['text']  = str(text)
        new_entry['token'] = str(token)
        new_entry['time']  = time
        old_m_list.append(new_entry) #now it's new :)
        self.ByUsers[user_name] = old_m_list

    def get_messages(self, user_name, password):
        assert (self.ByUsers.has_key(str(user_name)))
        if self.Passwords[str(user_name)]==str(password):
            return self.ByUsers[str(user_name)]
        else:
            return self.WrongPassword

    def get_users(self):
        return self.ByUsers.keys()

    def get_otp_window(self, user_name):
        assert(self.ByUsers.has_key(str(user_name)))
        IntLen = 30         # don't change
        window_bi_size = 3  # should be configurable later
        otp_window = [otp.get_totp(self.PrivateKeys[str(user_name)], clock=time.time() - d, as_string=True) \
         for d in range(-IntLen * window_bi_size, IntLen * window_bi_size + 1, IntLen)]

        return otp_window
