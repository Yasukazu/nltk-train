import requests

# URL of the webpage
def save_html(
url: str
):
    """
    This function fetches the HTML content of a webpage and prints it.
    """
    # Send a GET request to the URL
    response = requests.get("https://" + url)

    # Get the HTML content of the webpage
    html_content = response.text

    # Print or process the HTML content
    print(html_content)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python save_a_webpage.py [URL]")
        sys.exit(1)
    url = sys.argv[1]
    # Call the function to save the HTML content
    save_html(url)