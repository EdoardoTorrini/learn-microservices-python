class CardValidatorService:
    def payment_check(self, order) -> bool:
        return order.get("creditCardNumber", "").startswith("7777")