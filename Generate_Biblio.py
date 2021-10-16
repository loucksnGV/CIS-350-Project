file_in = open("Book Rec Data - book_biblio_data.tsv", mode = "r", errors = "ignore")
file_out = open("output_biblio.json", "w")

file_in.readline() #skip first line

file_out.write("[\n")
while True:
    line = file_in.readline()
    if not line: #reached eof
        break
    
    tokens = line.split('\t')
    for i, token in enumerate(tokens):
        tokens[i] = ''.join(s for s in tokens[i].replace("\\", "\\\\").replace("\"", "\\\"") if ord(s)>31 and ord(s)<126) #tokenize and sanitize
    
    file_out.write("  {{\n    \"_id\": \"{}\",\n    \"title\": \"{}\",\n    \"synopsis\": \"{}\",\n    \"image_url\": \"{}\",\n    \"author\": \"{}\"\n  }},\n"
          .format(tokens[0], tokens[1], tokens[2], tokens[3], tokens[4])) #format and print
file_out.write("]")

file_in.close()
file_out.close()