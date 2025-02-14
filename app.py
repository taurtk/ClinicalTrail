import os
import json
from flask import Flask, render_template, request, jsonify
import requests
from openai import OpenAI

app = Flask(__name__)

# Constants
DEEPSEEK_API_KEY = "301a3eec-c4c9-4920-836e-7fdc0b3639d4"
DEEPSEEK_BASE_URL = "https://api.sambanova.ai/v1"
CLINICAL_TRIALS_API_URL = "https://clinicaltrials.gov/api/v2"

# Initialize DeepSeek Client
deepseek_client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_BASE_URL,
)

def match_trial(patient_data):
    """
    Uses DeepSeek AI to match a patient with a suitable clinical trial.
    
    :param patient_data: Dictionary containing patient medical data.
    :return: AI-generated recommendation for a clinical trial.
    """
    messages = [
        {"role": "system", "content": "You are a clinical trial matching expert."},
        {"role": "user", "content": f"Match this patient to a relevant clinical trial: {json.dumps(patient_data)}"}
    ]
    
    response = deepseek_client.chat.completions.create(
        model="DeepSeek-R1-Distill-Llama-70B",
        messages=messages,
        temperature=0.1,
        top_p=0.1
    )
    
    return response.choices[0].message.content

@app.route('/', methods=['GET', 'POST'])
def index():
    patient_data = {
        'age': 30,
        'condition': '',
        'location': '',
        'symptoms': '',
        'previous_treatment': ''
    }
    if request.method == 'POST':
        patient_data = {
            'age': int(request.form.get('age', 30)),
            'condition': request.form.get('condition', ''),
            'location': request.form.get('location', ''),
            'symptoms': request.form.get('symptoms', ''),
            'previous_treatment': request.form.get('previous_treatment', '')
        }
        
        recommendation = match_trial(patient_data)
        
        # filters = {
        #     'status': 'RECRUITING',
        #     'condition': patient_data['condition']
        # }
        trials = fetch_trials()
        print(trials)
        return render_template('index.html', 
                               recommendation=recommendation, 
                               trials=trials.get('studies', []),
                               patient_data=patient_data)
    
    return render_template('index.html', recommendation=None, trials=[], patient_data=patient_data)

def fetch_trials():
    """
    Fetch clinical trials based on given filters from mock data.
    
    :param filters: Dictionary of filters to apply to the mock data.
    :return: Mock JSON response.
    """
    # print("Incoming filters:", filters)  # Debug print
    
    mock_data = {
        "studies": [
            {
                "protocolSection": {
                    "identificationModule": {
                        "briefTitle": "Study of Novel Treatment for Cancer",
                        "detailedDescription": "A Phase III clinical trial evaluating the efficacy of a new immunotherapy treatment for various types of cancer.",
                        "location": "New York, NY",
                        "condition": "Cancer"
                    },
                    "statusModule": {
                        "overallStatus": "RECRUITING"
                    }
                }
            },
            {
                "protocolSection": {
                    "identificationModule": {
                        "briefTitle": "Diabetes Type 2 Management Study",
                        "detailedDescription": "Investigation of a new oral medication for better management of Type 2 Diabetes with reduced side effects.",
                        "location": "Los Angeles, CA",
                        "condition": "Diabetes"
                    },
                    "statusModule": {
                        "overallStatus": "RECRUITING"
                    }
                }
            },
            {
                "protocolSection": {
                    "identificationModule": {
                        "briefTitle": "Asthma Treatment Clinical Trial",
                        "detailedDescription": "Testing a new inhaler device and medication combination for better asthma control.",
                        "location": "Boston, MA",
                        "condition": "Asthma"
                    },
                    "statusModule": {
                        "overallStatus": "RECRUITING"
                    }
                }
            },
            {
                "protocolSection": {
                    "identificationModule": {
                        "briefTitle": "Arthritis Pain Management Study",
                        "detailedDescription": "Evaluating a novel pain management approach for patients with rheumatoid arthritis.",
                        "location": "Chicago, IL",
                        "condition": "Arthritis"
                    },
                    "statusModule": {
                        "overallStatus": "RECRUITING"
                    }
                }
            }
        ]
    }

    # Return all studies if no condition specified
   

      # Debug print
    return {"studies": mock_data["studies"]}

if __name__ == '__main__':
    app.run(debug=True)