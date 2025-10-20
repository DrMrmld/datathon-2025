"""
filename: make_docs.py
purpose: generate a 'documentation' that describes the structure
            of the dataset from a JSON file.
"""


import json

output_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D002 Structure</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h1>Structure of the D002 dataset</h1>
    sections
</body>
</html>
"""

field_begin = """
    <div class="ml-2">
        <h3 class="font-mono fsize-15">field_name</h3>
        <p class="mb-05 ml-3">field_description</p>
        <p class="mt-05 ml-3"><b>Original Fields:</b> original_fields</p>
        <p class="mt-05 mb-05 ml-3"><b>Type:</b> <span class="font-mono fsize-12">field_type</span></p>
"""

field_end = """
    </div>
"""

question_template = """
        <p class="mt-05 mb-05 ml-3"><b>Question:</b> question</p>
        <p class="mt-05 mb-05 ml-3"><b>Answer options:</b></p>
        <ul class="mt-0 ml-3">
            answer_options
        </ul>
"""

answer_option_template = """
            <li><b class="font-mono fsize-12">option_name</b> - option_description.</li>
"""

section_begin = """
    <section>
        <h2>section_name</h2>
"""

section_end = """
    </section>
"""


path = "./data.json"
sections: list[dict] = []
with open(path) as f:
    sections = json.load(f)


current_sections = ""
for section in sections:
    current_section = section_begin.replace("section_name", section["section_name"])
    current_fields = ""
    
    fields = section["fields"]
    for field in fields:
        current_field = field_begin.replace("field_name", field["field_name"])
        current_field = current_field.replace("field_description", field["field_description"])
        current_field = current_field.replace("original_fields", field["original_fields"])
        current_field = current_field.replace("field_type", field["type"])

        if "question" not in field.keys():
            current_fields += current_field + field_end
            continue

        current_question = question_template.replace("question", field["question"])
        current_options = ""

        answer_options = field["answer_options"]
        for option in answer_options:
            current_option = answer_option_template.replace("option_name", option[0])
            current_option = current_option.replace("option_description", option[1])
            current_options += current_option

        current_field += current_question.replace("answer_options", current_options)
        current_fields += current_field + field_end

    current_section += current_fields
    current_sections += current_section + section_end


outputHTML = output_template.replace("sections", current_sections)
output_path = "./index.html"
with open(output_path, "w") as f:
    f.write(outputHTML)
