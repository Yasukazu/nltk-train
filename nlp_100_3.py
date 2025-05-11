from nlp_100_2 import DATA_DIR
import pandas as pd
import json

def extract_json_lines(key = "イギリス",
                       jawiki_country_json = DATA_DIR / 'jawiki-country.json'):
    jawiki_country_df = pd.read_json(jawiki_country_json, lines=True)
    matching_row = jawiki_country_df.loc[jawiki_country_df['title'] == key]
    content = matching_row['text'].values[0] if not matching_row.empty else None
    if content:
        content = content.strip("'").replace("\\'", "'").replace("\\n", "\n")
        return content #print(f"Content for '{key}':\n{content}")
    #else: print(f"No content found for '{key}'")  
# Display the matching row
if __name__ == "__main__":
    key = "イギリス"
    jawiki_country_json = DATA_DIR / 'jawiki-country.json'
    matching_row = extract_json_lines(key, jawiki_country_json)
    if matching_row:
        print(f"Content for '{key}':\n{matching_row}")
    else:
        print(f"No content found for '{key}'")
