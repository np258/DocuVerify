**DocuVerify: Vendor Spec & Compliance Copilot**

DocuVerify is a proof-of-concept (POC) application designed to automate unstructured data extraction from vendor product specification sheets and validate them against retail compliance policies.

The system uses a Human-in-the-Loop architecture, allowing automated document ingestion while requiring human verification before committing records to downstream enterprise systems.

**Live Demo** 
Access the interactive web application here: [DocuVerify Web App](https://docuverify-6ounfmeylyhhazuf7rrdhw.streamlit.app/)

**Key Features:**

    PDF Document Ingestion: Extracts raw text from vendor spec sheets using standard Python processing.

    Automated Rule Validation: Checks extracted fields against policy requirements (e.g., bilingual French packaging, standard retail ABV limits, volume unit formatting).

    Split-Screen Verification UI: Displays extracted text side-by-side with an editable verification form for real-time review.

    Dataverse Ready Payload: Formats approved records into structured JSON staged for Microsoft Dataverse or D365 product catalog integration.

**Project Structure**

    app.py: Main Streamlit web interface and form handling.

    compliance.py: Core PDF extraction parser and compliance rule engine.

    create_mock_pdfs.py: Utility script to generate sample compliant and non-compliant test PDFs.

    requirements.txt: Python package dependencies.

**Local Setup & Execution (PowerShell)**

  Activate Virtual Environment:
    
    .\venv\Scripts\Activate.ps1

  Install Dependencies:
    
    python -m pip install -r requirements.txt

  Generate Sample Data:
    
    python create_mock_pdfs.py

  Run the Application:
    
    python -m streamlit run app.py
