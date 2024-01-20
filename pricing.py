
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
            model_name = cells[0].find('span')
            
            if model_name:
            
                model_name = clean_txt(model_name.text)
                prices[model_name] = {}
                
                # Other cells
                for i, (cell, column) in enumerate(zip(cells[1:], columns[1:])):
                    
                    # Extract content from cell
                    spans = cell.find_all("span")
                    if spans:
                        if len(spans) > 1:
                            text = "".join([clean_txt(span.text) for span in spans])
                        else:
                            text = clean_txt(spans[0].text)
                        
                        prices[model_name][column] = text
        
    return prices


if __name__ == "__main__":
    
    prices = refresh_openai_price()
    from pprint import pprint
    pprint(prices)