from bs4 import BeautifulSoup
import requests


def refresh_openai_price() -> dict:
    """
    Returns a dict of OpenAI's pricing, where every key is a model name.
    """
    
    def clean_txt(txt):
        return txt.encode("ISO-8859-1").decode("UTF-8").replace("\xa0", "").replace("Â·", "")

    response = requests.get("https://openai.com/pricing")

    soup = BeautifulSoup(response.text, 'html.parser')

    container_div = soup.find("div", {"id": "content"})
    models_div = container_div.find_all("div", {"class": "ui-block ui-block--pricing-table"})

    prices = {}

    for div in models_div:
        
        father_model_name = div.get("id")
        prices[father_model_name] = {}
        
        # find the table in div
        table = div.find("table")
        # find all tr in table
        trs = table.find_all("tr")
        
        # Header row
        columns = [td.text for td in trs[0].find_all("td")]
        
        # Content rows
        for row in trs[1:]:
            
            # Cells
            cells = [td for td in row.find_all("td")]
            assert len(cells) == len(columns)
            
            # First cell
            submodel_name = cells[0].find('span')
            
            if submodel_name:
            
                submodel_name = clean_txt(submodel_name.text)
                prices[father_model_name][submodel_name] = {}
                
                # Other cells
                for i, (cell, column) in enumerate(zip(cells[1:], columns[1:])):
                    
                    # Extract content from cell
                    spans = cell.find_all("span")
                    if spans:
                        if len(spans) > 1:
                            text = "".join([clean_txt(span.text) for span in spans])
                            
                        else:
                            text = clean_txt(spans[0].text)
                        
                        prices[father_model_name][submodel_name][column] = text
        
    return prices


def parse_price(prices:dict):
    
    for k,v in prices.items():
        
        if "gpt" in k.lower():
        
            for k2,v2 in prices[k].items():
                
                k2 = k2.lower()
                if "input" in k2:
                    price = int(v2.split("/")[0].replace("$", ""))
                    prices[k][k2] = price
                    # remove key from dict

    

if __name__ == "__main__":
    
    prices = refresh_openai_price()
    import json
    with open("apikeylogger/prices.json", "w") as f:
        json.dump(prices, f)
    from pprint import pprint
    pprint(prices)