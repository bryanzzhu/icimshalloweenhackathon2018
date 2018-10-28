# The "Companies Keep Rejecting Me" Support Site! (iCIMS Halloween Hackathon 2018)

### Winner of the "Best use of iCIMS Hackathon API" category!

[http://www.companieskeeprejecting.me](http://www.companieskeeprejecting.me)

(at the moment the actual website crashes, probably due to the size of the GET call, haven't tried it with a smaller dataset yet, but you can run it locally with `python flash_app.py` with no issues)

A facetious proof-of-concept application that tries to help job seekers with rejected offers figure out what went wrong and what areas they can improve on.

Lists most common skills that other applicants (accepted, and rejected, and all-inclusive) to this position have, sorted both by quantity alone and weighted according to the skill levels of the applicants with these skills.

This was my first experience using Flask and manipulating JSON files using Python; as such I was not able to implement most of what I had invisioned the app to be capable of.

Features To Come:

- list of jobs that other people with similar skills as you are applying to (sorted by most relevant to your field of expertise)
- list of jobs that other people with similar skills as you have applied for and/or successfully been accepted into
- most common missing skills
- most common missing skills weighted average
- most common skills learned (over all companies, same job, skills gained between rejection and final acceptance)
- users can update skill level
- companies update application status
- snapshot of user skill level is taken whenever one of their application statuses changes
- skill progression displayed using previous snapshots