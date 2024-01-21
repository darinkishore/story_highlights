from bs4 import BeautifulSoup

# Mapping of old CSS classes to new ones
css_class_mapping = {
    "c10": "Main_Male_Character",
    "c26": "Other_Male_3",
    "c17": "Other_Male_2",
    "c18": "Other_Male_1",
    "c19": "Main_Female_Character",
    "c33": "Other_Female_2",
    "c42": "Other_Female_1",
    "c6": "Antagonist_Villain",
    "c12": "Groups_of_People",
    "c7": "Important_Information",
    "c31": "Climax_or_Resolution",
    "c13": "Positive_Time_Reference",
    "c16": "Positive_Descriptions",
    "c32": "Money_and_Wealth",
}

# Load the HTML file
with open("transformations/dat/stories_html/reference.html", "r") as file:
    html = file.read()

# Parse the HTML
soup = BeautifulSoup(html, 'html.parser')

# Find all elements with a class attribute
for tag in soup.find_all(True, {'class': True}):
    # Get the list of classes
    classes = tag['class']
    # Replace old classes with new ones
    new_classes = [css_class_mapping.get(c, c) for c in classes]
    # Update the class attribute
    tag['class'] = new_classes

# Write the updated HTML back to the file
with open("transformations/dat/stories_html/reference.html", "w") as file:
    file.write(str(soup))