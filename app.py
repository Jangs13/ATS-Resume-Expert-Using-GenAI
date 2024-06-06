from dotenv import load_dotenv
import base64
import streamlit as st
import os
import io
from PIL import Image
import requests
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Save the uploaded PDF to a file
        with open("uploaded.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Upload the PDF to an online service for conversion
        with open("uploaded.pdf", "rb") as f:
            response = requests.post(
                "https://api.pdf2jpg.net/v1/api/convert",
                files={"file": f}
            )

        if response.status_code == 200:
            data = response.json()
            if data["success"]:
                # Download the first image from the response
                image_url = data["images"][0]
                image_response = requests.get(image_url)
                img_byte_arr = io.BytesIO(image_response.content)
                pdf_parts = [
                    {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_byte_arr.getvalue()).decode()
                    }
                ]
                return pdf_parts
            else:
                raise Exception("Failed to convert PDF to image: " + data["error"])
        else:
            raise Exception("Failed to upload PDF for conversion")
    else:
        raise FileNotFoundError("No file uploaded")


## Streamlit App

st.set_page_config(page_title="ATS Resume Expert", layout="wide")

# CSS for glowing buttons and icons
st.markdown("""
    <style>
    .glow-button {
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 5px;
        background-color: #2e7bcf;
        color: white;
        border: none;
        cursor: pointer;
        box-shadow: 0 0 20px rgba(46, 123, 207, 0.6);
        transition: box-shadow 0.3s ease-in-out;
    }
    .glow-button:hover {
        box-shadow: 0 0 40px rgba(46, 123, 207, 1);
    }
    .icon-row {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 40px;
        margin-top: 20px;
    }
    .icon-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    .icon {
        width: 60px;
        height: 60px;
    }
    .icon-name {
        margin-top: 5px;
        font-size: 14px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Landing Page Layout
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def go_to_scanner():
    st.session_state.page = 'scanner'

if st.session_state.page == 'landing':
    st.image("https://as1.ftcdn.net/v2/jpg/08/09/16/42/1000_F_809164245_wal25tvomDyad6tBc3OVOpDzqx0bsnRK.jpg", use_column_width=True)  # Use your uploaded image path
    st.markdown("""
        # Land More Job Interviews with Our Resume Scanner

        Get hired faster with an ATS-friendly resume that highlights the right skills. Our resume scanner helps you write the perfect resume so that you stand out from the competition.

        ### How It Works
        1. Upload your resume and job description.
        2. Get a detailed analysis of your resume's match with the job description.
        3. Identify missing keywords and areas for improvement.

        Click the button below to get started!
    """)
    if st.button("Scan My Resume", on_click=go_to_scanner, key="scan_my_resume"):
        go_to_scanner()

    st.markdown("""
        ## About This Project

        This project was developed to help job seekers improve their resumes and increase their chances of getting hired. Here’s how we made it:
    """)

    st.markdown("""
        ### Technology Stack
        """)
    st.markdown("""
        <div class="icon-row">
            <div class="icon-col">
                <img class="icon" src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python">
                <div class="icon-name">Python</div>
            </div>
            <div class="icon-col">
                <img class="icon" src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit">
                <div class="icon-name">Streamlit</div>
            </div>
            <div class="icon-col">
                <img class="icon" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Google_Gemini_logo.svg/516px-Google_Gemini_logo.svg.png" alt="Google Generative AI">
                <div class="icon-name">Google Generative AI</div>
            </div>
            <div class="icon-col">
                <img class="icon" src="https://pandas.pydata.org/static/img/pandas_mark.svg" alt="Pandas">
                <div class="icon-name">Pandas</div>
            </div>
            <div class="icon-col">
                <img class="icon" src="https://images.prismic.io/plotly-marketing-website-2/8f977c91-7b4e-4367-8228-26fbba2506e4_69e12d6a-fb65-4b6e-8423-9465a29c6028_plotly-logo-sm.png?auto=compress%2Cformat&fit=max&w=128" alt="Plotly">
                <div class="icon-name">Plotly</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        ### Features
        - **Resume Analysis**: Upload a resume and job description to get a detailed analysis of how well they match.
        - **Keyword Matching**: Identify missing keywords in the resume.
        - **Interactive Visualizations**: Visualize the analysis results with interactive charts.
    """)

    st.markdown("""
        ### Development Process
        1. **Ideation**: Identified the need for a tool that helps job seekers optimize their resumes.
        2. **Design**: Created wireframes and designed the user interface.
        3. **Implementation**: Developed the backend logic and integrated the frontend with Streamlit.
        4. **Testing**: Conducted thorough testing to ensure the tool works as expected.
        5. **Deployment**: Deployed the application for public use.

        We hope you find this tool helpful in your job search!
    """)

elif st.session_state.page == 'scanner':
    st.title("Applicant Tracking Systems (ATS)")

    st.header("Job Description")
    input_text = st.text_area("Enter the job description here")

    st.header("Upload your resume (PDF)")
    uploaded_file = st.file_uploader("Choose a file...", type=["pdf"])

    if uploaded_file is not None:
        st.success("PDF Uploaded Successfully")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Tell Me About the Resume", key="about_resume", help="Get a detailed analysis of your resume against the job description."):
            submit1 = True
        else:
            submit1 = False

    with col2:
        if st.button("Percentage Match", key="percentage_match", help="Get the percentage match between your resume and the job description."):
            submit3 = True
        else:
            submit3 = False

    input_prompt1 = """
    You are an experienced Technical Human Resource Manager. Your task is to review the provided resume against the job description.
    Please share your professional evaluation on whether the candidate's profile aligns with the role.
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
    """

    input_prompt3 = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full Stack Web Development, Big Data Engineering, DevOps, Data Analyst and deep ATS functionality. Your task is to evaluate the resume against the provided job description.

    Please provide the following:
    1. The percentage match between the resume and the job description.
    2. Keywords missing from the resume.
    3. Final thoughts on the overall fit of the candidate for the job.

    Start with the percentage match, followed by the missing keywords, and conclude with your final thoughts.
    """

    response = ""

    if submit1:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt1)
            st.subheader("The Response is")
            st.write(response)
        else:
            st.error("Please upload the resume")

    if submit3:
        if uploaded_file is not None:
            pdf_content = input_pdf_setup(uploaded_file)
            response = get_gemini_response(input_text, pdf_content, input_prompt3)
            st.subheader("The Response is")
            st.write(response)
            keywords = ["SQL", "Python", "R", "Java", "C++", "AWS", "Azure", "Tableau", "Power BI", "Git", "Jira", "Scrum", "Agile", "DataOps", "MLOps", "CI/CD"]
            found_keywords = [kw for kw in keywords if kw.lower() in response.lower()]
            missing_keywords = list(set(keywords) - set(found_keywords))
            st.write("The following keywords are missing from the resume:")
            st.write(missing_keywords)
        else:
            st.error("Please upload the resume")

