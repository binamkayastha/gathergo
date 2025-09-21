import streamlit as st
import pandas as pd

st.title('Gather Go')


with st.form("relationship_form"):
    person_name = st.text_input("What is the person's name?")

    relationship_options = [
        "Select relationship",
        "Immediate family",
        "Extended family",
        "Close friends",
        "Casual friends",
        "Acquaintance",
        "Online/distant connection",
        "In a relationship with",
        "Spouse",
    ]
    relationship = st.selectbox(
        "What is your relationship with them?",
        options=relationship_options,
    )

    frequency_options = [
        "Select frequency",
        "Very frequently - usually daily",
        "Not every day but weekly",
        "Once or twice a month",
        "Once or twice a year",
        "Every few years",
    ]
    contact_frequency = st.selectbox(
        "How often do you speak with them?",
        options=frequency_options,
    )

    duration_options = [
        "Select duration",
        "Since birth/childhood",
        "1-5 years",
        "5-15 years",
        "15+years",
    ]
    known_duration = st.selectbox(
        "How long have you known them?",
        options=duration_options,
    )

    life_stage_options = [
        "Select life stage",
        "Very similar to mine",
        "Similar to mine in some respects",
        "Quite different from mine",
    ]
    life_stage = st.selectbox(
        "Their life stage is?",
        options=life_stage_options,
    )

    location = st.text_input("Where do they live (city, state, and country)?")

    relative_age_options = [
        "Select relative age",
        "Younger than me by 6+years",
        "My age +/- 5 years",
        "Older than me by 6+years",
        "I don't know",
    ]
    relative_age = st.selectbox(
        "Their are?",
        options=relative_age_options,
    )

    submitted = st.form_submit_button("Submit")

if submitted:
    data = {
        "person_name": person_name,
        "relationship_type": "" if relationship == relationship_options[0] else relationship,
        "communication_frequency": "" if contact_frequency == frequency_options[0] else contact_frequency,
        "relationship_duration": "" if known_duration == duration_options[0] else known_duration,
        "life_stage_similarity": "" if life_stage == life_stage_options[0] else life_stage,
        "location": location,
        "age_relative": "" if relative_age == relative_age_options[0] else relative_age,
    }

    st.dataframe(pd.DataFrame([data]))
