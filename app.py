
import warnings
warnings.filterwarnings('ignore')

import os
import streamlit as st
from crewai import Agent, Task, Crew
from utils import get_openai_api_key  # Importing the function to get OpenAI API key

# Load OpenAI API key from the .env file
openai_api_key = get_openai_api_key()
os.environ["OPENAI_API_KEY"] = openai_api_key  # Set it as an environment variable

# Optional: If you use the OpenAI API directly, you can also set the model
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'


# Define Agents
resident_doctor = Agent(
    role="Resident Doctor",
    goal="Collect initial statistics and patient information on {topic}",
    backstory="As a Resident Doctor, your role is to take initial medical statistics, "
              "patient history, and basic symptoms related to {topic}. "
              "You gather vital information that will help the Doctor in making a diagnosis. "
              "Your role is essential for creating a foundation for the Doctor's examination.",
    allow_delegation=False,
    verbose=True
)

doctor = Agent(
    role="Doctor",
    goal="Examine the patient and diagnose based on initial data collected on {topic}",
    backstory="As a Doctor, you analyze the information provided by the Resident Doctor. "
              "You conduct a thorough examination of the patient, listening to their symptoms, "
              "examining the collected data, and making a diagnosis. "
              "Your goal is to provide an accurate diagnosis and create a treatment plan.",
    allow_delegation=False,
    verbose=True
)

medical_report_writer = Agent(
    role="Medical Report Writer",
    goal="Write a comprehensive report on the Doctor's findings after patient consultation",
    backstory="As the Medical Report Writer, your task is to review the Doctor's findings from "
              "the patient examination and prepare a detailed report. "
              "This report includes diagnosis, treatment recommendations, and follow-up instructions based on the Doctor's input.",
    allow_delegation=False,
    verbose=True
)


# Define Tasks
initial_statistics = Task(
    description=(
        "1. Collect the patient's basic details, medical history, and symptoms related to {topic}.\n"
        "2. Measure vital signs such as blood pressure, temperature, and pulse.\n"
        "3. Organize all collected data in a structured format for the Doctor's examination."
    ),
    expected_output="A detailed patient information sheet, including vital signs and symptom history, "
                    "ready for the Doctor's review.",
    agent=resident_doctor,
)

patient_examination = Task(
    description=(
        "1. Analyze the patient's symptoms and medical history provided by the Resident Doctor.\n"
        "2. Perform a physical examination and conduct necessary tests.\n"
        "3. Formulate a diagnosis based on the collected information and examination."
    ),
    expected_output="A detailed diagnosis and treatment plan for the patient, including any tests or prescriptions needed.",
    agent=doctor,
)

report_writing = Task(
    description=(
        "Write a medical report based on the Doctor's examination and diagnosis. "
        "The report should include the diagnosis, treatment plan, and any follow-up recommendations."
    ),
    expected_output="A comprehensive medical report documenting the diagnosis, treatment, and follow-up plan.",
    agent=medical_report_writer
)

# Set up the Streamlit UI
st.title('Medical Diagnosis and Report System')

# User input for topic (patient condition)
topic = st.text_input('Enter the patient condition/topic (e.g., Diabetes Management):')

# Process when the button is pressed
if st.button('Start Diagnosis'):
    if topic:
        # Updated Crew and Execution
        crew = Crew(
            agents=[resident_doctor, doctor, medical_report_writer],
            tasks=[initial_statistics, patient_examination, report_writing],
            verbose=2
        )
        
        # Kick off the task
        result = crew.kickoff(inputs={"topic": topic})

        # Display results
        st.subheader('Diagnosis and Report:')
        st.markdown(result)
    else:
        st.error("Please enter a valid topic.")
