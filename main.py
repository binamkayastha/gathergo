import streamlit as st
import pandas as pd

st.title('Gather Go')
st.caption("Don't forget to add yourself!")

if "contacts" not in st.session_state:
    st.session_state.contacts = []

SELF_RELATIONSHIP = "Yourself"

relationship_options = [
    "Select relationship",
    SELF_RELATIONSHIP,
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


def _append_contact(entry: dict[str, str]) -> None:
    st.session_state.contacts.append(entry)



@st.dialog("Add Person")
def person_form_dialog() -> None:
    with st.form("relationship_form", clear_on_submit=True):
        person_name = st.text_input("What is the person's name?")

        relationship = st.selectbox(
            "What is your relationship with them?",
            options=relationship_options,
        )

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
    st.dataframe(pd.DataFrame(st.session_state.contacts))
else:
    st.info("Add someone to start building your list.")
