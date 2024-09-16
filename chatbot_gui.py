import customtkinter as ctk
import re
import random

patterns = {
    r'\b(hi|hello|hey)\b': "Hello! Welcome to our hospital chatbot. How can I assist you today? You can ask about doctor appointments, describe your symptoms, or inquire about hospital services.",
    r'\bhow\s*are\s*you\b': "I'm here to help you book an appointment or answer any questions you have. What can I assist you with?",
    r'\b(doctor|appointment|book|schedule)\b': "I can help you with that. Please tell me about your symptoms or what kind of specialist you need. For example, you can say 'I have a skin rash' or 'I need a cardiologist'.",
    r'\b(hospital|services|facilities|emergency)\b': "Our hospital offers a wide range of services including emergency care, surgery, and specialized treatments. Would you like to know more about a specific service?",
    r'\b(chest pain|heart attack|shortness of breath|palpitations|high blood pressure|hypertension|arrhythmia|heart disease)\b': "It sounds like you may need a cardiologist. They specialize in heart-related issues. Would you like to book an appointment with our heart specialist? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(skin rash|acne|eczema|psoriasis|itching|dermatitis|moles|skin cancer|hair loss|nail issues)\b': "You might need to see a dermatologist for your skin condition. Would you like to book an appointment with our skin specialist? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(fever|cough|cold|flu|sore throat|headache|fatigue|general check-up|wellness exam)\b': "A general physician can assist with these symptoms. Would you like to book an appointment with one? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(stomach ache|abdominal pain|indigestion|nausea|vomiting|diarrhea|constipation|IBS|acid reflux|liver disease|ulcers)\b': "For digestive issues, a gastroenterologist would be appropriate. Would you like to book an appointment with our specialist? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(child|children|kid|baby|infant|toddler|pediatric care|childhood illness)\b': "We have pediatricians who specialize in children's health. Would you like to book an appointment for your child? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(bone pain|joint pain|arthritis|back pain|fracture|sprain|dislocation|osteoporosis|scoliosis)\b': "An orthopedic specialist can help with bone and joint issues. Would you like to book an appointment with our orthopedic doctor? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(teeth pain|toothache|cavities|gum issues|dental cleaning|root canal|braces|orthodontics)\b': "A dentist can assist with dental issues. Would you like to book an appointment with our dentist? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(women\'s health|pregnancy|gynecology|menstrual issues|contraception|fertility|pap smear|breast exam)\b': "A gynecologist would be the right specialist for women's health issues. Would you like to book an appointment? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(mental health|anxiety|depression|stress|therapy|counseling|psychotherapy|PTSD|trauma)\b': "For mental health support, a psychologist can help. Would you like to book an appointment with our psychologist? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(seizures|epilepsy|migraine|stroke|neuropathy|multiple sclerosis|parkinson\'s|dementia|neurological disorder)\b': "A neurologist specializes in nervous system issues. Would you like to book an appointment with our neurologist? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(diabetes|thyroid|hormonal issues|endocrine disorders|metabolism|adrenal gland|pituitary gland)\b': "An endocrinologist can help with hormonal and metabolic issues. Would you like to book an appointment? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(urinary tract|UTI|kidney stones|prostate|bladder issues|erectile dysfunction|incontinence)\b': "A urologist can assist with urinary tract issues. Would you like to book an appointment with our urologist? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(cancer|tumor|chemotherapy|radiation therapy|oncology|cancer screening)\b': "An oncologist specializes in cancer treatment. Would you like to book an appointment? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(rheumatoid arthritis|lupus|autoimmune disease|rheumatology|inflammation)\b': "A rheumatologist can help with autoimmune and inflammatory conditions. Would you like to book an appointment? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(asthma|COPD|lung disease|respiratory issues|bronchitis|pneumonia|sleep apnea)\b': "A pulmonologist specializes in lung and respiratory issues. Would you like to book an appointment? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\b(vision issues|eye pain|blurry vision|cataracts|glaucoma|eye infection|ophthalmology)\b': "An ophthalmologist can assist with eye-related issues. Would you like to book an appointment? Please reply with 'yes' to proceed or 'no' to cancel.",
    r'\bthank you|thanks\b': "You're welcome! If you have any more questions or need further assistance, feel free to ask.",
    r'\bbye\b': "Goodbye! If you need further assistance, don't hesitate to contact us."
}

doctors = {
    "Cardiologist": {
        "name": "Dr. Smith",
        "availability": {
            "Monday": ["9:00am", "10:00am", "11:00am"],
            "Tuesday": ["9:00am", "10:00am", "11:00am"],
            "Wednesday": ["9:00am", "10:00am"],
            "Thursday": ["10:00am", "11:00am"],
            "Friday": ["9:00am", "11:00am"]
        }
    },
    "Dermatologist": {
        "name": "Dr. Johnson",
        "availability": {
            "Monday": ["1:00pm", "2:00pm"],
            "Tuesday": ["3:00pm", "4:00pm"],
            "Wednesday": ["2:00pm", "3:00pm"],
            "Thursday": ["1:00pm", "2:00pm"]
        }
    },
    "General Physician": {
        "name": "Dr. Miller",
        "availability": {
            "Monday": ["9:00am", "10:00am", "11:00am"],
            "Wednesday": ["9:00am", "11:00am"],
            "Friday": ["10:00am", "11:00am"]
        }
    },
    "Gastroenterologist": {
        "name": "Dr. Wilson",
        "availability": {
            "Tuesday": ["10:00am", "11:00am", "1:00pm"],
            "Thursday": ["2:00pm", "3:00pm"],
            "Saturday": ["11:00am", "12:00pm"]
        }
    },
    "Pediatrician": {
        "name": "Dr. Adams",
        "availability": {
            "Tuesday": ["9:00am", "10:00am"],
            "Thursday": ["11:00am", "1:00pm"],
            "Saturday": ["10:00am", "11:00am"]
        }
    },
    "Orthopedic Specialist": {
        "name": "Dr. Brown",
        "availability": {
            "Wednesday": ["10:00am", "11:00am", "12:00pm"],
            "Friday": ["1:00pm", "2:00pm"]
        }
    },
    "Dentist": {
        "name": "Dr. Clark",
        "availability": {
            "Monday": ["9:00am", "10:00am"],
            "Tuesday": ["11:00am", "1:00pm"],
            "Wednesday": ["10:00am", "11:00am", "2:00pm"],
            "Thursday": ["3:00pm", "4:00pm"],
            "Friday": ["9:00am", "10:00am"],
            "Saturday": ["11:00am", "12:00pm"]
        }
    },
    "Gynecologist": {
        "name": "Dr. Davis",
        "availability": {
            "Monday": ["9:00am", "10:00am", "11:00am"],
            "Wednesday": ["1:00pm", "2:00pm"],
            "Friday": ["10:00am", "11:00am"]
        }
    },
    "Psychologist": {
        "name": "Dr. Evans",
        "availability": {
            "Tuesday": ["2:00pm", "3:00pm"],
            "Thursday": ["1:00pm", "3:00pm"]
        }
    },
    "Neurologist": {
        "name": "Dr. Patel",
        "availability": {
            "Monday": ["10:00am", "11:00am"],
            "Thursday": ["2:00pm", "3:00pm"],
            "Saturday": ["10:00am", "11:00am"]
        }
    },
    "Endocrinologist": {
        "name": "Dr. Green",
        "availability": {
            "Monday": ["1:00pm", "2:00pm"],
            "Wednesday": ["10:00am", "11:00am"],
            "Friday": ["3:00pm", "4:00pm"]
        }
    },
    "Urologist": {
        "name": "Dr. White",
        "availability": {
            "Tuesday": ["11:00am", "12:00pm"],
            "Friday": ["2:00pm", "3:00pm"]
        }
    },
    "Oncologist": {
        "name": "Dr. Lee",
        "availability": {
            "Monday": ["10:00am", "11:00am"],
            "Wednesday": ["3:00pm", "4:00pm"],
            "Friday": ["1:00pm", "2:00pm"]
        }
    },
    "Rheumatologist": {
        "name": "Dr. King",
        "availability": {
            "Tuesday": ["10:00am", "11:00am"],
            "Thursday": ["3:00pm", "4:00pm"]
        }
    },
    "Pulmonologist": {
        "name": "Dr. Moore",
        "availability": {
            "Monday": ["9:00am", "10:00am"],
            "Thursday": ["11:00am", "12:00pm"],
            "Saturday": ["2:00pm", "3:00pm"]
        }
    },
    "Ophthalmologist": {
        "name": "Dr. Taylor",
        "availability": {
            "Wednesday": ["11:00am", "12:00pm"],
            "Friday": ["10:00am", "11:00am"],
            "Saturday": ["1:00pm", "2:00pm"]
        }
    }
}

class Chatbot:
    def __init__(self):
        self.context = {}

    def check_doctor_availability(self, doctor_type, day):
        doctor = doctors.get(doctor_type)
        if doctor and day.capitalize() in doctor["availability"]:
            times = ', '.join(doctor["availability"][day.capitalize()])
            self.context['current_doctor'] = doctor_type
            self.context['current_day'] = day.capitalize()
            return f"{doctor['name']} ({doctor_type}) is available on {day} at {times}. Which time would you prefer? Please reply with a specific time (e.g., 10:00am)."
        else:
            available_days = ', '.join(doctor["availability"].keys()) if doctor else "N/A"
            return f"Sorry, {doctor['name']} ({doctor_type}) is not available on {day}. They are available on {available_days}. Please choose another day."

    def confirm_appointment(self, doctor_type, day, time):
        booking_id = random.randint(10000, 99999)
        doctor = doctors.get(doctor_type)
        if doctor and time in doctor["availability"].get(day.capitalize(), []):
            self.context.clear()
            return f"Your appointment with {doctor['name']} ({doctor_type}) on {day} at {time} is confirmed. Your booking ID is {booking_id}. Thank you for using our service!"
        else:
            return f"Sorry, the time {time} is not available on {day} for {doctor['name']} ({doctor_type}). Please choose a different time."

    def handle_follow_up(self, user_input):
        if 'suggested_doctor' in self.context and user_input.lower() == 'yes':
            doctor_type = self.context['suggested_doctor']
            available_days = ', '.join(doctors[doctor_type]["availability"].keys())
            return f"Great! {doctors[doctor_type]['name']} ({doctor_type}) is available on {available_days}. Please specify a day for the appointment."

        if 'current_doctor' in self.context and 'current_day' not in self.context:
            doctor_type = self.context['current_doctor']
            for day in doctors[doctor_type]["availability"].keys():
                if day.lower() in user_input.lower():
                    return self.check_doctor_availability(doctor_type, day)

        if 'current_doctor' in self.context and 'current_day' in self.context:
            time_pattern = re.search(r'\b(\d{1,2}:\d{2}(?:am|pm)?)\b', user_input, re.IGNORECASE)
            if time_pattern:
                time = time_pattern.group(1)
                return self.confirm_appointment(self.context['current_doctor'], self.context['current_day'], time)

        return None

    def get_response(self, user_input):
        follow_up_response = self.handle_follow_up(user_input)
        if follow_up_response:
            return follow_up_response

        for pattern, response in patterns.items():
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                if "Would you like to book an appointment" in response:
                    self.context['suggested_doctor'] = list(doctors.keys())[list(patterns.values()).index(response)]
                    self.context['current_doctor'] = self.context['suggested_doctor']
                return response

        return "Sorry, I couldn't understand you. Could you please clarify or ask about something else?"

chatbot = Chatbot()

def send_message(user_input):
    if user_input.strip() != "":
        chat_log.configure(state="normal")
        chat_log.insert("end", f"You: {user_input}\n", "user")
        chat_log.configure(state="disabled")
        chat_log.yview("end")

        response = chatbot.get_response(user_input)

        chat_log.configure(state="normal")
        chat_log.insert("end", f"Bot: {response}\n", "bot")
        chat_log.configure(state="disabled")
        chat_log.yview("end")

        entry.delete(0, "end")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("Hospital Appointment Chatbot")
root.geometry("600x700")

chat_frame = ctk.CTkFrame(root)
chat_frame.pack(padx=10, pady=(10, 0), fill="both", expand=True)

chat_log = ctk.CTkTextbox(
    chat_frame,
    height=25,
    width=70,
    wrap="word",
    state="disabled"
)
chat_log.pack(padx=10, pady=10, fill="both", expand=True)

chat_log.tag_config("user", foreground="#3498DB")
chat_log.tag_config("bot", foreground="#2ECC71")

input_frame = ctk.CTkFrame(root)
input_frame.pack(padx=10, pady=10, fill="x")

entry = ctk.CTkEntry(input_frame, placeholder_text="Type your message here...")
entry.pack(side="left", padx=(10, 5), pady=5, fill="x", expand=True)

send_button = ctk.CTkButton(
    input_frame,
    text="Send",
    command=lambda: send_message(entry.get())
)
send_button.pack(side="right", padx=(5, 10), pady=5)

root.mainloop()
