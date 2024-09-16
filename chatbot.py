import re
from tkinter import scrolledtext
import tkinter as tk

# Define regex patterns and responses for a more extensive knowledge base
patterns = {
    r'\b(hi|hello|hey)\b': "Hello! Welcome to our hospital. How can I assist you today?",
    r'\bhow\s*are\s*you\b': "I'm just a bot, but I'm here to help you book an appointment!",
    r'\b(doctor|appointment|book|schedule)\b': "I can help you with that. Can you tell me what symptoms you're experiencing or what kind of specialist you need?",

    # Cardiologist
    r'\b(chest pain|heart attack|shortness of breath|palpitations|high blood pressure|hypertension|arrhythmia|heart disease)\b':
        "You may need to see a cardiologist. They specialize in heart-related issues. Would you like to book an appointment with our heart specialist?",

    # Dermatologist
    r'\b(skin rash|acne|eczema|psoriasis|itching|dermatitis|moles|skin cancer|hair loss|nail issues)\b':
        "A dermatologist could help with your skin condition. Would you like to book an appointment with our skin specialist?",

    # General Physician
    r'\b(fever|cough|cold|flu|sore throat|headache|fatigue|general check-up|wellness exam)\b':
        "These symptoms can be treated by a general physician. Would you like to book an appointment with a general physician?",

    # Gastroenterologist
    r'\b(stomach ache|abdominal pain|indigestion|nausea|vomiting|diarrhea|constipation|IBS|acid reflux|liver disease|ulcers)\b':
        "A gastroenterologist can help with digestive issues. Would you like to book an appointment with a digestive health specialist?",

    # Pediatrician
    r'\b(child|children|kid|baby|infant|toddler|pediatric care|childhood illness)\b':
        "We have pediatricians who specialize in children's health. Would you like to book an appointment for your child?",

    # Orthopedic Specialist
    r'\b(bone pain|joint pain|arthritis|back pain|fracture|sprain|dislocation|osteoporosis|scoliosis)\b':
        "An orthopedic specialist can help with bone and joint issues. Would you like to book an appointment with an orthopedic doctor?",

    # Dentist
    r'\b(teeth pain|toothache|cavities|gum issues|dental cleaning|root canal|braces|orthodontics)\b':
        "A dentist can help with dental issues. Would you like to book an appointment with a dentist?",

    # Gynecologist
    r'\b(women\'s health|pregnancy|gynecology|menstrual issues|contraception|fertility|pap smear|breast exam)\b':
        "We have gynecologists who specialize in women's health. Would you like to book an appointment with a gynecologist?",

    # Psychologist
    r'\b(mental health|anxiety|depression|stress|therapy|counseling|psychotherapy|PTSD|trauma)\b':
        "A psychologist can assist with mental health issues. Would you like to book an appointment with a psychologist?",

    # Neurologist
    r'\b(seizures|epilepsy|migraine|stroke|neuropathy|multiple sclerosis|parkinson\'s|dementia|neurological disorder)\b':
        "A neurologist specializes in the nervous system. Would you like to book an appointment with a neurologist?",

    # Endocrinologist
    r'\b(diabetes|thyroid|hormonal issues|endocrine disorders|metabolism|adrenal gland|pituitary gland)\b':
        "An endocrinologist specializes in hormonal and metabolic issues. Would you like to book an appointment with an endocrinologist?",

    # Urologist
    r'\b(urinary tract|UTI|kidney stones|prostate|bladder issues|erectile dysfunction|incontinence)\b':
        "A urologist can help with urinary tract issues. Would you like to book an appointment with a urologist?",

    # Oncologist
    r'\b(cancer|tumor|chemotherapy|radiation therapy|oncology|cancer screening)\b':
        "An oncologist specializes in cancer treatment. Would you like to book an appointment with an oncologist?",

    # Rheumatologist
    r'\b(rheumatoid arthritis|lupus|autoimmune disease|rheumatology|inflammation)\b':
        "A rheumatologist can help with autoimmune and inflammatory conditions. Would you like to book an appointment with a rheumatologist?",

    # Pulmonologist
    r'\b(asthma|COPD|lung disease|respiratory issues|bronchitis|pneumonia|sleep apnea)\b':
        "A pulmonologist specializes in lung and respiratory issues. Would you like to book an appointment with a pulmonologist?",

    # Ophthalmologist
    r'\b(vision issues|eye pain|blurry vision|cataracts|glaucoma|eye infection|ophthalmology)\b':
        "An ophthalmologist can help with eye-related issues. Would you like to book an appointment with an eye specialist?",

    # Booking time and day
    r'\b(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b':
        "Which time would you prefer for your appointment on {}?".format,

    r'\b(\d{1,2}:\d{2}(?:am|pm)?)\b':
        "Thank you! Your appointment is tentatively scheduled for {}. A representative will contact you to confirm.".format,

    # Gratitude and closing
    r'\bthank you|thanks\b': "You're welcome! If you have any more questions or need further assistance, feel free to ask.",
    r'\bbye\b': "Goodbye! If you need further assistance, don't hesitate to contact us."
}

