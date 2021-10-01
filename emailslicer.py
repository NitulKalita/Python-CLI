email = input("What is your email address?: ")

usrname = email[:email.index("@")]

domainname = email[email.index("@")+1:]

sliced = "Username is '{}' and Domain name is '{}'".format(usrname, domainname)

print(sliced)