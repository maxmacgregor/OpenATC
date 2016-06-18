import json
with open("userinfo.json") as conffile:
    userinfo = json.load(conffile)

# No real better way...
card_cvv = userinfo["card_cvv"]
card_exp_month = userinfo["card_exp_month"]
card_exp_year = userinfo["card_exp_year"]
card_number = userinfo["card_number"]
card_type = userinfo["card_type"]
email = userinfo["email"]
first_name = userinfo["first_name"]
last_name = userinfo["last_name"]
phone_number = userinfo["phone_number"]
shipping_address_1 = userinfo["shipping_address_1"]
shipping_address_2 = userinfo["shipping_address_2"]
shipping_apt_suite = userinfo["shipping_apt_suite"]
shipping_city = userinfo["shipping_city"]
shipping_state = userinfo["shipping_state"]
shipping_state_abbrv = userinfo["shipping_state_abbrv"]
shipping_zip = userinfo["shipping_zip"]