# Define available doctors and their schedules
doctors = {
    "Cardiologist": {
        "name": "Dr. Smith",
        "availability": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    },
    "Dermatologist": {
        "name": "Dr. Johnson",
        "availability": ["Monday", "Tuesday", "Wednesday", "Thursday"]
    },
    "General Physician": {
        "name": "Dr. Miller",
        "availability": ["Monday", "Wednesday", "Friday"]
    },
    "Gastroenterologist": {
        "name": "Dr. Wilson",
        "availability": ["Tuesday", "Thursday", "Saturday"]
    },
    "Pediatrician": {
        "name": "Dr. Adams",
        "availability": ["Tuesday", "Thursday", "Saturday"]
    },
    "Orthopedic Specialist": {
        "name": "Dr. Brown",
        "availability": ["Wednesday", "Friday"]
    },
    "Dentist": {
        "name": "Dr. Clark",
        "availability": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    },
    "Gynecologist": {
        "name": "Dr. Davis",
        "availability": ["Monday", "Wednesday", "Friday"]
    },
    "Psychologist": {
        "name": "Dr. Evans",
        "availability": ["Tuesday", "Thursday"]
    },
    "Neurologist": {
        "name": "Dr. Patel",
        "availability": ["Monday", "Thursday", "Saturday"]
    },
    "Endocrinologist": {
        "name": "Dr. Green",
        "availability": ["Monday", "Wednesday", "Friday"]
    },
    "Urologist": {
        "name": "Dr. White",
        "availability": ["Tuesday", "Friday"]
    },
    "Oncologist": {
        "name": "Dr. Lee",
        "availability": ["Monday", "Wednesday", "Friday"]
    },
    "Rheumatologist": {
        "name": "Dr. King",
        "availability": ["Tuesday", "Thursday"]
    },
    "Pulmonologist": {
        "name": "Dr. Moore",
        "availability": ["Monday", "Thursday", "Saturday"]
    },
    "Ophthalmologist": {
        "name": "Dr. Taylor",
        "availability": ["Wednesday", "Friday", "Saturday"]
    }
}

def check_doctor_availability(doctor_type, day):
    """
    Check if the specified doctor type is available on the given day.
    """
    doctor = doctors.get(doctor_type)
    if doctor and day.capitalize() in doctor["availability"]:
        return f"{doctor['name']} ({doctor_type}) is available on {day}. Please provide a specific time for your appointment."
    else:
        available_days = ', '.join(doctor["availability"]) if doctor else "N/A"
        return f"Sorry, {doctor['name']} ({doctor_type}) is not available on {day}. They are available on {available_days}."

def get_response(user_input):
    """
    Match the user input to predefined patterns and return the appropriate response.
    """
    # Check for specific symptoms or specialist booking
    for doctor_type in doctors.keys():
        if re.search(rf'\b({doctor_type.lower()})\b', user_input, re.IGNORECASE):
            for day in doctors[doctor_type]["availability"]:
                if re.search(rf'\b{day.lower()}\b', user_input, re.IGNORECASE):
                    return check_doctor_availability(doctor_type, day)

    # Match general patterns
    for pattern, response in patterns.items():
        match = re.search(pattern, user_input, re.IGNORECASE)
        if match:
            # Handle specific time scheduling
            if callable(response):
                return response(*match.groups())
            return response

    return "Sorry, I couldn't understand you. Could you describe your symptoms or what kind of help you're looking for?"

# Example usage (this will be part of the integration with the frontend)
if __name__ == "__main__":
    print("Chatbot: Hello! How can I assist you today? (type 'exit' to end the chat)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Chatbot: Goodbye! Take care.")
            break
        response = get_response(user_input)
        print("Chatbot:", response)
