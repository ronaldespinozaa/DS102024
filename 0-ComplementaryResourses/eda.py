import pandas as pd
import numpy as np

class EDAToolkit:
    def __init__(self, df, date_formats):
        """
        Initialize the EDAToolkit with a dataframe and a dictionary of date formats.
        """
        if not isinstance(df, pd.DataFrame):
            raise ValueError("The input must be a pandas DataFrame.")
        self.df = df
        self.date_formats = date_formats  # Diccionario de formatos de fecha

    def validate_dtypes(self):
        """
        Check and report inconsistencies in data types.
        """
        print("=== Data Types Validation ===")
        dtypes_summary = self.df.dtypes.value_counts()
        print("Data Types Summary:\n", dtypes_summary)

        # Look for mixed-type columns
        mixed_columns = [
            col for col in self.df.columns
            if self.df[col].apply(type).nunique() > 1
        ]
        if mixed_columns:
            print("\nMixed-Type Columns Detected:")
            for col in mixed_columns:
                print(f" - {col}: {self.df[col].apply(type).value_counts().to_dict()}")
        else:
            print("\nNo mixed-type columns detected.")



    def analyze_datetime_columns(self):
        """
        Analyze columns of type datetime and attempt to convert object columns
        to datetime only if their format matches one in the `date_formats` dictionary.
        """
        print("=== Analysis of Datetime Columns ===")
        datetime_cols = self.df.select_dtypes(include=["datetime"]).columns

        # Attempt to identify potential datetime columns
        potential_datetime_cols = [
            col for col in self.df.columns if self.df[col].dtype == "object"
        ]
        for col in potential_datetime_cols:
            for fmt, desc in self.date_formats.items():
                try:
                    # Attempt to parse using the known format
                    test_conversion = pd.to_datetime(self.df[col], format=fmt, errors="coerce")
                    
                    # Check if conversion was successful
                    if test_conversion.notna().sum() > 0:  # At least some valid dates
                        print(f"Column '{col}' matches format '{desc}' ({fmt}). Converting.")
                        self.df[col] = test_conversion
                        datetime_cols = datetime_cols.append(pd.Index([col]))
                        break  # No need to check other formats if one works
                except Exception as e:
                    continue  # Skip to next format if current format doesn't work

        if datetime_cols.empty:
            print("No datetime columns found.")
            return

        for col in datetime_cols:
            print(f"\nColumn: {col}")
            min_date = self.df[col].min()
            max_date = self.df[col].max()
            print(f"  - Date Range: {min_date} to {max_date}")
            missing_dates = self.df[col].isnull().sum()
            print(f"  - Missing Dates: {missing_dates}")
            unique_dates = self.df[col].nunique()
            print(f"  - Unique Dates: {unique_dates}")

    def analyze_percentage_columns(self):
        """
        Analyze columns with percentage data to numerical format, and return a summary table
        with unique counts and cardinality classification for all object columns.
        """
        summary = []

        for col in self.df.select_dtypes(include=['object']).columns:
            unique_count = self.df[col].nunique()  # Contar valores únicos
            porc_card = (self.df[col].nunique() / len(self.df)) * 100
            # Clasificar la cardinalidad
            if unique_count < 10:
                cardinality = "Low Cardinality"
            elif unique_count <= 50:
                cardinality = "Medium Cardinality"
            else:
                cardinality = "High Cardinality"

            # Verificar si contiene porcentajes y realizar la transformación
            if self.df[col].str.contains('%', na=False).any():
                try:
                    mask = self.df[col].str.contains('%', na=False)
                    self.df.loc[mask, col] = (
                        self.df.loc[mask, col]
                        .str.replace('%', '', regex=False)
                        .astype(float) / 100
                    )
                    transformation_status = "Transformed to Numeric"
                except Exception as e:
                    transformation_status = f"Error: {e}"
            else:
                transformation_status = "No Transformation Needed"

            # Agregar resultados al resumen
            summary.append({
                "Column": col,
                "Unique Count": unique_count,
                "Cardinality (%)": porc_card,
                "Cardinality": cardinality,
            })

        # Crear un DataFrame resumen
        return print('Summary', pd.DataFrame(summary).sort_values(by='Cardinality'))

    def data_quality_report(self):
        """
        Generate a comprehensive data quality report.
        """
        print("=== Data Quality Report ===")
        report = pd.DataFrame({
            "Data Type": self.df.dtypes,
            "Missing Values": self.df.isnull().sum(),
            "Missing (%)": (self.df.isnull().sum() / len(self.df)) * 100,
            # "Unique Values": self.df.nunique(),
            # "Most Frequent Value": self.df.mode().iloc[0],
            # "Most Frequent Count": self.df.apply(lambda x: x.value_counts().max()),
        }).sort_values(by="Missing (%)", ascending=False)
        print(report)

    def descriptive_analysis(self):
        """
        Perform a detailed descriptive analysis for each column based on its data type.
        - Float columns: Mean, Median, Variance, Min, Max, Std, Kurtosis, Skewness.
        - Object columns: Mode, Unique Count, Cardinality.
        - Datetime columns: Min Date, Max Date, Range (Max - Min).
        - Other types: Basic descriptive statistics if applicable.
        """
        from scipy.stats import kurtosis, skew
        
        results = []

        for col in self.df.columns:
            if self.df[col].dropna().empty:
                analysis = {"Column": col, "Data Type": "-"}
            else:
                dtype = self.df[col].dtype
                analysis = {"Column": col, "Data Type": dtype.name}

                if np.issubdtype(dtype, np.number):  # Análisis para columnas numéricas
                    analysis.update({
                        "Mean": self.df[col].mean(),
                        "Median": self.df[col].median(),
                        "Variance": self.df[col].var(),
                        "Min": self.df[col].min(),
                        "Max": self.df[col].max(),
                        "Std Dev": self.df[col].std(),
                        "Kurtosis": kurtosis(self.df[col], ),
                        "Skewness": skew(self.df[col], ),
                    })
                    results.append(analysis)

        return print("Descriptive Analysis Results:",pd.DataFrame(results))

