import os

lines = """monokai
manni
rrt
perldoc
borland
colorful
default
murphy
vs
trac
tango
fruity
autumn
bw
emacs
vim
pastie
friendly
native
solarizeddark
solarizedlight""".split("\n")

lines= ['autumn']

template = """pygmentize -O "style=%s,fontface=Courier Bold,font_size=36,line_numbers=False" -o andy_%s.png andy.clj"""
template = """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o app_%s.png app.d"""
template = """pygmentize -O "style=%s,font_size=40,line_numbers=False" -o snippet2_%s.png snippet2.d"""

for template in [ """pygmentize -O "style=%s,font_size=36,line_numbers=False" -o andy_%s.png andy.clj""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o app_%s.png app.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o csv_%s.png csv.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o incrementAndGet_%s.png incrementAndGet.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o manyToManyCommon_%s.png manyToManyCommon.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o manyToManyReader_%s.png manyToManyReader.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o manyToManyWriter_%s.png manyToManyWriter.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o multipleHeads_%s.png multipleHeads.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o padded_%s.png padded.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o events_%s.png events.scala""",
                  """pygmentize -O "style=%s,font_size=36,line_numbers=False" -o event_decl_%s.png event_decl.d""",
                  """pygmentize -O "style=%s,font_size=25,line_numbers=False" -o BidAskChange_%s.png /home/andy/repos/lambdaExperiment/src/main/java/BidAskChange.java""",
                  """pygmentize -O "style=%s,font_size=40,line_numbers=False" -o marketData_%s.png marketData.d""",
                  
                  """pygmentize -O "style=%s,font_size=30,line_numbers=False" -o dumpInfo_%s.png dumpInfo.d""",
                  """pygmentize -O "style=%s,font_size=20,line_numbers=False" -o padding_%s.png padding.java""",
                  """pygmentize -O "style=%s,font_size=30,line_numbers=False" -o cost_%s.png cost.py""",
                  """pygmentize -O "style=%s,font_size=40,line_numbers=False" -o snippet2_%s.png snippet2.d""" ]:

    for x in lines:
        cmd = template % (x,x)
        print cmd
        os.system(cmd)










