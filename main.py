import os
from typing import Any, Dict, Optional

import streamlit as st
import pandas as pd
import requests

st.title('Gather Go')
st.caption("Don't forget to add yourself!")

if "contacts" not in st.session_state:
    st.session_state.contacts = []

relationship_options = [
    "Select relationship",
    "Yourself",
    "Immediate family",
    "Extended family",
    "Close friends",
    "Casual friends",
    "Acquaintance",
    "Online/distant connection",
    "In a relationship with",
    "Spouse",
]

frequency_options = [
    "Select frequency",
    "Very frequently - usually daily",
    "Not every day but weekly",
    "Once or twice a month",
    "Once or twice a year",
    "Every few years",
]

duration_options = [
    "Select duration",
    "Since birth/childhood",
    "1-5 years",
    "5-15 years",
    "15+years",
]

life_stage_options = [
    "Select life stage",
    "Very similar to mine",
    "Similar to mine in some respects",
    "Quite different from mine",
]

relative_age_options = [
    "Select relative age",
    "Younger than me by 6+years",
    "My age +/- 5 years",
    "Older than me by 6+years",
    "I don't know",
]

trigger_rerun = getattr(st, "rerun", None) or getattr(st, "experimental_rerun", None)

if "show_form" not in st.session_state:
    st.session_state.show_form = False


def _append_contact(entry: Dict[str, str]) -> None:
    st.session_state.contacts.append(entry)


@st.dialog("Add Person")
def person_form_dialog() -> None:
    with st.form("relationship_form", clear_on_submit=True):
        person_name = st.text_input("What is the person's name?")

        relationship = st.selectbox(
            "What is your relationship with them?",
            options=relationship_options,
        )

        interests = st.text_input("What are their interests?")

        contact_frequency = st.selectbox(
            "How often do you speak with them?",
            options=frequency_options,
        )

        known_duration = st.selectbox(
            "How long have you known them?",
            options=duration_options,
        )

        life_stage = st.selectbox(
            "Their life stage is?",
            options=life_stage_options,
        )

        location = st.text_input("Where do they live (city, state, and country)?")

        relative_age = st.selectbox(
            "Their are?",
            options=relative_age_options,
        )

        save = st.form_submit_button("Save person")
        cancel = st.form_submit_button("Cancel", type="secondary")

    if save:
        entry = {
            "person_name": person_name,
            "relationship_type": "" if relationship == relationship_options[0] else relationship,
            "interests": interests,
            "communication_frequency": "" if contact_frequency == frequency_options[0] else contact_frequency,
            "relationship_duration": "" if known_duration == duration_options[0] else known_duration,
            "life_stage_similarity": "" if life_stage == life_stage_options[0] else life_stage,
            "location": location,
            "age_relative": "" if relative_age == relative_age_options[0] else relative_age,
        }

        _append_contact(entry)
        st.session_state.show_form = False

        if trigger_rerun is not None:
            trigger_rerun()

    if cancel:
        st.session_state.show_form = False
        if trigger_rerun is not None:
            trigger_rerun()


if st.button("Add person"):
    st.session_state.show_form = True

if st.session_state.show_form:
    person_form_dialog()

if st.session_state.contacts:
    contacts_df = pd.DataFrame(st.session_state.contacts)
    st.dataframe(contacts_df)
else:
    st.info("Add someone to start building your list.")

st.write("---")

if "gemini_response" not in st.session_state:
    st.session_state.gemini_response = None


def call_gemini(contacts: pd.DataFrame) -> Optional[Dict[str, Any]]:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not set in environment.")
        return None

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": api_key,
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Please find ways that I can build stronger connections with the people in my contacts. I am 'Yourself' in this data: " + contacts.to_json(orient="records") if not contacts.empty else "[]",
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        st.error(f"Gemini API request failed: {exc}")
    except ValueError:
        st.error("Gemini API returned non-JSON response.")

    return None


col_actions = st.columns(2)

with col_actions[0]:
    st.button("Visualize connections")

with col_actions[1]:
    if st.button("Suggest plans"):
        if not st.session_state.contacts:
            st.warning("Add at least one person before requesting plan suggestions.")
        else:
            result = call_gemini(pd.DataFrame(st.session_state.contacts))
            if result is not None:
                st.session_state.gemini_response = result

if st.session_state.gemini_response:
    st.subheader("Gemini response")
    st.json(st.session_state.gemini_response)
