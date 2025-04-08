import csv
import os
from supabase import create_client
from dotenv import load_dotenv
import time

# Load environment variables from .env file
load_dotenv()

# Get Supabase URL and key from environment variables
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_API_KEY")

# Initialize Supabase client
supabase = create_client(supabase_url, supabase_key)

def test_connection():
    try:
        # Simple query to test connection - USE LOWERCASE table name
        result = supabase.table("destinations").select("*").limit(1).execute()
        print("Connection successful!")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False

def import_destinations_csv():
    try:
        # Path to the CSV file
        csv_file_path = "DESTINATIONS.csv"
        
        # Read CSV file
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            # Count for statistics
            total_rows = 0
            inserted_rows = 0
            error_rows = 0
            
            # Process each row
            for row in csv_reader:
                total_rows += 1
                
                try:
                    # Prepare data for insertion
                    destination_data = {
                        "name": row.get("Name", ""),
                        "state": row.get("State", ""),
                        "type": row.get("Type", None),
                        "popularity": float(row.get("Popularity", 0)) if row.get("Popularity") else None,
                        "best_time_to_visit": row.get("BestTimeToVisit", None)
                    }
                    
                    # Insert data into the destinations table - USE LOWERCASE
                    print(f"Attempting to insert: {destination_data}")
                    result = supabase.table("destinations").insert(destination_data).execute()
                    
                    inserted_rows += 1
                    print(f"Inserted destination: {row.get('name')}")
                except Exception as e:
                    error_rows += 1
                    print(f"Error type: {type(e).__name__}")
                    print(f"Error inserting row {total_rows}: {str(e)}")
                    print(f"Row data: {row}")
                    # Try to extract more error details
                    if hasattr(e, 'response'):
                        print(f"Response status: {getattr(e.response, 'status_code', 'Unknown')}")
                        print(f"Response content: {getattr(e.response, 'content', 'No content')}")
                
                # Small delay to prevent rate limiting
                time.sleep(0.1)
            
            # Print statistics
            print("\nImport Summary:")
            print(f"Total rows processed: {total_rows}")
            print(f"Successfully inserted: {inserted_rows}")
            print(f"Errors: {error_rows}")
            
    except Exception as e:
        print(f"Error reading CSV file: {str(e)}")

if __name__ == "__main__":
    # Check if required environment variables are set
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_API_KEY in your .env file.")
        exit(1)
    
    # Test connection first
    if not test_connection():
        print("Aborting import due to connection failure")
        exit(1)
    
    # Run the import function
    import_destinations_csv()