# Usage Example

data=pd.read_csv(r"2-DataAnalysis\2-Pandas\Practica\1-World_Food_Facts\food_100.csv")

# Usage Example
if __name__ == "__main__":
    date_formats = {
    "DD-MM-YYYY": "%d-%m-%Y",    # 26-08-1987
    "DD/MM/YYYY": "%d/%m/%Y",    # 26/08/1987
    "YYYY-MM-DD": "%Y-%m-%d",    # 1987-08-26
    "YYYY/MM/DD": "%Y/%m/%d",    # 1987/08/26
    "MM-DD-YYYY": "%m-%d-%Y",    # 08-26-1987
    "MM/DD/YYYY": "%m/%d/%Y",    # 08/26/1987
    "DD.MM.YYYY": "%d.%m.%Y",    # 26.08.1987
    "YYYY.MM.DD": "%Y.%m.%d",    # 1987.08.26
    "DD-MMM-YYYY": "%d-%b-%Y",   # 26-Aug-1987
    "DD-MMMM-YYYY": "%d-%B-%Y",  # 26-August-1987
    "MMM DD, YYYY": "%b %d, %Y", # Aug 26, 1987
    "MMMM DD, YYYY": "%B %d, %Y",# August 26, 1987
    "YYYY-MM-DD HH:MM:SS": "%Y-%m-%d %H:%M:%S",  # 1987-08-26 14:30:00
    "YYYY/MM/DD HH:MM:SS": "%Y/%m/%d %H:%M:%S",  # 1987/08/26 14:30:00
    "DD-MM-YYYY HH:MM:SS": "%d-%m-%Y %H:%M:%S",  # 26-08-1987 14:30:00
    "DD/MM/YYYY HH:MM:SS": "%d/%m/%Y %H:%M:%S",  # 26/08/1987 14:30:00
    "HH:MM:SS": "%H:%M:%S",        # 14:30:00
    "YYYY-MM": "%Y-%m",           # 1987-08
    "DD-MM-YYYY HH:MM": "%d-%m-%Y %H:%M"  # 26-08-1987 14:30
}
    df = pd.DataFrame(data)
    eda = EDAToolkit(df, date_formats)

    # Validate data types
    eda.validate_dtypes()

    # Analyze percentage columns
    eda.analyze_percentage_columns()

    # Perform descriptive analysis
    eda.descriptive_analysis()
    # Generate a data quality report
    eda.data_quality_report()