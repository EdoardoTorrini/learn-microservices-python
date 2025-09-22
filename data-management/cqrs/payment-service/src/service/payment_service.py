from events.sender import EventSender
from service.card_validator_service import CardValidatorService
from events.receive import EventReceiver

def run_payment_service():
    validator = CardValidatorService()
    sender = EventSender()
    receiver = EventReceiver(card_validator_service=validator, event_sender=sender)
    receiver.start() 
