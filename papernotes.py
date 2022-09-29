import markdown
import os
from bs4 import BeautifulSoup
from mdutils.mdutils import MdUtils
from datetime import datetime
import pandas as pd

# DATABASE_FILE_NAME = "database.pkl"
NOTES_FILE_NAME = "README.md"

f = open(NOTES_FILE_NAME,"r")
papernotes = markdown.markdown(f.read(),extensions=['tables'])
papernotes = BeautifulSoup(papernotes,"html.parser")

paperarray = []

# fetch all papers in the list
alltables = papernotes.find_all("tbody")
for table in alltables:
    for row in table.find_all("tr"):
        paperarray.append(row)

# convert html to list of objects (dict)
paperdict = {}
updatedKeys = []
for paper in paperarray:
    date,name,paperlink,tags = paper.find_all("td")
    tags = tags.find_all("a")
    
    ## convert html to strings
    notes = name.find("a").get('href')
    name = name.find("a").get_text()
    paper = paperlink.find("a").get("href")
    taglinks = [tag.get("href") for tag in tags]
    tags = [tag.get_text() for tag in tags]
    date = datetime.strptime(date.get_text(),"%Y-%m")
    
    ## check if local pdf exists
    local = os.path.isfile(notes.replace("notes/","local/").replace(".md",".pdf"))
    
    ## add paper object to dict
    paperdict[name] = {"notes":notes,"paper":paper,"tags": tags,"taglinks": taglinks,"date": date,"local":local}           
    

# create notes section for new papers 
for name,content in paperdict.items():
    ## Check first if a notes file already exists with this name
    if os.path.exists(content["notes"]):
        continue
        
    ## otherwise create new notes file from template
    mdFile = MdUtils(file_name=content["notes"])
    if(content["local"]):
        mdFile.new_header(1, "["+name+"]("+content["paper"]+") ([local]("+content["notes"].replace("notes/","../local/").replace(".md",".pdf")+"))")
    else:
        mdFile.new_header(1, "["+name+"]("+content["paper"]+")")
    tagstrings = ["["+tag+"]" for tag in content["tags"]]
    taglinks = ["(../"+tag+")" for tag in content["taglinks"]]
    mdFile.new_paragraph("Published: "+content["date"].strftime("%Y-%m"))
    mdFile.new_paragraph("Tags: "+", ".join([tagstrings[i]+taglinks[i] for i in range(len(tagstrings))]))
    mdFile.new_paragraph("tl;dr:")
    mdFile.new_header(2, "Summary")
    mdFile.new_header(2, "Technical Details")
    mdFile.new_header(2, "Notes")
    mdFile.new_header(2, "Questions")
    mdFile.new_header(2, "Related")
    mdFile.create_md_file()
    
    
# Sort all papers by publishing date
## Create pandas dataframe from dict (to be able to easily sort by date)
df_papers = pd.DataFrame.from_dict(paperdict,orient="index")
df_papers_sorted = df_papers.sort_values(by="date",ascending=False)
## split up date column to month and year
df_papers_sorted["year"] = df_papers_sorted["date"].dt.year
df_papers_sorted["month"] = df_papers_sorted["date"].dt.month

# Create new README.md with sorted list
mdFile = MdUtils(file_name="README.md")
mdFile.new_header(1,"PaperNotes")
## loop over every year
years = df_papers_sorted["date"].dt.year.unique().tolist()
for year in years:
    mdFile.new_header(2,str(year))
    text_list = ['Date','Name', 'Link', 'Tags']
    ### now loop over every paper in this year
    df_papers_year = df_papers_sorted[df_papers_sorted['year'] == year]
    for index, row in df_papers_year.iterrows():
        #### add new table line for each paper
        text_list.append(row["date"].strftime("%Y-%m"))
        text_list.append("["+index+"]("+ row["notes"] + ")")
        if row["local"]:
           text_list.append("[paper]("+ row["paper"] + ") ([local](" +row["notes"].replace("notes/","../local/").replace(".md",".pdf") +"))") 
        else:
            text_list.append("[paper]("+ row["paper"] + ")")
        tagstring = []
        for i in range(len(row["tags"])):
            tagstring.append("["+row["tags"][i]+"]("+row["taglinks"][i] + ")")
        text_list.append(", ".join(tagstring))
    mdFile.new_table(4, int(len(text_list)/4), text=text_list, text_align='left')
    
mdFile.create_md_file()

# create dict of tags containing all papers per tag
pertag = {}
for name, content in paperdict.items():
    for taglink in content["taglinks"]:
        tag = taglink.replace('tags/','').replace(".md","")
        if tag not in pertag:
            pertag[tag] = []     
        pertag[tag].append(name)

# create page for each tag
for tag,papernames in pertag.items():
    mdFile = MdUtils(file_name="tags/"+tag)
    mdFile.new_header(1, "Tag: "+tag)
    text_list = ['Date','Name', 'Link', 'Tags']
    for paper in papernames:
        text_list.append(paperdict[paper]["date"].strftime("%Y-%m"))
        text_list.append("["+paper+"](../"+ paperdict[paper]["notes"] + ")")
        text_list.append("[paper]("+ paperdict[paper]["paper"] + ")")
        tagstring = []
        for i in range(len(paperdict[paper]["tags"])):
            tagstring.append("["+paperdict[paper]["tags"][i]+"](../"+paperdict[paper]["taglinks"][i] + ")")
        text_list.append(", ".join(tagstring))
        
    
    mdFile.new_table(4, int(len(text_list)/4), text=text_list, text_align='left')
    mdFile.create_md_file()