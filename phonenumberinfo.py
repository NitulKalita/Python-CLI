import phonenumbers
from phonenumbers import carrier, geocoder, timezone

phone_num = input("Enter Phone Number with country code - ")
phone_num = phonenumbers.parse(phone_num)

# timezone
print("Time Zone - ", timezone.time_zones_for_number(phone_num))

# carrier
print("Carrier Name - ", carrier.name_for_number(phone_num, "en"))

# region info
print("Region - ", geocoder.description_for_number(phone_num, "en"))

# validate
print("Valid Phone Number - ", phonenumbers.is_valid_number(phone_num))