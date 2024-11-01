import streamlit as st
import txtai
import time
import pandas as pd
import json
import ast

# Function to get a key based on index
def get_key_by_index(original_dict, index):
    keys = list(original_dict.keys())
    if index < 0 or index >= len(keys):
        raise IndexError("Index out of range")
    return keys[index]

# Example condition
condition_met = False

# Function to simulate condition being met after some time
def check_condition():
    global condition_met
    time.sleep(1)  # Simulate waiting for 5 seconds
    condition_met = True
    
if 'submit_button' not in st.session_state:
    st.session_state.submit_button = False
    
def click_submit():
    st.session_state.submit_button = True

st.title("Welcome! AI Neighborhood Assistant is here to help you 🤖🏠")

## read the suburbs listings json file
with open('neighborhood_profiles.json', 'r') as file:
     neighborhood_profiles_json = json.load(file)

with open('suburb_listings.json', 'r') as file:
     suburb_listings_json =  json.load(file)
     
with st.chat_message("user"):
    st.write("Hello 👋 I am here to help you find the perfect location. Do you prefer to fill the questionnaire or to tell me your preferences?")
    
# Add a radio button for the selection
selection = st.radio(
    "Choose your preference:",
    ('Fill the questionnaire', 'Tell me your preferences')
)

# Display the selected option
if selection == 'Fill the questionnaire':
    st.write("You chose to fill the questionnaire.")
    
    # Create a form for the questionnaire
    with st.form(key='questionnaire_form'):
        # Sample questions
        q1 = 'Which city do you want  to move to?'
        a1 = st.text_input(q1)
        
        q2 = 'How big is your household?'
        a2 = st.slider(q2, 1, 20, step=1)
        
        q3 = 'Do you have or want to have pets?'
        a3 = st.selectbox(q3, ['yes', 'no'])
        
         # Question allowing custom input or selection
        q4 = 'What is your working arrangement? WFH, onsite or Hybrid?'
        work_arrangement = ['wfh', 'onsite', 'hybrid']
        a4 = st.selectbox(q4, work_arrangement)
        
        q5 = 'Tell us more about your preferred distance to the city'
        a5 = st.text_input(q5)

        q6 = 'How many bedrooms do you need?'
        a6 = st.slider(q6, 1, 10, step=1)

        q7 = 'City, Nature or Both? Tell us about your lifestyle'
        a7 = st.text_input(q7)

        q8 = 'House or flat? Tell us about your ideal place?'
        a8 = st.text_input(q8)

        q9 = 'How do you spend your free time?'
        a9 = st.text_input(q9)

        q10 = 'If you have or planning to have kids, what will be your schooling preference?'
        a10 = st.text_input(q10)
        
        # Submit button
        submit_button = st.form_submit_button(label='Submit', on_click=click_submit, icon="✅")
    
    # Handle form submission
    if st.session_state.submit_button:
        st.write("Thank you for filling the questionnaire ☺️")
        
elif selection == 'Tell me your preferences':
    st.write("You chose to tell me your preferences.")
    # Add your speech-to-text code or form for preferences here
    preferences = st.text_area("Please describe your preferences:")
    submit_button = st.button(label='Submit', on_click=click_submit, icon="✅")
    if st.session_state.submit_button:
        st.write("Thank you for providing your preferences.")
        st.write(f"Preferences: {preferences}")
        
        
# llm = LLM("meta-llama/Meta-Llama-3.1-8B-Instruct"))
questions = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
answers = [a1, a2, a3, a4, a5, a6, a7, a8, a9, a10]

persona_input = "\n".join([f"{q}: {a}" for q, a in zip(questions, answers)])

    # Convert the strings to valid JSON format and then to dictionaries
def convert_to_dict(json_str):
    try:
        # Replace single quotes with double quotes and handle escaped characters
        json_str = json_str.replace("'", "\"")
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

# Button to start the process
if st.session_state.submit_button:
    # Start checking the condition
    check_condition()
    
    # Wait until the condition is met
    while not condition_met:
        time.sleep(1)  # Check every second
    
    # Once the condition is met, proceed with the chat message
    st.chat_message("AI")
    st.write("I have created a persona based on your preferences. Let me find the perfect neighborhood for you. 👀")
    neighborhoods_embeddings = txtai.Embeddings(path="sentence-transformers/all-MiniLM-L6-v2")
    neighborhood_profiles  = list(neighborhood_profiles_json.values())
    neighborhoods_embeddings.index(neighborhood_profiles)
    recommended_neighborhood_index = neighborhoods_embeddings.search(persona_input, 1)[0][0]

    recommended_neighborhood_description = neighborhood_profiles[recommended_neighborhood_index]
    neighborhoood_name = get_key_by_index(neighborhood_profiles_json, recommended_neighborhood_index)
    print(recommended_neighborhood_index)
    st.header(f"Based on your preferences, we recommend the following neighborhood for you: {neighborhoood_name} 🪴")
    st.write("Here is a brief description of the neighborhood:")
    st.write(recommended_neighborhood_description)
    
    accept_recommendation = st.button(label='Accept recommendation', icon="✅")
    print(accept_recommendation)

    if accept_recommendation:
        st.write("Great! I'm glad you liked the recommendation. Let's find the perfect home for you.")
        listings_embeddings = txtai.Embeddings(path="sentence-transformers/all-MiniLM-L6-v2")
        listings_from_neighborhood = suburb_listings_json[neighborhoood_name]
        listings_embeddings.index(listings_from_neighborhood)
        recommendations = listings_embeddings.search(str({"user_profile": persona_input}), 3)
        list_of_ids_profile_recs = [item[0] for item in recommendations]

        recommended_listings = [listings_from_neighborhood[i] for i in list_of_ids_profile_recs]
       
        st.subheader("Here are some listings that match your preferences:")
        for recs in recommended_listings:
            data = ast.literal_eval(recs)
            st.write(data["listing_description"].replace('<br/>', ""))
            listing_id = data['listing_id']
            link = f"https://www.realestate.com.au/property-apartment-vic-southbank-{listing_id}"
            st.link_button("Check out this property", link, icon="🏡")
            
            



        


        
        
        

        