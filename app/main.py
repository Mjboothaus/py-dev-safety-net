from pathlib import Path

import duckdb
import pandas as pd
import plotly.express as px
import streamlit as st
from great_tables import GT


def load_and_save_iris(method="duckdb"):
    try:
        # Load Iris dataset
        if method == "pandas":
            df = pd.read_csv(
                "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data",
                names=[
                    "sepal_length",
                    "sepal_width",
                    "petal_length",
                    "petal_width",
                    "species",
                ],
            )
        elif method == "duckdb":
            conn = duckdb.connect()
            df = conn.execute(
                """
                SELECT * FROM read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', 
                columns={'sepal_length': 'DOUBLE', 'sepal_width': 'DOUBLE', 'petal_length': 'DOUBLE', 'petal_width': 'DOUBLE', 'species': 'VARCHAR'})
            """
            ).fetchdf()
            conn.close()
        else:
            raise ValueError("Invalid method. Use 'pandas' or 'duckdb'.")

        # Save to DuckDB
        conn = duckdb.connect("iris.duckdb")
        conn.execute("CREATE OR REPLACE TABLE iris AS SELECT * FROM df")
        conn.close()
    except Exception as e:
        print(f"An error occurred: {e}")


# Load data from DuckDB
def connect_data():
    if not Path("iris.duckdb").exists():
        load_and_save_iris(method="duckdb")
    return duckdb.connect("iris.duckdb")


# Streamlit UI
def main_app():
    st.title("Iris Dataset Explorer")

    # Default query to demonstrate filtering by species count
    default_query = """
    SELECT species, COUNT(*) AS count 
    FROM iris 
    GROUP BY species 
    ORDER BY count DESC;
    """

    conn = connect_data()

    # Display data using GreatTables for interactive exploration

    tab1, tab2 = st.tabs(["Data", "Visualisation"])

    with tab2:
        st.write("### Interactive Data Exploration")
        df = conn.execute("SELECT * FROM iris").fetchdf()
        table = GT(df)

        st.markdown(table.as_raw_html(), unsafe_allow_html=True)

    with tab1:
        # Plotly Visualisation: Scatter Plot

        st.write("### Visualise Sepal Dimensions")
        fig = px.scatter(
            df,
            x="sepal_length",
            y="sepal_width",
            color="species",
            title="Sepal Length vs Sepal Width by Species",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Filter by species and visualise petal dimensions

        species = st.selectbox("Select Species", df["species"].unique())
        filtered_df = df[df["species"] == species]

        st.write(f"### Filtered Data: {species}")
        fig_filtered = px.scatter(
            filtered_df,
            x="petal_length",
            y="petal_width",
            title=f"Petal Dimensions for {species}",
        )
        st.plotly_chart(fig_filtered, use_container_width=True)

        # Custom SQL Query Input and Execution

        st.write("### Run Custom SQL Query")
        user_query = st.text_area("Enter your SQL query:", default_query)
        if st.button("Run Query"):
            try:
                query_result = conn.sql(user_query).df()
                st.write("Query Results:")
                st.dataframe(query_result)
            except Exception as e:
                st.error(f"Error executing query: {e}")

    conn.close()


if __name__ == "__main__":
    main_app()

    # Uncomment the following lines to load and save the Iris dataset

    # # Load and save the Iris dataset using DuckDB
    # load_and_save_iris(method="duckdb")

    # # Load and save the Iris dataset using Pandas
    # load_and_save_iris(method="pandas")
