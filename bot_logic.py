user_states = {}

def get_reply(phone, message):
    if phone not in user_states:
        user_states[phone] = {"step": "start", "data": {}}

    state = user_states[phone]

    if state["step"] == "start":
        state["step"] = "budget"
        return "Hi 👋 What type of property are you looking for? (1BHK / 2BHK / 3BHK)"

    elif state["step"] == "budget":
        state["data"]["type"] = message
        state["step"] = "location"
        return "Great 👍 What is your budget?"

    elif state["step"] == "location":
        state["data"]["budget"] = message
        state["step"] = "timeline"
        return "Which location are you interested in?"

    elif state["step"] == "timeline":
        state["data"]["location"] = message
        state["step"] = "name"
        return "When are you planning to buy?"

    elif state["step"] == "name":
        state["data"]["timeline"] = message
        state["step"] = "done"
        return "Can you share your name?"

    elif state["step"] == "done":
        state["data"]["name"] = message

        summary = f"""
Thanks {state['data']['name']}!

Here’s what I understood:
- Type: {state['data']['type']}
- Budget: {state['data']['budget']}
- Location: {state['data']['location']}
- Timeline: {state['data']['timeline']}

We’ll contact you soon 😊
"""
        user_states.pop(phone)
        return summary

    return "Sorry, something went wrong."