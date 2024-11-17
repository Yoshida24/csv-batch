import streamlit as st
import pandas as pd
from utils import validate_csv, get_downloadable_csv, get_column_dtypes, generate_summary_stats
from processors import DataProcessor
import io

# Page configuration
st.set_page_config(
    page_title="CSV Data Processor",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.title("CSV Data Processor")
    st.markdown("Upload your CSV file for processing and analysis")

    # Initialize session state
    if 'df' not in st.session_state:
        st.session_state.df = None
    if 'processed_df' not in st.session_state:
        st.session_state.processed_df = None

    # File upload section
    with st.container():
        st.markdown('<div class="uploadSection">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded_file is not None:
            # Validate and load CSV
            is_valid, message, df = validate_csv(uploaded_file)
            
            if is_valid:
                st.session_state.df = df
                st.success("File uploaded successfully!")
            else:
                st.error(message)
                return

    # Data processing section
    if st.session_state.df is not None:
        st.header("Data Preview")
        st.dataframe(st.session_state.df.head(), use_container_width=True)

        # Column selection
        columns = st.session_state.df.columns.tolist()
        selected_columns = st.multiselect("Select columns for processing", columns, default=columns)

        # Processing options
        st.header("Processing Options")
        col1, col2 = st.columns(2)

        with col1:
            process_duplicates = st.checkbox("Remove duplicates")
            handle_missing = st.checkbox("Handle missing values")
            missing_method = st.selectbox(
                "Missing values method",
                ["mean", "median", "mode"],
                disabled=not handle_missing
            )

        with col2:
            normalize_data = st.checkbox("Normalize numeric columns")
            remove_outliers = st.checkbox("Remove outliers")
            outlier_threshold = st.slider(
                "Outlier threshold (z-score)",
                1.0, 5.0, 3.0,
                disabled=not remove_outliers
            )

        # Process button
        if st.button("Process Data"):
            processed_df = st.session_state.df.copy()

            with st.spinner("Processing data..."):
                # Apply selected operations
                if process_duplicates:
                    processed_df = DataProcessor.remove_duplicates(processed_df, selected_columns)

                if handle_missing:
                    processed_df = DataProcessor.fill_missing_values(
                        processed_df, selected_columns, missing_method
                    )

                if normalize_data:
                    processed_df = DataProcessor.normalize_columns(processed_df, selected_columns)

                if remove_outliers:
                    processed_df = DataProcessor.remove_outliers(
                        processed_df, selected_columns, outlier_threshold
                    )

                st.session_state.processed_df = processed_df
                st.success("Processing complete!")

        # Results section
        if st.session_state.processed_df is not None:
            st.header("Processed Data Preview")
            st.dataframe(st.session_state.processed_df.head(), use_container_width=True)

            # Summary statistics
            st.header("Summary Statistics")
            stats = generate_summary_stats(st.session_state.processed_df)
            for col, col_stats in stats.items():
                with st.expander(f"Statistics for {col}"):
                    for stat_name, value in col_stats.items():
                        st.write(f"{stat_name}: {value:.2f}")

            # Download processed data
            csv = get_downloadable_csv(st.session_state.processed_df)
            st.download_button(
                label="Download Processed Data",
                data=csv,
                file_name="processed_data.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()
