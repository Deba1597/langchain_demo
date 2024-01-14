import streamlit as st
import google.generativeai as genai 
from dotenv import load_dotenv
load_dotenv()
import os
import sqlite3

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows:
        print(row)
    return rows

def main():
    st.set_page_config(page_title='SQL query generator',page_icon=":robot:")
    st.markdown(
        """
            <div style="text-align: center;">
            <h1> SQL query generator </h1>
            <h3>I can generate SQL Query for you</h3>
            <h4>With explaination as well !!!!</h4>
            <p>This tool is a simple tool that allow yoy to geerate SQL queries based on your prompts</p>
        """,
        unsafe_allow_html=True
    )

    text_input = st.text_area('Enter your query here in plain English: ')

    submit = st.button("Generate SQL Query")
    if submit:
        with st.spinner("Generating SQL Query....."):
            template = """
                Create a SQL Query snippet using the below text:
                    ```
                    {text_input}
                    ```
                    I just want a SQL Query.

                """
            formated_template = template.format(text_input=text_input)
            
            # st.write(formated_template)
            response = model.generate_content(formated_template)
            sql_query = response.text
            
            # st.write(sql_query)
            sql_query = sql_query.strip().lstrip("```sql").rstrip("```")

            expected_output = """
                What would be the expected response of this SQL Query snippet:
                    ```
                    {sql_query}
                    ```
                    Provide sample tabular response With no explanation :

                """
            expected_output_format = expected_output.format(sql_query=sql_query)
            eoutput = model.generate_content(expected_output_format)
            eoutput = eoutput.text
            # st.write(eoutput)

            explaination = """
                Explain this SQL Query:
                    ```
                    {sql_query}
                    ```
                    Plese provide with simplest of explanation :

                """
            explanation_formated = explaination.format(sql_query=sql_query)
            explane = model.generate_content(explanation_formated)
            explaination = explane.text
            # st.write(explaination)

            with st.container():
                st.success('SQL Query generated sucessfully! Here is your Query below')
                st.code(sql_query, language='sql')

                st.success("Expected output of the SQL Query will be: ")
                st.markdown(eoutput)

                st.success("Explanation of this SQL Query: ")
                st.markdown(explaination)


        # response = model.generate_content(text_input)
        # print(response.text)
        # st.write(response.text)

main()