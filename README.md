# The "Companies Keep Rejecting Me" Support Group! (iCIMS Halloween Hackathon 2018)

[www.companieskeeprejecting.me](www.companieskeeprejecting.me)

(at the moment the actual website crashes, probably due to the size of the GET call, you'll have to run it locally with `python flash_app.py`)

A facetious proof-of-concept application that tries to help job seekers with rejected offers figure out what went wrong and what areas they can improve on.

Lists most common skills that other applicants to this position have, sorted both by quantity alone and weighted according to the skill levels of the applicants with these skills.

This was my first experience using Flask and manipulating with JSON files using Python, as such I was not able to implement most of what I had invisioned the app to eb capable of.

Features To Come:

- [currently bugged] lists skills and skill levels of accepted people for those jobs you applied to (to figure out what skills you should learn or look to learn)
- list of jobs that other people with similar skills as you are applying to (sorted by most relevant to your field of expertise)
- list of jobs that other people with similar skills as you have applied for and/or successfully been accepted into
- most common missing skills
- most common missing skills weighted average
- most common skills learned (over all companies, same job, skills gained between rejection and final acceptance)
- users can update skill level
- companies update application status
- snapshot of user skill level is taken whenever one of their application statuses changes
- skill progression displayed using previous snapshots