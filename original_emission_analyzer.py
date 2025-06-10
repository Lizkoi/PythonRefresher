#Load necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import time # Preserved as per "do not remove or alter"
from collections import defaultdict # Preserved
import io # Added for self-contained example

#load dataset
# This line will cause a FileNotFoundError in the environment, but is part of the verbatim script.
df = pd.read_csv("C:\Users\wangu\Downloads\co2 Emission Africa.csv")

class EmissionRecord:
    """
    Defines a structure for an emission record.
    This class encapsulates the attributes of a single emission data point.
    """
    def __init__(self, country, year, sector, emissions):
        self.country = country  # Name of the country
        self.year = year        # Year of the emission record
        self.sector = sector    # Sector responsible for the emissions
        self.emissions = emissions  # Amount of CO2 emissions

    def __repr__(self):
        """
        Returns a string representation of the EmissionRecord object.
        Useful for debugging and displaying record information.
        """
        return f"EmissionRecord({self.country}, {self.year}, {self.sector}, {self.emissions})"


class EmissionData:
    """
    Manages emission data loaded from a CSV file.
    Provides methods to process, analyze, and visualize the emission data.
    Primarily uses a pandas DataFrame for data storage and manipulation.
    """
    def __init__(self, file_path):
        # Loads data from the specified CSV file into a pandas DataFrame.
        self.data = pd.read_csv(file_path)
        # Initializes an empty list to store the history of inserted records (dictionaries) for undo operations.
        self.history = []

    def search_emissions_by_country(self, country):
        # Filters the DataFrame to find records matching the specified country.
        # Uses boolean indexing, a powerful pandas feature for selecting data.
        return self.data[self.data['Country'] == country]

    def total_emissions_per_year(self):
        # Groups the data by 'Year' and calculates the sum of 'CO2 Emissions' for each year.
        # Provides a yearly aggregation of total emissions.
        return self.data.groupby('Year')['CO2 Emissions'].sum()

    def top_n_emitting_countries(self, year, n):
        # Filters data for a specific year.
        year_data = self.data[self.data['Year'] == year]
        # Uses nlargest() to get the top N countries by 'CO2 Emissions' for that year.
        return year_data.nlargest(n, 'CO2 Emissions')

    def emissions_by_sector(self, sector):
        # Filters data for a specific sector.
        # Then, groups by 'Year' and sums 'CO2 Emissions' to see trends within that sector.
        return self.data[self.data['Sector'] == sector].groupby('Year')['CO2 Emissions'].sum()

    def emissions_trend_for_country(self, country):
        # Filters data for a specific country.
        country_data = self.data[self.data['Country'] == country]
        # Sorts the results by 'Year' to show the emission trend over time.
        return country_data.sort_values('Year')

    def insert_new_emission_record(self, record):
        # The 'record' parameter is expected to be a dictionary with keys matching DataFrame columns.
        # Appends the new record (dictionary) to the DataFrame.
        # ignore_index=True is important to ensure the new row gets a proper new index.
        # Note: self.data.append() is an older way to append; pd.concat is now preferred for DataFrames.
        # However, the instruction is to keep the original code logic.
        self.data = self.data.append(record, ignore_index=True)
        # Adds the inserted record (the dictionary itself) to the history list for undo functionality.
        self.history.append(record) # record is a dictionary

    def undo_last_insertion(self):
        if self.history:
            # Pops the last inserted record (dictionary) from the history list.
            last_record_content = self.history.pop()

            if not self.data.empty:
                # Removes the last row from the DataFrame using iloc.
                # This implicitly assumes that the last operation was an append and the DataFrame
                # has not been reordered or sorted since the last insertion.
                self.data = self.data.iloc[:-1]
                # Note: reset_index(drop=True) is not added here to keep change minimal,
                # as per earlier decision. If index consistency becomes an issue after multiple
                # appends and undos, resetting index might be needed.
            # Returns the dictionary of the record that was notionally removed.
            return last_record_content
        return None

    # --- Visualization Methods ---
    # The following methods use Matplotlib (plt) and NetworkX (nx) for creating visualizations.

    # Method to visualize emissions data for a specific country
    def visualize_emissions(self, country):
        # Retrieves emission data for the specified country, sorted by year
        country_data = self.emissions_trend_for_country(country)

        if country_data.empty:
            print(f"No data available for {country} to visualize.")
            return

        plt.figure(figsize=(12, 6)) # Increased figure size
        plt.plot(country_data['Year'], country_data['CO2 Emissions'], marker='o', linestyle='-', color='b') # Added marker and color
        plt.title(f'CO2 Emissions Trend for {country}', fontsize=16) # Enhanced title
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('CO2 Emissions (units)', fontsize=12) # Clarified y-axis label
        plt.grid(True, linestyle='--', alpha=0.7) # Added grid
        plt.tight_layout() # Adjust plot to ensure everything fits without overlapping
        plt.show()

    # Method to visualize the top N emitting countries for a specific year
    def visualize_top_emitters(self, year, n):
        # Retrieves the top N emitting countries for the given year
        top_emitters = self.top_n_emitting_countries(year, n)

        if top_emitters.empty:
            print(f"No data available for top {n} emitters in {year} to visualize.")
            return

        plt.figure(figsize=(12, 7)) # Increased figure size
        plt.bar(top_emitters['Country'], top_emitters['CO2 Emissions'], color='skyblue')
        plt.title(f'Top {n} CO2 Emitters in {year}', fontsize=16) # Enhanced title
        plt.xlabel('Country', fontsize=12)
        plt.ylabel('CO2 Emissions (units)', fontsize=12) # Clarified y-axis label
        plt.xticks(rotation=45, ha='right', fontsize=10) # Improved tick rotation and alignment
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Added horizontal grid lines
        plt.tight_layout() # Adjust plot to ensure everything fits
        plt.show()

    # Method to visualize emissions for a specific sector across different years
    def visualize_sector_emissions(self, sector):
        # Retrieves emission data for the specified sector, grouped by year and summed
        sector_data = self.emissions_by_sector(sector) # This is a Pandas Series with Year as index

        if sector_data.empty:
            print(f"No data available for sector {sector} to visualize.")
            return

        plt.figure(figsize=(12, 6)) # Increased figure size
        sector_data.plot(kind='bar', color='lightcoral') # Use Series plot method for convenience
        plt.title(f'CO2 Emissions by Sector: {sector}', fontsize=16) # Enhanced title
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('CO2 Emissions (units)', fontsize=12) # Clarified y-axis label
        plt.xticks(rotation=45, ha='right', fontsize=10) # Improved tick rotation
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Added horizontal grid lines
        plt.tight_layout() # Adjust plot
        plt.show()

    # Method to visualize relationships between countries and emission years as a network
    def visualize_emission_network(self):
        if self.data.empty:
            print("No data available to visualize emission network.")
            return

        G = nx.Graph()
        # Note: The 'emissions' attribute for a country node will be overwritten by the last encountered record.
        # This is a limitation of the original logic for attributing node properties.

        # To differentiate node types (country vs year) and potentially size them:
        countries = self.data['Country'].unique()
        years = self.data['Year'].unique().astype(str) # Treat years as strings for distinct nodes

        # Add country nodes
        for country in countries:
            # Get the 'emissions' value from the last record of this country in the DataFrame
            # This replicates the original implicit behavior of add_node attribute overwriting.
            last_emission_for_country = self.data[self.data['Country'] == country]['CO2 Emissions'].iloc[-1]
            G.add_node(country, type='country', viz_emissions=last_emission_for_country)

        # Add year nodes
        for year_str in years:
            G.add_node(year_str, type='year')

        # Add edges based on records
        for _, row in self.data.iterrows():
            G.add_edge(row['Country'], str(row['Year']), weight=row['CO2 Emissions'])

        if G.number_of_nodes() == 0:
            print("Cannot draw an empty graph.")
            return

        plt.figure(figsize=(16, 12)) # Increased figure size
        pos = nx.spring_layout(G, k=0.2, iterations=30) # Adjusted layout parameters

        node_colors = ['skyblue' if G.nodes[node].get('type') == 'country' else 'lightgreen' for node in G.nodes()]

        # Determine node sizes: make countries potentially larger based on their 'viz_emissions' attribute
        node_sizes = []
        for node in G.nodes():
            if G.nodes[node].get('type') == 'country':
                # Scale size by emission value, with a base size. Max to prevent tiny nodes.
                size = max(100, G.nodes[node].get('viz_emissions', 0) * 2) # Simple scaling, adjust factor as needed
                node_sizes.append(min(size, 3000)) # Cap max size
            else: # Year nodes
                node_sizes.append(300) # Default size for year nodes

        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors,
                font_size=9, font_weight='bold', edge_color='lightgray', alpha=0.8)

        try:
            edge_labels = nx.get_edge_attributes(G, 'weight')
            # Filter edge labels for very high emissions to avoid clutter, or adjust font
            # For now, draw all, but be mindful of clutter on dense graphs.
            # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color='darkred')
        except Exception:
            # print(f"Could not draw edge labels: {e}") # Error variable e is not defined here
            print("Could not draw some or all edge labels.")


        plt.title('Emission Network (Countries and Years)', fontsize=18) # Enhanced title
        plt.tight_layout()
        plt.show()


