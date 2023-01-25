import pandas as pd


df = pd.read_csv("hotels.csv")


class User:
    pass


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
        """Book hotel if available"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True

        return False


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


print(df)
hotel_id = int(input("Enter the id of the hotel: "))
hotel = Hotel(hotel_id)

if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation = Ticket(name, hotel)
    print(reservation.generate_ticket())
else:
    print("Hotel is not available.")