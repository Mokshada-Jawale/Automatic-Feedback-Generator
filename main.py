import streamlit as st
from groq import Groq

def generate_summary(input_dict):
    # Update the API key with your valid API key
    groq_api = "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"
    client = Groq(api_key=groq_api)
    default_instruction = """
    You will receive an input context in the form of a dictionary containing 'question' and 'answer' keys. Perform the following steps:

    step 1: Read the question and the corresponding answer carefully.
    step 2: Analyze how well the answer addresses the question and provide a concise, one-line feedback on how much of the answer is correct or relevant to the question.
    step 3: Suggest ways to improve the answer by mentioning specific information or aspects should be included to make the answer more complete or accurate with respect to the question.
    step 4: The feedback should be within 6-7 lines.
    step 5: Do not copy the question or answer verbatim. Analyze the answer by considering question and give me feedback.
    step 6: if answer is totally different from question, mention the answer is releted to and tells what should be answer.
    step 7: give specific feedback like what is incorrect and what points should be added to answer for improvement.
    step 8: try to write feedback in human language, it should be easy to understand. and avoid ai generated language.
    step 9: give specific details rather than generalize statements.
    step 10: give study material links from geeksforgeeks, tutorial points, javatpoint for better answering the question.

    Input context: {input_dict}
    """

    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": default_instruction},
            {"role": "user", "content": f"Generate a summary for the given context {input_dict}"},
        ],
        model="llama3-70b-8192",
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        # stop=None,
        # stream=False,
    )
    # print(chat_completion)

    llm_output = chat_completion.choices[0].message.content
    llm_output = llm_output.replace("**", "")
    llm_output = llm_output.replace("*", "")
    llm_output = llm_output.replace("Here is a concise summary of the feedback:", "")
    return llm_output

def process_data(data):
    feedback = {}
    for data_dict in data:
        summary = generate_summary(data_dict)
        feedback[data_dict['question']] = summary
    return feedback

st.title("Personalized Q&A Feedback Generator")

# Input section
st.header("Input the Question and Answer")
question = st.text_input("Question", "Enter your question here")
answer = st.text_area("Answer", "Enter your answer here")

if st.button("Generate Feedback"):
    data = [{'question': question, 'answer': answer}]
    feedback_dict = process_data(data)
    for question, summary in feedback_dict.items():
        st.subheader("Question and Answer")
        st.write(f"**Question**: {question}")
        st.write(f"**Answer**: {answer}")
        st.subheader("Feedback")
        st.write(summary)
