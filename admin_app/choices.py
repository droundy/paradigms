# ActivityMedia media_type Choices
AMSAM = "Student Activity Media"
AMAM = "Activity Media"
ACTIVITYMEDIACHOICES = (
    (AMSAM, "Student Activity Media"),
    (AMAM, "Activity Media"),
)

# Activity Time Estimate Choices
TEC5 = 5
TEC10 = 10
TEC30 = 30
TEC60 = 60
TEC120 = 120

TIMEESTIMATECHOICES = (
    (TEC5, "Under 5 Minutes"),
    (TEC10, "5-10 Minutes"),
    (TEC30, "15-30 Minutes"),
    (TEC60, "1 Hour"),
    (TEC120, "2+ Hours"),
)

# Activity Type of Beast Choices
TBCSMALLGROUP = "Small Group Activity"
TBCSMALLBOARD = "Small White Board Question"
TBCMATHEMATICA = "Mathematica Activity"
TBCKINESTHETIC = "Kinesthetic"
TBCQUIZ = "Quiz"
TBCWHOLECLASS = "Whole Class Activity"
TBCEXPERIMENT = "Experiment"
TBCCOMPUTERSIM = "Computer Simulation"
TBCLECTURE = "Lecture"
# TBCHOMEWORK = "Homework"

TYPEOFBEASTCHOICES = (
    (TBCSMALLGROUP, "Small Group Activity"),
    (TBCSMALLBOARD, "Small White Board Question"),
    (TBCMATHEMATICA, "Mathematica Activity"),
    (TBCKINESTHETIC, "Kinesthetic"),
    (TBCQUIZ, "Quiz"),
    (TBCWHOLECLASS, "Whole Class Activity"),
    (TBCEXPERIMENT, "Experiment"),
    (TBCCOMPUTERSIM, "Computer Simulation"),
    (TBCLECTURE, "Lecture"),
    # (TBCHOMEWORK, "Homework"),
)

BEASTICONS = (
    (TBCSMALLGROUP, "puzzle-piece"),
    (TBCSMALLBOARD, "person"),
    (TBCMATHEMATICA, "code"),
    (TBCKINESTHETIC, "bolt"),
    (TBCQUIZ, "question-mark"),
    (TBCWHOLECLASS, "people"),
    (TBCEXPERIMENT, "beaker"),
    (TBCCOMPUTERSIM, "laptop"),
    (TBCLECTURE, "microphone"),
)

# Activity Publication Status Choices
PSCDRAFT = "Draft"
PSCPUBLISHED = "Published"
PSCPOSTPUBLICATIONDRAFT = "Post-Publication Draft"

PUBLICATIONSTATUSCHOICES = (
    (PSCDRAFT, "Draft"),
    (PSCPUBLISHED, "Published"),
    (PSCPOSTPUBLICATIONDRAFT, "Post-Publication Draft"),
)

CODE = "Code"
GUIDE = "Guide"
HANDOUT = "Handout"
PROMPT = "Prompt"
SOLUTION = "Solution"
SLIDES = "Slides"
FIGURE = "Figure"
OTHER = "Other"

# Media Type Choices
MEDIATYPECHOICES = (
    (GUIDE, "Guide"),
    (HANDOUT, "Handout"),
    (CODE, "Code"),
    (SOLUTION, "Solution"),
    (SLIDES, "Slides"),
    (PROMPT, "Prompt"),
    (FIGURE, "Figure"),
    (OTHER, "Other"),
)