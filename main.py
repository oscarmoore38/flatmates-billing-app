# Import statements
import datetime
import calendar
from fpdf import FPDF
from time import strftime
from datetime import datetime
from datetime import date


class Flatmate:
    """Creates flatmates"""

    def __init__(self, name, days_in_house):
        """ Constructor for Flatmates class
        :param name: (str) Name of flatmate
        :param days_in_house: (int) Number of days in house
        """
        self._name = name
        self._days_in_house = days_in_house

    def get_name(self):
        """Returns the name of flatmate"""
        return self._name

    def get_days_in_house(self):
        """Returns the days in house"""
        return self._days_in_house


class CreateBill:
    """ Creates bill and handles calculating amount owed """

    def __init__(self, amount, period):
        """ Constructor for class
        :param amount: (float) total amount of bill for period
        :param period: (str) period for billing expressed as mm/yyyy
        """
        self._period = period
        self._amount = amount
        self._bill_log = {}
        self._flatmate_log = {}

    def get_period(self):
        """Returns current billing period"""
        return self._period

    def get_amount(self):
        """Returns current amount owed"""
        return self._amount

    def get_bill_log(self):
        """Returns bill log"""
        return self._bill_log

    def log_bill(self, flatmate):
        """logs the current bill
        :param flatmate: flatmate object
        """
        self.flatmate_log[flatmate.get_name()] = flatmate.get_days_in_house()
        self._bill_log['Date period'] = self.get_period()
        self._bill_log['Amount'] = self.get_amount()
        self._bill_log['Flatmates'] = self.flatmate_log

    def bill_pay(self):
        """Calculates how much is owed"""
        total = 0
        for name, day in self._bill_log['Flatmates'].items():
            total += day

        for name, day in self._bill_log['Flatmates'].items():
            amount_owed = self.math_magic(total, day)
            print(f"{name} stayed in the flat {day} days and owes ${amount_owed} of the ${self.get_amount()} total.")

    def math_magic(self, total, day):
        """Method for calculating how much people owe"""
        div = (day / total)
        amount_owed = self._amount * div
        return round(amount_owed, 2)


class BillHistory:
    """Class to log bill history"""
    def __init__(self):
        """ Constructor for class """
        self._db = {}

    def history(self):
        """Returns log of bill history"""
        return self.db

    def log_history(self, bill):
        """Logs bill history"""
        self.db[bill.get_period()] = bill.get_bill_log()


class PdfReport:
    """Creates a Pdf file that contains data about the flatmates such as their names,their due amounts and the period
    of the bill."""

    def generate(self, bill):
        """generates PDF doc"""

        # Creates a pdf file.
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Header
        pdf.set_font(family='Courier', style='BU', size=22)
        pdf.cell(w=0, h=80, txt='Flatmates Bill', border=0, align='C', ln=1)

        # Body
        # Main header 1 - 'Period - XX/XXXX'
        pdf.set_font(family='Courier', style="BU", size=12)
        pdf.cell(w=0, h=40, txt=f'Period: {bill.get_period()}', border=1, align='C', ln=1)

        # Main header 2 - 'Amount due'
        pdf.set_font(family='Courier', style="B", size=10)
        pdf.cell(w=0, h=40, txt=f'Total amount due: ${bill.get_amount()}', border=1, align='L', ln=1)

        # Body text - 'Names and amount due'
        bill_dict = bill.get_bill_log()
        total = 0

        # Have bill_pay function return name + amount owed. Then cut this repeated code out.
        for name, day in bill_dict['Flatmates'].items():
            total += day

        for name, day in bill_dict['Flatmates'].items():
            amount_owed = bill.math_magic(total, day)
            flatmate_name = name
            pdf.set_font(family='Courier', size=10)
            pdf.cell(w=0, h=40, txt=f'Name: {flatmate_name} -- amount due is ${amount_owed}',
                     border=1, align='L', ln=1)

        # Time body
        pdf.set_font(family='Courier', style="I", size=6)
        pdf.cell(w=0, h=40, txt=f'Report created on: {strftime("%a, %d, %b, %Y, %H:%M")}',
                 border=1, align='L', ln=1)

        # Filename output
        pdf.output('Invoice.pdf')


