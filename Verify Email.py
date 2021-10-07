from verify_email import verify_email

enter = input("Enter the email to verify: ")

verify = verify_email(enter)

if verify == False:
    print("Invalid Email")
else:
    print("Valid email")