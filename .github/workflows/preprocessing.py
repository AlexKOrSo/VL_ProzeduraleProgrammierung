import glob, os
import shutil
import re

blackList = ["{{", "******", "@Rextester", "@Tau", "@LIA.eval"]

for file in glob.glob("*.md"):
    if file != "README.md":
        shutil.copy2(file, file+"x")

for file in glob.glob("*.mdx"):
    content = open(file, 'r').readlines()
    filtered = []
    for line in content:
        if any(entry in line for entry in blackList):
            continue
        result = re.search( r'```\S+', line)
        if result:
            line = result.group(0) + "\n"
        filtered.append(line)

    with open(file, "w") as outfile:
        if file.endswith("00_Einfuehrung.mdx"):  # insert metadata for pandoc in first md file
            title = "**Procedurale Programmierung - TU Freiberg**"
            outfile.write(f"---\ntitle: |\n  {title}\n  https://github.com/SebastianZug/VL_Softwareentwicklung/\nauthor:\n")
            with open(".github/workflows/authors.txt", "r") as authors:  # read in authors and write them into the yaml code
                for line in authors:
                    name = line.strip()
                    outfile.write(f"  - {name}\n")

            outfile.write("papersize:\n  - a4\ngeometry:\n  - margin=2cm\n")
            outfile.write("header-includes:\n  - \\usepackage{titling}\n  - \\pretitle{\\begin{center}\n    \\includegraphics[width=2cm]{images/Logo_TU_Freiberg.png}\\LARGE\\\\}\n  - \\posttitle{\\end{center}}\n---\n")
        outfile.write("".join(filtered))
