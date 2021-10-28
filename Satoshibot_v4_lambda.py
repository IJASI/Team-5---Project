import json
import requests

   ### Required Libraries ###
from datetime import datetime
from dateutil.relativedelta import relativedelta


### Functionality Helper Functions ###
def parse_int(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return int(n)
    except ValueError:
        return float("nan")
        
def parse_float(n):
    """
    Securely converts a non-integer value to integer.
    """
    try:
        return float(n)
    except ValueError:
        return float("nan")  


def get_btcprice():
    """
    Retrieves the current price of bitcoin in US or CA dollars from the alternative.me Crypto API.
    """
    bitcoin_api_url = "https://api.alternative.me/v2/ticker/bitcoin/?convert=USD"
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    price_dollars = parse_float(response_json["data"]["1"]["quotes"]["USD"]["price"])
    return price_dollars



def build_validation_result(is_valid, violated_slot, message_content):
    """
    Define a result message structured as Lex response.
    """
    if message_content is None:
        return {"isValid": is_valid, "violatedSlot": violated_slot}

    return {
        "isValid": is_valid,
        "violatedSlot": violated_slot,
        "message": {"contentType": "PlainText", "content": message_content},
    }


### Dialog Actions Helper Functions ###
def get_slots(intent_request):
    """
    Fetch all the slots and their values from the current intent.
    """
    return intent_request["currentIntent"]["slots"]


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    """
    Defines an elicit slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "ElicitSlot",
            "intentName": intent_name,
            "slots": slots,
            "slotToElicit": slot_to_elicit,
            "message": message,
        },
    }


def delegate(session_attributes, slots):
    """
    Defines a delegate slot type response.
    """

    return {
        "sessionAttributes": session_attributes,
        "dialogAction": {"type": "Delegate", "slots": slots},
    }


def close(session_attributes, fulfillment_state, message):
    """
    Defines a close slot type response.
    """

    response = {
        "sessionAttributes": session_attributes,
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": fulfillment_state,
            "message": message,
        },
    }

    return response

### Intents Handlers ###
def convert_dollars(intent_request):
    """
    Performs dialog management and fulfillment for recommending a portfolio.
    """

    first_name = get_slots(intent_request)["firstName"]
    age = get_slots(intent_request)["age"]
    investment_amount = get_slots(intent_request)["investmentAmount"]
    #risk_level = get_slots(intent_request)["riskLevel"]
    source = intent_request["invocationSource"]

 
    if source == "DialogCodeHook":
        # Perform basic validation on the supplied input slots.
        # Use the elicitSlot dialog action to re-prompt
        # for the first violation detected.
        slots = get_slots(intent_request)
        validation_result = validate_data(age, investment_amount)
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot
            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )
        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]
        return delegate(output_session_attributes, get_slots(intent_request))
    # Get the initial investment recommendation
    initial_recommendation = convert_dollars(dollars)
    # Return a message with the initial recommendation based on the risk level.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """{} thank you for your information;
            based on the risk level you defined, my recommendation is to choose an investment portfolio with {}
            """.format(
                first_name, initial_recommendation
            ),
        },
    )
            
def validate_data (age, investment_amount):
    
    # confirm retirement age of 65 years
    if age is not None:
        age = parse_int(
            age)
        if age < 18:
            return build_validation_result(
                False,
                "age",
                "Please re-enter your age."
                "You must be at least 18 years of age or older to use this service.",
            )
        #if age >= 65:
         #   return build_validation_result(
          #      False,
          #      "age",
           #     "You are past the age of 64, "
            #     "Please take into consideration your retirement strategy as cryptocurrency is a volatile asset.",
            #)
        
        # Confirm the investment amount is greater than 50
    if investment_amount is not None:
        investment_amount = parse_int(investment_amount)
        if investment_amount < 50:
            return build_validation_result(
                False,
                "investmentAmount",
                "The minimum investment amount is $50 (No dustrading is allowed on the exchange), "
                "could you please provide a greater amount?",
            )
            
    return build_validation_result(True, None, None)     


### Intents Handlers ###
def convert_dollars(intent_request):
    """
    Performs dialog management and fulfillment for converting from dollars to bitcoin.
    """

    # Gets slots' values
    age = get_slots(intent_request)["age"]
    investmentAmount = get_slots(intent_request)["investmentAmount"]
    # currency = get_slots(intent_request)["currency"]

    # Explicitly parse currency as string and make it uppercase
   # currency = str(currency).upper()

    # Gets the invocation source, for Lex dialogs "DialogCodeHook" is expected.
    source = intent_request["invocationSource"]

    if source == "DialogCodeHook":
        # This code performs basic validation on the supplied input slots.

        # Gets all the slots
        slots = get_slots(intent_request)

        # Validates user's input using the validate_data function
        validation_result = validate_data(age, investmentAmount,)

        # If the data provided by the user is not valid,
        # the elicitSlot dialog action is used to re-prompt for the first violation detected.
        if not validation_result["isValid"]:
            slots[validation_result["violatedSlot"]] = None  # Cleans invalid slot

            # Returns an elicitSlot dialog to request new data for the invalid slot
            return elicit_slot(
                intent_request["sessionAttributes"],
                intent_request["currentIntent"]["name"],
                slots,
                validation_result["violatedSlot"],
                validation_result["message"],
            )

        # Fetch current session attributes
        output_session_attributes = intent_request["sessionAttributes"]

        # Once all slots are valid, a delegate dialog is returned to Lex to choose the next course of action.
        return delegate(output_session_attributes, get_slots(intent_request))

    # Get the current price of bitcoin in dolars and make the conversion from dollars to bitcoin.
    btc_value = parse_float(investmentAmount) / get_btcprice()
    btc_value = round(btc_value, 4)

    # Return a message with conversion's result.
    return close(
        intent_request["sessionAttributes"],
        "Fulfilled",
        {
            "contentType": "PlainText",
            "content": """Thank you for your information;
            you can get {} Bitcoins for your ${}.
            """.format(
                btc_value, investmentAmount,
            ),
        },
    )



### Intents Dispatcher ###

def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """

    intent_name = intent_request["currentIntent"]["name"]

    # Dispatch to bot's intent handlers
    if intent_name == "GetFGIndex":
        return convert_dollars(intent_request)

    raise Exception("Intent with name " + intent_name + " not supported")


### Main Handler ###
def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """

    return dispatch(event)