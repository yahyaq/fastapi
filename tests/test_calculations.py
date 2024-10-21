import pytest
from app.calculations import add, BankAccount, Insufficient_funds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(40)


@pytest.mark.parametrize("num1, num2, expected", [
    (4, 4, 8),
    (5, 2, 7),
    (4, 14, 18)
])
def test_add1(num1, num2, expected):
    assert add(num1, num2) == expected


@pytest.mark.parametrize("num1, num2, expected", [
    (5, 5, 4),
    (6, 2, 4),
    (10, 4, 15)
])
def test_add2(num1, num2, expected):
    assert add(num1, num2) != expected


def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 40


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_deposit(bank_account):
    bank_account.deposit(44)
    assert bank_account.balance == 84


def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 20


def test_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 44


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (20000, 16250, 3750),
    (4000, 2400, 1600),
    (6000, 2400, 3600)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(Insufficient_funds):
        bank_account.withdraw(50)
