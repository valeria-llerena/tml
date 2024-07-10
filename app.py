# main_app.py
import streamlit as st
from streamlit_option_menu import option_menu
import upload
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Fraud Detection System")

# Initialize session state if not already done
if 'uploaded_df' not in st.session_state:
    st.session_state['uploaded_df'] = None

# Sidebar menu
with st.sidebar: 
    selected = option_menu(
        menu_title="Menu", 
        options=["Add Transactions", "Add Connection", "Reports"],
    )

# Handle menu selection
if selected == "Add Transactions":
    uploaded_df = upload.upload_and_predict()
    if uploaded_df is not None:
        st.session_state['uploaded_df'] = uploaded_df

if selected == "Add Connection": 
    st.title("Which of the supported systems do you want to connect with")

if selected == "Reports": 
    st.title("Reports on the transaction uploaded")

    def plot_fraud_report(df):
        # Check if DataFrame is not empty
        if df is not None and not df.empty:
            # Count the number of fraudulent and non-fraudulent transactions
            fraud_counts = df['Prediction'].value_counts()
            fraud_labels = ["Not Fraudulent", "Fraudulent"]

            # Create a bar plot
            fraud_data = pd.DataFrame({
                'Transaction Type': fraud_labels,
                'Count': fraud_counts.values
            })
            # Display the plot in Streamlit
            st.title("Number of Fraudulent vs Non-Fraudulent Transactions")
            st.bar_chart(fraud_data )
            
            # Filter fraudulent transactions and show their amounts
            fraudulent_transactions = df[df['Prediction'] == 'Fraudulent']

            st.write("Fraudulent Transactions Amounts:")
            st.write(fraudulent_transactions['Amount'])

            # Create a bar plot for amounts of fraudulent transactions
            plt.figure(figsize=(10, 6))
            sns.barplot(x=fraudulent_transactions.index, y=fraudulent_transactions['Amount'])
            plt.xlabel("Transaction Index")
            plt.ylabel("Amount")
            plt.title("Amounts of Fraudulent Transactions")
            st.pyplot(plt)
            
        else:
            st.write("No data available for generating the report.")

    # Plot the report if uploaded_df is available in session state
    if st.session_state['uploaded_df'] is not None:
        plot_fraud_report(st.session_state['uploaded_df'])
    else:
        st.write("Please upload a file in the 'Add Transactions' section.")