# Functions for main script - adds dates, amount owed, and flatmates.
def date_selection():
    """Function used to select dates for bill objects"""
    today_date = datetime.now().strftime('%m/%Y')
    while True:
        # Checks if user would like to select current month and year.
        user_date = input(f"Is this bill for {today_date}? [Y/N]: ")
        user_date = user_date.lower()

        if user_date == 'y' or user_date == 'yes':
            user_date = today_date
            return user_date

        if user_date == 'n' or user_date == 'no':
            while True:
                other_user_input_month = int(
                    input("Please enter the desired month for your bill in XX integer format: "))
                other_user_input_year = int(
                    input("Please enter the desired year for your bill in XXXX integer format: "))
                try:
                    new_user_date = date(other_user_input_year, other_user_input_month, 1).strftime('%m/%Y')
                except ValueError:
                    print("Date or time formats are incorrect. Please try again.")
                    continue

                confirm = input(f"Is this date correct? {new_user_date}: [Y/N]: ")
                confirm = confirm.lower()

                if confirm == 'y' or confirm == 'yes':
                    user_date = new_user_date
                    return user_date
                else:
                    print('Ok, please re-enter your desired month and year')
                    continue
            return False
        else:
            print("I'm sorry, I didn't understand that input. Please enter only [Y/N]")
            continue


def amount_selection():
    """Returns the amount owed for months rent"""
    while True:
        amount_owed = float(input("Please enter the amount of money owed: "))
        confirm = input(f"Is this correct? ${amount_owed} Please enter [Y/N]: ")
        confirm = confirm.lower()
        if confirm == 'y' or confirm == 'yes':
            return amount_owed
        elif confirm == 'n' or confirm == 'no':
            continue
        else:
            print("I didn't understand your input")
            continue


def flatmate_name():
    """Checks if flatmate names exist and if not, returns name"""
    while True:
        name = str(input("Please enter the name of the flatmate you'd like to add to the bill: "))
        name = name.capitalize()
        if name.isalpha() is True:
            if name not in flatmate_objects:
                return name
            else:
                print("That flatmate already exists. Please enter a different name")
                continue
        else:
            print("Please only enter valid names")
            continue


def flatmate_days_in_home(date, name):
    """Checks how many days flatmates have been in the house"""

    # Convert str date to an int to check if days_in_home is not greater than the days in invoice month.
    date_month = int(date[:2])
    date_year = int(date[3:])
    days_in_home = 0

    while True:
        try:
            days_in_home = int(input(f"How many days has {name} been in the house? "))
        except ValueError:
            print("Please only enter integer values")
            continue
        # Days in home can't be less than 1 and more than days in invoice month.
        if days_in_home < 1:
            print("flatmate can't be on the invoice if less than 1 day in home.")
            continue
        elif days_in_home > calendar.monthrange(date_year, date_month)[1]:
            print(f"Selection can't be greater than days in the month.")
            continue
        else:
            days_in_home = days_in_home
            break
    return days_in_home


if __name__ == '__main__':
    """Main Script for Program"""
    flatmate_objects = {}

    # The welcome note
    print("Welcome to the Flatmates Billing App!")
    # Check if user would like to start a new bill
    while True:
        choice = str(input("Would you like to create an invoice? [Yes/No]: "))
        choice = choice.lower()

        if choice == 'yes' or choice == 'y':
            # Inputs for Bill object creation
            selected_date = date_selection()
            selected_amount = amount_selection()

            # Creates bill object
            our_bill = CreateBill(selected_amount, selected_date)
            print(f'Your bill for {selected_date} of amount {selected_date} has been created')

            while True:
                add_flatmates = str(input("Would you like to add flatmates to this bill? [Y/N]: "))
                add_flatmates = add_flatmates.lower()
                if add_flatmates == 'y' or add_flatmates == 'yes':
                    name = flatmate_name()
                    days_spent_in_house = flatmate_days_in_home(selected_date, name)
                    confirm = input(f"Are you sure you want to add {name} to the bill?: ")
                    confirm = confirm.lower()
                    if confirm == 'y' or confirm == 'yes':
                        name = Flatmate(name, days_spent_in_house)
                        # Logs bill
                        our_bill.log_bill(name)
                        flatmate_objects[name.get_name()] = name.get_days_in_house()
                        print(f'Ok, {name.get_name()} has been added to the bill ')
                        continue
                    else:
                        print(f"Ok, not adding {name} to bill.")
                        continue

                elif add_flatmates == 'n' or add_flatmates == 'no':
                    print(f'Ok, here are you current flatmates {flatmate_objects}')
                    break

                else:
                    print("I didn't recognize that input. Please enter only 'Y' or 'N'")
                    continue

        elif choice == 'no' or 'n':
            print("Ok, thanks.")
            break

        else:
            print("I didn't recognize that input. Please enter 'Yes' or 'No'.")
            continue

        # Breakdown of what people owe
        print("Here is what people owe for this billing period:")
        our_bill.bill_pay()
        print('*' * 40)
        pdf = PdfReport()
        print("Created PDF Invoice")
        pdf.generate(our_bill)










