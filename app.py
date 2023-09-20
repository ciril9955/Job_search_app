import requests
import streamlit as st

# Define the Jooble API URL and your API key
jooble_api_url = "https://jooble.org/api/"
jooble_api_key = "6f8cd7f1-7dd2-40b5-a72a-8e23dc5ebc4f"  # Replace with your actual Jooble API key

# Streamlit app
st.title("Job Search App")

# User input for job title and location
job_title = st.text_input("Job title:")
location = st.text_input("Location:")

# Button to trigger job search
if st.button("Search Jobs"):
    st.write(f"Searching for '{job_title}' jobs in '{location}'...")

    # Define the request headers for Jooble
    jooble_headers = {
        "Content-Type": "application/json",
    }

    # Define the JSON query parameters for Jooble
    jooble_query = {
        "keywords": job_title,
        "location": location,
    }

    # Send a POST request with the JSON query to Jooble
    try:
        jooble_response = requests.post(jooble_api_url + jooble_api_key, json=jooble_query, headers=jooble_headers)
        jooble_response.raise_for_status()  # Check for any HTTP errors

        # Parse the JSON response data from Jooble
        jooble_data = jooble_response.json()

        # Display job listings from Jooble
        if "jobs" in jooble_data:
            jooble_jobs = jooble_data["jobs"]
            if len(jooble_jobs) > 0:
                st.subheader("Jobs Available:")
                for i, job in enumerate(jooble_jobs):
                    company_name = job.get("company")
                    job_title = job.get("title")
                    experience = job.get("experience")
                    job_location = job.get("location")
                    apply_url = job.get("link")  # Job application URL
                    company_logo_url = job.get("company_logo")  # Company logo URL

                    st.write(f"**Company:** {company_name}")

                    # Display the company logo if the URL is provided and it's a valid image
                    if company_logo_url:
                        try:
                            st.image(company_logo_url, caption=company_name, use_container_width=True)
                        except Exception as img_error:
                            st.write("Error displaying logo:", img_error)

                    st.write(f"**Job Title:** {job_title}")
                    st.write(f"**Experience:** {experience}")
                    st.write(f"**Location:** {job_location}")

                    # Add an "Apply" button for each job listing with a link to the application URL
                    if apply_url:
                        apply_button_label = f"Apply for {job_title} at {company_name}"

                        # Use an iframe to create a clickable link with a "target" attribute
                        st.markdown(
                            f'<a href="{apply_url}" target="_blank"><button>{apply_button_label}</button></a>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.write("No application link provided.")

                    st.write("---")

            else:
                st.warning("No job listings found on Jooble.")
        else:
            st.warning("No job listings found in the Jooble response.")

    except requests.exceptions.RequestException as e:
        st.error(f"Jooble Error: {e}")
