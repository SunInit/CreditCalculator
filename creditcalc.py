# credit calculator by @sonja
from math import log, ceil, pow
import argparse


class CreditCalculator:
    text_out = ['You need {} {} and {} {} to repay this credit!',           # [0]
                'You need {} {} to repay this credit!',                     # [1]
                'Your annuity payment = {}!',                               # [2]
                "Overpayment = {}",                                         # [3]
                'Your credit principal = {}!',                              # [4]
                'Month {}: paid out {}',                                    # [5]
                'Incorrect parameters']                                     # [6]
    state = "start"

    def __init__(self, credit_principal=0, monthly=0, months=0, interest=0):
        self.credit_principal = credit_principal
        self.months = months
        self.monthly = monthly
        self.interest = interest / 1200
        self.over = 0
        self.payments = []

    def console(self, mode):
        if mode == "month":
            if 1 < self.months < 12:
                print(self.text_out[1].format(int(self.months), "months"))
            elif self.months == 1:
                print(self.text_out[1].format(1, "month"))
            elif self.months == 12:
                print(self.text_out[1].format(1, "year"))
            elif self.months > 12 and self.months % 12 == 0:
                print(self.text_out[1].format(int(self.months/12), "years"))
            else:
                print(self.text_out[0].format(int(self.months // 12), "years", int(self.months % 12), "months"))
            if self.over > 0:
                print(self.text_out[3].format(int(self.over)))
        elif mode == "monthly":
            print(self.text_out[2].format(int(self.monthly)))
            if self.over > 0:
                print(self.text_out[3].format(int(self.over)))
        elif mode == "princ":
            print(self.text_out[4].format(int(self.credit_principal)))
            if self.over > 0:
                print(self.text_out[3].format(int(self.over)))
        elif mode == "diffmonthly":
            now = 1
            for pay in self.payments:
                print(self.text_out[5].format(now, int(pay)))
                now += 1
            if self.over > 0:
                print(self.text_out[3].format(int(self.over)))
        elif mode == "error":
            print(self.text_out[6])

    def cal_months(self):
        self.months = ceil(log(self.monthly/(self.monthly-self.interest*self.credit_principal), 1+self.interest))
        self.over = self.months * self.monthly - self.credit_principal

    def cal_monthly(self):
        term = pow(1 + self.interest, self.months)
        self.monthly = ceil(self.credit_principal * ((self.interest * term) / (term - 1)))
        self.over = self.months * self.monthly - self.credit_principal

    def cal_princ(self):
        term = pow(1 + self.interest, self.months)
        self.credit_principal = self.monthly / ((self.interest * term) / (term - 1))
        self.over = self.monthly * self.months - self.credit_principal

    def cal_diffmonth(self):
        now = 1
        _sum = 0
        while now <= self.months:
            term = self.credit_principal - ((self.credit_principal * (now - 1))/self.months)
            diffmonth = ceil((self.credit_principal / self.months) + self.interest * term)
            _sum += diffmonth
            now += 1
            self.payments.append(diffmonth)
        self.over = _sum - self.credit_principal


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help="mode of calculation, diff of annuity only")
    parser.add_argument("-cp", "--principal", help="Give the total amount of credit principal", type=float, default=0)
    parser.add_argument("-p", "--periods", help="Give the total of month", type=float, default=0)
    parser.add_argument("-i", "--interest", help="Give the interest rate in %", type=float, default=0)
    parser.add_argument("-pay", "--payment", help="Give the monthly payment in annuity payment", type=float, default=0)
    args = parser.parse_args()

    new_credit = CreditCalculator(credit_principal=args.principal, monthly=args.payment,
                                  months=args.periods, interest=args.interest)
    if args.type == "diff":
        if args.principal > 0 and args.periods > 0 and args.interest > 0:
            new_credit.state = "diffmonthly"
            new_credit.cal_diffmonth()
        else:
            new_credit.state = "error"
    elif args.type == "annuity":
        if args.payment > 0 and args.principal > 0 and args.interest > 0:
            new_credit.state = "month"
            new_credit.cal_months()
        elif args.payment > 0 and args.periods > 0 and args.interest > 0:
            new_credit.state = "princ"
            new_credit.cal_princ()
        elif args.principal > 0 and args.periods > 0 and args.interest > 0:
            new_credit.state = "monthly"
            new_credit.cal_monthly()
        else:
            new_credit.state = "error"
    else:
        new_credit.state = "error"
    new_credit.console(new_credit.state)
