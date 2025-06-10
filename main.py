import pandas as pd
from emission_data import EmissionData # Assuming emission_data.py is in the same directory
import io

# Prepare dummy CSV data for testing
dummy_csv_data = """Country,Year,Sector,CO2 Emissions
Nigeria,2020,Energy,100
Nigeria,2020,Transport,20
Nigeria,2021,Transport,50
Kenya,2020,Energy,30
Kenya,2021,Energy,35
Kenya,2021,Industry,20
South Africa,2020,Industry,200
South Africa,2021,Energy,180
"""

# Use io.StringIO to simulate a file for pd.read_csv
csv_file = io.StringIO(dummy_csv_data)

def run_tests():
    print("Initializing EmissionData with dummy CSV...")
    # The original file path was: "C:\Users\wangu\Downloads\co2 Emission Africa.csv"
    emission_data_processor = EmissionData(csv_file) # Use the dummy CSV for testing
    print("Initialization complete.\n")

    print("1. Search Emissions by Country (Kenya):")
    kenya_emissions = emission_data_processor.search_emissions_by_country('Kenya')
    for record in kenya_emissions:
        print("  ", record) # EmissionRecord's __repr__ will be used
    print("\n")

    print("2. Total Emissions Per Year:")
    total_per_year = emission_data_processor.total_emissions_per_year()
    if total_per_year: # Check if dictionary is not empty
        for year, total in total_per_year.items():
            print("  Year:", year, ", Total Emissions:", total)
    else:
        print("  No yearly totals found.")
    print("\n")

    print("3. Top N Emitting Countries (Year 2020, N=2):")
    top_2_2020 = emission_data_processor.top_n_emitting_countries(2020, 2)
    if top_2_2020:
        for entry in top_2_2020: # entry is {'Country': name, 'CO2 Emissions': val}
            print("  Country:", entry['Country'], ", Emissions:", entry['CO2 Emissions'])
    else:
        print("  No top emitters found for 2020, N=2.")
    print("\n")

    print("3b. Top N Emitting Countries (Year 2021, N=1):")
    top_1_2021 = emission_data_processor.top_n_emitting_countries(2021, 1)
    if top_1_2021:
        for entry in top_1_2021:
            print("  Country:", entry['Country'], ", Emissions:", entry['CO2 Emissions'])
    else:
        print("  No top emitters found for 2021, N=1.")
    print("\n")

    print("4. Emissions by Sector (Energy):")
    energy_emissions_by_year = emission_data_processor.emissions_by_sector('Energy')
    if energy_emissions_by_year:
        for year, total in energy_emissions_by_year.items():
            print("  Year:", year, ", Emissions in Energy:", total)
    else:
        print("  No emissions found for Energy sector.")
    print("\n")

    print("5. Emissions Trend for a Country (Nigeria):")
    nigeria_trend = emission_data_processor.emissions_trend_for_country('Nigeria')
    if nigeria_trend:
        for record in nigeria_trend: # Records are sorted by year
            print("  ", record)
    else:
        print("  No trend data found for Nigeria.")
    print("\n")

    print("6. Insert New Emission Record:")
    new_record_data = {'Country': 'Kenya', 'Year': 2022, 'Sector': 'Transport', 'CO2 Emissions': 25}
    inserted_record = emission_data_processor.insert_new_emission_record(new_record_data)
    print("  Inserted:", inserted_record)
    kenya_emissions_after_insert = emission_data_processor.search_emissions_by_country('Kenya')
    print("  Kenya emissions after insert:")
    for record in kenya_emissions_after_insert:
        print("    ", record)
    print("\n")

    print("7. Undo Last Insertion:")
    undone_record = emission_data_processor.undo_last_insertion()
    print("  Undone:", undone_record)
    kenya_emissions_after_undo = emission_data_processor.search_emissions_by_country('Kenya')
    print("  Kenya emissions after undo:")
    for record in kenya_emissions_after_undo:
        print("    ", record)
    print("\n")

    print("7b. Undo behavior with multiple inserts/undos:")
    ghana_record_1 = {'Country': 'Ghana', 'Year': 2023, 'Sector': 'Waste', 'CO2 Emissions': 5}
    ghana_record_2 = {'Country': 'Ghana', 'Year': 2024, 'Sector': 'Waste', 'CO2 Emissions': 8}

    print("  Inserting Ghana record 2023...")
    emission_data_processor.insert_new_emission_record(ghana_record_1)
    print("  Inserted: Ghana 2023")

    print("  Inserting Ghana record 2024...")
    emission_data_processor.insert_new_emission_record(ghana_record_2)
    print("  Inserted: Ghana 2024")

    undone_ghana_2 = emission_data_processor.undo_last_insertion()
    print(f"  Undoing Ghana 2024 record: {undone_ghana_2}")
    undone_ghana_1 = emission_data_processor.undo_last_insertion()
    print(f"  Undoing Ghana 2023 record: {undone_ghana_1}")
    attempt_empty_undo = emission_data_processor.undo_last_insertion()
    print(f"  Attempting to undo with empty history: {attempt_empty_undo}")
    print("\n")

    print("--- Visualization Method Calls (These would generate plots in a local environment) ---")
    print("Call: visualize_emissions('Nigeria')")
    # emission_data_processor.visualize_emissions('Nigeria')
    print("Call: visualize_top_emitters(2020, 2)")
    # emission_data_processor.visualize_top_emitters(2020, 2)
    print("Call: visualize_sector_emissions('Energy')")
    # emission_data_processor.visualize_sector_emissions('Energy')
    print("Call: visualize_emission_network()")
    # emission_data_processor.visualize_emission_network()
    print("--- End of Visualization Method Calls ---")

if __name__ == '__main__':
    run_tests()
