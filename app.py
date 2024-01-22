import os
from dotenv import load_dotenv

load_dotenv()

import google.generativeai as genai
from flask import Flask, render_template, request, send_from_directory
from fuzzywuzzy import fuzz


genai.configure(api_key=os.environ.get("API_KEY"))

from google.generativeai import GenerativeModel

# Assume you have some data from your website
website_data = {
    "faq": {
        "What is your website about?": "Our website is a comprehensive document creation platform. We specialize in generating professional documents such as CVs, application letters, receipts, invoices, and more. With user-friendly tools, industry-specific templates, and flexible pricing plans, we empower individuals and businesses to craft polished and tailored documents effortlessly. Whether you're advancing your career or managing business documentation, our platform streamlines the process, providing a one-stop solution for all your document creation needs.",
        "How to contact support?": "You can contact support by phone 0551389510",
        "How does your service work?": "Our service is user-friendly. Simply navigate to the appropriate section on our website, provide the necessary information, and our platform will generate a professionally crafted document for you.",
        "What types of documents can I create on your website?": "Our platform allows you to create a wide range of documents, including CVs, application letters, receipts, invoices, and more. If you need a specific type of document, explore our menu for the available options.",   
        "Is my information secure when using your service?": "Yes, we take data security seriously. We use industry-standard encryption protocols to ensure the confidentiality and security of your information. Your data will only be used for the purpose of generating the requested document.",
        "Can I edit the documents after they are generated?": "Absolutely. Once a document is generated, you have the option to download and edit it as needed. We understand that personalization is important, and our platform is designed to be flexible.",
        "How much does it cost to use your service?": "Our pricing depends on the type and complexity of the document you're creating. You can find detailed pricing information on our website. We offer both free and premium plans to cater to different needs.",
        "Do you provide templates for different industries?": "Yes, our platform offers templates tailored for various industries and purposes. You can choose a template that aligns with your profession or the purpose of the document, and then customize it to suit your specific needs.",
        "Can I get a refund if I'm not satisfied with the document?": "We strive to ensure customer satisfaction. If you encounter any issues or are dissatisfied with the document, please reach out to our customer support. We will work with you to address any concerns and provide a solution.",
        "Will you share my information with anyone?": "Nothing of such please, we don't share your information with anyone, infact our website does not save any data provided.",
        "Do you keep my generated documen t after sent to me?": "No, we don't keep any document after sent to you. You must download it as needed.",
        "Can I download the documents in different file formats?": "Yes, our platform supports multiple file formats. After generating a document, you can typically download it in popular formats such as PDF, Word, or plain text, depending on your preference.",
         "Are the documents created by your platform ATS-friendly (Applicant Tracking System)?": "Yes, we optimize our templates to be compatible with Applicant Tracking Systems commonly used by employers. This increases the chances of your resume or application being successfully parsed by these systems.",
        "Can I use your service for business-related documents like proposals and contracts?": "Yes, our service can be used for a variety of business-related documents, including proposals and contracts. Explore the business section on our website to access templates tailored for professional use.",
         "Do you offer a spell-check or grammar-check feature?": "Yes, our platform includes basic spell-check and grammar-check features. However, we recommend thoroughly reviewing the document to ensure accuracy and appropriateness for your specific context.",
        # Add more FAQ data as needed
    },
    # Add other website data as needed
}

app = Flask(__name__)

# Configure and create the GenerativeModel object (outside the route for efficiency)
model = GenerativeModel(
    model_name="gemini-pro",
    generation_config={
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    },
    safety_settings=[
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    ],
)



def format_generated_text(generated_text):
    # Remove leading asterisks and whitespaces from each line
    cleaned_lines = [line.strip('- ').lstrip('*').strip() for line in generated_text.split('\n')]

    # Join cleaned lines with HTML line breaks
    formatted_text = '<br>'.join(cleaned_lines)
    
    return formatted_text



def find_closest_match(question, data):
    max_similarity = 0
    closest_match = None

    for key, value in data.items():
        similarity = fuzz.ratio(question, key)
        if similarity > max_similarity:
            max_similarity = similarity
            closest_match = value

    return closest_match, max_similarity

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_response', methods=['POST'])
def generate_response():
    if request.method == 'POST':
        prompt = request.form['question']

        # Check if the prompt matches any predefined questions in your website data
        for category, data in website_data.items():
            if prompt in data:
                response = data[prompt]
                return render_template('index.html', question=prompt, response=response)

        # If no exact match is found, find the closest match using fuzzy matching
        closest_match, similarity = find_closest_match(prompt, website_data.get("faq", {}))

        # Set a threshold for similarity (adjust as needed)
        similarity_threshold = 80

        if similarity >= similarity_threshold:
            return render_template('index.html', question=prompt, response=closest_match)
        else:
            # If the similarity is below the threshold, use the generative model
            response = model.generate_content([prompt]).text
            return render_template('index.html', question=prompt, response=response)

if __name__ == '__main__':
    app.run(debug=False, port=int(os.environ.get("PORT", 5000)))



