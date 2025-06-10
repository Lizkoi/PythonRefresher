import pandas as pd
from collections import defaultdict
import heapq
import bisect
import matplotlib.pyplot as plt # Added import
import networkx as nx # Added import


class EmissionRecord:
    def __init__(self, country, year, sector, emissions):
        self.country = country
        self.year = year
        self.sector = sector
        self.emissions = emissions

    def __repr__(self):
        return f"EmissionRecord(country='{self.country}', year={self.year}, sector='{self.sector}', emissions={self.emissions})"

class EmissionData:
    # Time Complexity: O(M + Sum(Kc log Kc)) where M is the total number of records,
    #                  Kc is the number of records for country c.
    #                  Roughly O(M log K_max) where K_max is max records for any country.
    #                  This accounts for reading M records and then sorting records for each country.
    # Space Complexity: O(M) to store all M records in various data structures.
    def __init__(self, file_path):
        self.records_by_country = defaultdict(list)
        self.records_by_year = defaultdict(list)
        self.records_by_sector = defaultdict(list)
        self.all_records = []
        self.history = [] # For undo functionality, not populated during initial load

        # Load data from CSV
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            record = EmissionRecord(
                country=row['Country'],
                year=row['Year'],
                sector=row['Sector'],
                emissions=row['CO2 Emissions']
            )
            self.all_records.append(record)
            self.records_by_country[record.country].append(record)
            self.records_by_year[record.year].append(record)
            self.records_by_sector[record.sector].append(record)

        for country_records in self.records_by_country.values():
            country_records.sort(key=lambda r: r.year)

    # Time Complexity: O(k) where k is the number of records for the specific country.
    #   - Creating EmissionRecord: O(1).
    #   - Appending to self.all_records, self.records_by_year, self.records_by_sector: Amortized O(1).
    #   - Creating [r.year for r in country_records] is O(k).
    #   - bisect_left is O(log k) on the years list, but overall O(k) due to list creation.
    #   - country_records.insert(idx, record) is O(k).
    #   - Appending to self.history: O(1).
    # Space Complexity: O(k) temporarily for the list of years, O(1) otherwise for the operation itself.
    def insert_new_emission_record(self, record_dict):
        # Assuming record_dict has keys: 'Country', 'Year', 'Sector', 'CO2 Emissions'
        record = EmissionRecord(
            country=record_dict['Country'],
            year=record_dict['Year'],
            sector=record_dict['Sector'],
            emissions=record_dict['CO2 Emissions']
        )
        self.all_records.append(record)
        country_records = self.records_by_country[record.country]
        years_in_country_records = [r.year for r in country_records]
        idx = bisect.bisect_left(years_in_country_records, record.year)
        country_records.insert(idx, record)
        self.records_by_year[record.year].append(record)
        self.records_by_sector[record.sector].append(record)
        self.history.append(record) # Push to history for undo
        return record # Optionally return the created record

    # Time Complexity: O(N) where N is the total number of records in self.all_records.
    #   - Pop from self.history: O(1).
    #   - list.remove() on self.all_records: O(N) in the worst case.
    #   - list.remove() on other lists (country, year, sector specific): O(k), O(N_y), O(N_s) respectively.
    # Space Complexity: O(1).
    def undo_last_insertion(self):
        if not self.history:
            return None # Or raise an error: raise IndexError("No insertions to undo")

        last_record = self.history.pop()

        try:
            self.all_records.remove(last_record)
            self.records_by_country[last_record.country].remove(last_record)
            self.records_by_year[last_record.year].remove(last_record)
            self.records_by_sector[last_record.sector].remove(last_record)
        except ValueError:
            # This should ideally not happen if history and records are consistent.
            pass
        return last_record

    # Time Complexity: O(1) on average (dictionary access).
    # Space Complexity: O(k) where k is the number of records for the country.
    def search_emissions_by_country(self, country_name):
        return self.records_by_country[country_name]

    # Time Complexity: O(N) where N is the total number of emission records.
    # Space Complexity: O(Y) where Y is the number of unique years.
    def total_emissions_per_year(self):
        yearly_totals = defaultdict(float)
        for record in self.all_records:
            yearly_totals[record.year] += record.emissions
        return yearly_totals

    # Time Complexity: O(N_y + C_y log n)
    #   - N_y: number of records for the given year.
    #   - C_y: number of unique countries in that year.
    #   - Accessing records for the year: O(1) avg. for dict lookup.
    #   - Aggregating by country: O(N_y)
    #   - Heap operations: C_y iterations, each log n. So, O(C_y log n).
    # Space Complexity: O(C_y + n)
    #   - O(C_y) for storing emission sums per country for the year.
    #   - O(n) for the min-heap.
    def top_n_emitting_countries(self, year, n):
        records_for_year = self.records_by_year.get(year, [])
        if not records_for_year: return []

        emissions_by_country = defaultdict(float)
        for record in records_for_year:
            emissions_by_country[record.country] += record.emissions

        if not emissions_by_country: return []
        if n <= 0: return [] # Or raise ValueError for invalid n

        min_heap = []
        for country, total_emissions in emissions_by_country.items():
            if len(min_heap) < n:
                heapq.heappush(min_heap, (total_emissions, country))
            elif total_emissions > min_heap[0][0]:
                heapq.heapreplace(min_heap, (total_emissions, country))
        top_countries_data = sorted(min_heap, key=lambda x: x[0], reverse=True)
        return [{'Country': country, 'CO2 Emissions': emissions} for emissions, country in top_countries_data]

    # Time Complexity: O(N_s) where N_s is the number of records for the given sector.
    # Space Complexity: O(Y_s) where Y_s is the number of unique years within that sector.
    def emissions_by_sector(self, sector_name):
        emissions_by_year_for_sector = defaultdict(float)
        records_for_sector = self.records_by_sector.get(sector_name, [])
        for record in records_for_sector:
            emissions_by_year_for_sector[record.year] += record.emissions
        return emissions_by_year_for_sector

    # Time Complexity: O(1) on average (dictionary access). List is already sorted by year.
    # Space Complexity: O(k) where k is the number of records for the country.
    def emissions_trend_for_country(self, country_name):
        return self.records_by_country[country_name]

    # Time Complexity: O(k) for data retrieval (k records for the country) + plotting time.
    # Space Complexity: O(k) for data for plotting.
    def visualize_emissions(self, country_name):
        country_data = self.emissions_trend_for_country(country_name) # List of EmissionRecord objects
        if not country_data:
            print(f"No data found for country: {country_name}")
            return

        years = [record.year for record in country_data]
        emissions = [record.emissions for record in country_data]

        plt.figure(figsize=(10, 6))
        plt.plot(years, emissions, marker='o', linestyle='-')
        plt.title(f'CO2 Emissions Trend for {country_name}')
        plt.xlabel('Year')
        plt.ylabel('CO2 Emissions (units)') # Add units if known
        plt.grid(True)
        plt.show()

    # Time Complexity: O(N_y + C_y log n) for data retrieval + plotting time.
    # Space Complexity: O(C_y + n) for data for plotting.
    def visualize_top_emitters(self, year, n):
        top_emitters_data = self.top_n_emitting_countries(year, n) # List of {'Country': name, 'CO2 Emissions': val}
        if not top_emitters_data:
            print(f"No data found for top {n} emitters in {year}")
            return

        countries = [data['Country'] for data in top_emitters_data]
        emissions = [data['CO2 Emissions'] for data in top_emitters_data]

        plt.figure(figsize=(12, 7))
        plt.bar(countries, emissions, color='skyblue')
        plt.title(f'Top {n} CO2 Emitters in {year}')
        plt.xlabel('Country')
        plt.ylabel('CO2 Emissions (units)') # Add units if known
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.grid(axis='y')
        plt.show()

    # Time Complexity: O(N_s) for data retrieval + plotting time.
    # Space Complexity: O(Y_s) for data for plotting.
    def visualize_sector_emissions(self, sector_name):
        sector_data = self.emissions_by_sector(sector_name) # {year: total_emissions, ...}
        if not sector_data:
            print(f"No emissions data found for sector: {sector_name}")
            return

        sorted_years = sorted(sector_data.keys())
        emissions = [sector_data[year] for year in sorted_years]

        plt.figure(figsize=(10, 6))
        plt.bar(sorted_years, emissions, color='lightgreen')
        plt.title(f'CO2 Emissions by Sector: {sector_name}')
        plt.xlabel('Year')
        plt.ylabel('CO2 Emissions (units)') # Add units if known
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(axis='y')
        plt.show()

    # Time Complexity: O(N_all + V + E) for graph creation (N_all records, V nodes, E edges) + NetworkX layout/drawing.
    # Space Complexity: O(V + E) for graph storage + plotting.
    def visualize_emission_network(self):
        if not self.all_records:
            print("No data available to visualize emission network.")
            return

        G = nx.Graph()

        country_total_emissions = defaultdict(float)
        for record in self.all_records:
            country_total_emissions[record.country] += record.emissions

        for country, total_emissions in country_total_emissions.items():
            G.add_node(country, total_emissions=total_emissions)

        for record in self.all_records:
            if not G.has_node(str(record.year)):
                 G.add_node(str(record.year))

            G.add_edge(record.country, str(record.year), weight=record.emissions)

        if not G.nodes():
            print("Graph has no nodes. Cannot visualize network.")
            return

        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(G, k=0.15, iterations=20)

        node_sizes = []
        node_colors = []
        for node in G.nodes():
            if node in country_total_emissions:
                node_sizes.append(country_total_emissions[node] * 0.1 if country_total_emissions[node] * 0.1 > 100 else 100)
                node_colors.append('skyblue')
            else:
                node_sizes.append(500)
                node_colors.append('lightgreen')

        nx.draw(G, pos, with_labels=True, node_size=node_sizes, node_color=node_colors, font_size=8, font_weight='bold', edge_color='gray', alpha=0.7)

        try:
            edge_labels = nx.get_edge_attributes(G, 'weight')
            # Filter edge_labels to include only edges present in pos to avoid warnings/errors if graph changed
            valid_edge_labels = {edge: label for edge, label in edge_labels.items() if edge[0] in pos and edge[1] in pos}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=valid_edge_labels, font_size=7)
        except Exception as e:
            print(f"Could not draw edge labels: {e}")

        plt.title('Emission Network (Countries and Years connected by Emissions)', fontsize=15)
        plt.show()
