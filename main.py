import pandas as pd


df = pd.read_csv("hotels.csv")
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pd.read_csv("card_security.csv", dtype=str)


class User:
    pass


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True

        return False


class SpaHotel(Hotel):
    def book(self):
        """This does nothing but is a requirement for so-called 'student-project'"""
        pass



class Ticket:
    def __init__(self, customer_name, hotel_object):
        self.name = customer_name
        self.hotel = hotel_object

    def generate_ticket(self):
        return f"""
        Thank you for the reservation.
        Your ticket: 
        Name: {self.name}
        Hotel: {self.hotel.name}
        TicketID: {self.hotel.hotel_id}{str(self.name).lower()}"""


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.name = customer_name
        self.hotel = hotel_object

    def generate_ticket(self):
        return f"""
        Thank you for the SPA reservation.
        Your ticket: 
        Name: {self.name}
        Hotel: {self.hotel.name}"""


class CreditCard:
    def __init__(self, card_number):
        self.card_number = card_number

    def validate(self, exp_date, holder_name, cvv_cvc):
        card_data = {"number": self.card_number,
                     "expiration": exp_date,
                     "cvc": cvv_cvc,
                     "holder": holder_name}
        if card_data in df_cards:
            return True
        return False


class SecureCreditCard(CreditCard):
    def authenticate(self, password):
        card_password = df_cards_security.loc[df_cards_security["number"] == str(self.card_number), "password"].squeeze()
        if card_password == password:
            return True
        return False


print(df)
hotel_id = int(input("Enter the id of the hotel: "))
hotel = SpaHotel(hotel_id)

if hotel.available():
    number = input("Please enter your credit/debit card number: ")
    credit_card = SecureCreditCard(number)
    expiration = input("Please enter expiration date as mm/yy: ")
    holder = input("Please enter holder name and surname: ").upper()
    cvc = input("Please enter cvc/cvv: ")
    if credit_card.validate(expiration, holder, cvc):
        password = input("Please enter card password: ")
        if credit_card.authenticate(password):
            hotel.book()
            name = input("Enter your name: ").title()
            reservation = Ticket(name, hotel)
            print(reservation.generate_ticket())
            choice = input("Do you want to book a SPA package? Enter yes or no: ")
            if choice.lower() == "yes":
                spa_reservation = SpaTicket(name, hotel)
                print(spa_reservation.generate_ticket())
        else:
            print("Credit/Debit card authentication failed.")
    else:
        print("Credit/Debit card validation failed.")
else:
    print("Hotel is not available.")