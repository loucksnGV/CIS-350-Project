file_in = open("Book Rec Data - book_recommendations.tsv", mode = "r", errors = "ignore")
file_out = open("output_rec.json", "w")

prev_id = ''

file_in.readline() #skip first line

file_out.write("[\n")
while True:
    line = file_in.readline()
    if not line: #reached eof
        break
    
    tokens = line.split('\t')
    
    if tokens[0] == prev_id:
        file_out.write(",\n")
    else:
        if prev_id != '':
            file_out.write("\n    ]\n  },\n")
        prev_id = tokens[0]
        file_out.write("  {{\n    \"book_id\": \"{}\",\n    \"recommended_ids\": [\n".format(tokens[0]))
        
    file_out.write("      \"{}\"".format(''.join(s for s in tokens[1] if ord(s)>31 and ord(s)<126)))
file_out.write("\n    ]\n  }\n]")

file_in.close()
file_out.close()