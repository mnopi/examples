from typing import Optional
from returns.maybe import Maybe, maybe


@maybe  # decorator to convert existing Optional[int] to Maybe[int]
def bad_function() -> Optional[int]:
    ...


maybe_number: Maybe[float] = bad_function().bind_optional(
    lambda number: number / 2,
)
# => Maybe will return Some[float] only if there's a non-None value
#    Otherwise, will return Nothing


# We can also bind a Optional-returning function over a container. To achieve this, we are going to use
# .bind_optional method.
class Balance:
    def __init__(self, balance=None):
        self.balance = balance

    def credit_amount(self):
        return self.balance


class User:
    def __init__(self, balance=None):
        self.balance = Balance(balance)

    def get_balance(self):
        return self.balance

    @staticmethod
    def choose_discount(n):
        return n * 0.1


user: Optional[User]

Maybe.from_optional(user).\
    bind_optional(lambda real_user: real_user.get_balance()).\
    bind_optional(lambda balance: balance.credit_amount(),).\
    bind_optional(lambda credit: User.choose_discount(credit) if credit > 0 else None)

# Type hint here is optional, it only helps the reader here:
discount_program: Maybe['DiscountProgram'] = Maybe.from_optional(
    user,
).bind_optional(  # This won't be called if `user is None`
    lambda real_user: real_user.get_balance(),
).bind_optional(  # This won't be called if `real_user.get_balance()` is None
    lambda balance: balance.credit_amount(),
).bind_optional(  # And so on!
    lambda credit: User.choose_discount(credit) if credit > 0 else None,
)