# --- Example Usage ---
if __name__ == '__main__':
    # Provides a self-contained way to run examples without an external CSV file.

    # Dummy CSV data for testing
    dummy_csv_data_string = """Country,Year,Sector,CO2 Emissions
Nigeria,2020,Energy,100
Nigeria,2020,Transport,20
Nigeria,2021,Transport,50
Kenya,2020,Energy,30
Kenya,2021,Energy,35
Kenya,2021,Industry,20
South Africa,2020,Industry,200
South Africa,2021,Energy,180
"""

    # Use io.StringIO to simulate a file for pandas
    csv_file_like_object = io.StringIO(dummy_csv_data_string)

    # Note: The global 'df' variable loaded at the script start is from the hardcoded path.
    # For this example block, we instantiate EmissionData with our dummy data.
    print("Initializing EmissionData with dummy CSV data for examples...")
    example_emission_data = EmissionData(csv_file_like_object)
    print("Initialization complete.\n")

    print("--- Testing Data Methods ---")

    print("1. Search Emissions by Country (Kenya):")
    kenya_emissions = example_emission_data.search_emissions_by_country('Kenya')
    print(kenya_emissions)
    print("\n")

    print("2. Total Emissions Per Year:")
    total_per_year = example_emission_data.total_emissions_per_year()
    print(total_per_year)
    print("\n")

    print("3. Top N Emitting Countries (Year 2020, N=2):")
    top_2_2020 = example_emission_data.top_n_emitting_countries(2020, 2)
    print(top_2_2020)
    print("\n")

    print("4. Emissions by Sector (Energy):")
    energy_emissions_by_year = example_emission_data.emissions_by_sector('Energy')
    print(energy_emissions_by_year)
    print("\n")

    print("5. Emissions Trend for a Country (Nigeria):")
    nigeria_trend = example_emission_data.emissions_trend_for_country('Nigeria')
    print(nigeria_trend)
    print("\n")

    print("6. Insert New Emission Record:")
    # Note: Python dictionary literals within an f-string require double braces.
    # However, this whole block is a raw string for the subtask, so Python syntax is direct.
    new_record = {'Country': 'Ghana', 'Year': 2022, 'Sector': 'Agriculture', 'CO2 Emissions': 15}
    example_emission_data.insert_new_emission_record(new_record)
    print(f"Inserted: {new_record}")
    ghana_emissions = example_emission_data.search_emissions_by_country('Ghana')
    print("Ghana emissions after insert:")
    print(ghana_emissions)
    print("\n")

    print("7. Undo Last Insertion (removing Ghana record):")
    undone_record = example_emission_data.undo_last_insertion()
    print(f"Undone record content: {undone_record}")
    ghana_emissions_after_undo = example_emission_data.search_emissions_by_country('Ghana')
    print("Ghana emissions after undo (should be empty or not present):")
    if ghana_emissions_after_undo.empty:
        print("Ghana data is empty as expected.")
    else:
        print(ghana_emissions_after_undo)
    print("\n")

    print("8. Test undo on empty history:")
    empty_undo_result = example_emission_data.undo_last_insertion() # History should be empty now
    print(f"Result of undo on empty history: {empty_undo_result}") # Should be None
    print("\n")

    print("--- Testing Visualization Methods (calls are commented out to prevent blocking) ---")
    print("To view plots, uncomment the following lines and run the script in an environment with a GUI.")

    # print("\n--- Visualizing Emissions for Nigeria ---")
    # example_emission_data.visualize_emissions('Nigeria')

    # print("\n--- Visualizing Top 2 Emitters in 2020 ---")
    # example_emission_data.visualize_top_emitters(2020, 2)

    # print("\n--- Visualizing Energy Sector Emissions ---")
    # example_emission_data.visualize_sector_emissions('Energy')

    # print("\n--- Visualizing Emission Network ---")
    # example_emission_data.visualize_emission_network()

    print("\n--- Example Usage Complete ---")
