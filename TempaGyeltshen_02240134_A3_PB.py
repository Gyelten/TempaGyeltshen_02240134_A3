"""
Unit Test Suite for Simple Banking Application

This module uses Python's unittest framework to validate core banking features.
It covers tests for user inputs, error handling, and functionality for deposits,
withdrawals, transfers, recharge, and authentication.
"""

import unittest
from TempaGyeltshen_02240134_A3_PA import (
    Personal, Business, BankCore, InputError, FundTransferError
)

class SimpleBankTest(unittest.TestCase):
    """
    Test class to evaluate individual banking features and edge cases.
    Includes tests for valid and invalid scenarios across core functionalities.
    """

    def setUp(self):                         #Initializes test accounts before each test.
        self.bank = BankCore()
        self.acc1 = Personal("11111", "1111", 1000)  # Account with initial Nu. 1000
        self.acc2 = Business("22222", "2222", 500)   # Account with initial Nu. 500
        self.bank.users["11111"] = self.acc1
        self.bank.users["22222"] = self.acc2

    # --- Unusual Inputs ---

    def test_negative_deposit(self):             #Check deposit with negative amount raises InputError.
        with self.assertRaises(InputError):
            self.acc1.deposit(-100)  # Invalid: can't deposit negative value

    def test_invalid_recharge_number(self):                   #Ensure recharge with letters in phone number is rejected.
        with self.assertRaises(InputError):
            self.acc1.recharge("abc123", 50)

    def test_short_number(self):                              #Ensure too-short phone number is rejected.
        with self.assertRaises(InputError):
            self.acc1.recharge("123", 50)

    # --- Invalid Usage Cases ---

    def test_withdraw_too_much(self):                            #Withdraw more than balance should raise InputError.
        with self.assertRaises(InputError):
            self.acc2.withdraw(10000)

    def test_transfer_too_much(self):                          #Attempting to transfer more than available balance should raise error.
        with self.assertRaises(FundTransferError):
            self.acc1.transfer(2000, self.acc2)

    def test_recharge_over_balance(self):                        #Mobile recharge amount exceeding balance should fail.
        with self.assertRaises(InputError):
            self.acc2.recharge("1234567890", 10000)

    # --- Valid Operations ---

    def test_deposit(self):                                #Successful deposit should increase balance.
        self.acc1.deposit(500)
        self.assertEqual(self.acc1.balance, 1500)

    def test_withdraw(self):                               #Successful withdrawal should decrease balance.
        self.acc2.withdraw(300)
        self.assertEqual(self.acc2.balance, 200)

    def test_transfer(self):                               #Valid fund transfer should update both balances correctly."""
        self.acc1.transfer(200, self.acc2)
        self.assertEqual(self.acc1.balance, 800)
        self.assertEqual(self.acc2.balance, 700)

    def test_valid_recharge(self):                            #Valid mobile recharge should deduct amount from account."""
        self.acc1.recharge("1234567890", 100)
        self.assertEqual(self.acc1.balance, 900)

    def test_remove_account(self):                            #Account removal should delete user from records."""
        self.bank.remove_account("11111")
        self.assertNotIn("11111", self.bank.users)

    def test_login_success(self):                              #Successful login returns the correct account object."""
        user = self.bank.authenticate("22222", "2222")
        self.assertEqual(user, self.acc2)

    def test_login_fail(self):                                 #Login with wrong PIN should raise InputError."""
        with self.assertRaises(InputError):
            self.bank.authenticate("22222", "0000")

# --- Execute all test cases ---
if __name__ == '__main__':
    unittest.main()
