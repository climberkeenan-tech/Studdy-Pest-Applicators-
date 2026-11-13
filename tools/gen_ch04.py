"""Generate content/chapters/ch04.json. Usage: python3 tools/gen_ch04.py content/chapters/ch04.json"""
import json, sys
CH = "Chapter 4 · Pesticide Formulations"
sections = []
cur = None

def card(title, pages, body, figures=None):
    global cur
    n = len(sections) + 1
    cur = {"id": f"c04-s{n:02d}", "chapter": CH, "title": title, "pages": pages, "body": body,
           "figures": figures or [], "questions": []}
    sections.append(cur)

def _q(d, style):
    d["id"] = f"{cur['id']}-t{len(cur['questions']) + 1}"
    d["src"] = "test"
    if style:
        d["style"] = style
    cur["questions"].append(d)

def mc(q, choices, ans, ref, why, style=None, fixed=False):
    d = {"kind": "mc", "q": q, "choices": choices, "answer": ans, "ref": ref, "why": why}
    if fixed:
        d["fixed"] = True
    _q(d, style)

def tf(q, ans, ref, why, style=None):
    _q({"kind": "tf", "q": q, "answer": ans, "ref": ref, "why": why}, style)

def sh(q, answer, keys, ref, why, accept=None, style=None):
    d = {"kind": "short", "q": q, "answer": answer, "keys": keys, "ref": ref, "why": why}
    if accept:
        d["accept"] = accept
    _q(d, style)

def img(id, title, page, file=None):
    return {"id": id, "title": title, "page": page, "imgFile": (file or id) + ".jpg"}

# ---------------------------------------------------------------- p. 49
card("What a pesticide formulation is", [49, 49], [
    {"box": "Learning objectives", "p": ["After studying this chapter, you should be able to:"], "list": [
        "Describe what a pesticide formulation is.",
        "Explain why pesticides are formulated for end use.",
        "Distinguish between active and inert ingredients.",
        "State the meaning of abbreviations used for common types of formulations, for example, WP.",
        "List the factors to consider when choosing a formulation for a specific site or situation.",
        "Discuss the properties of common formulations.",
        "Evaluate the advantages and disadvantages of the formulations described in this chapter.",
        "Explain the roles of adjuvants."]},
    {"p": [
        "A pesticide **formulation** is a combination of active and inert ingredients that forms an end-use pesticide product.",
        "Pesticides are formulated to make them safer or easier to use.",
        "This is because many pesticide **active ingredients**, in \"pure\" (**technical grade**) form, are not suitable for application.",
        "In their concentrated form, some are extremely toxic, many do not mix well with water, some are unstable, and some are difficult (or unsafe) to handle, transport, or store.",
        "To address these problems, manufacturers add **inert ingredients** to end-use pesticide products.",
        "Inert ingredients have **no pesticidal activity**, and some simply serve as **diluents** or **carriers**.",
        "In many cases, inert ingredients make the formulated product safer, easier to handle and apply, and/or more effective."]},
    {"p": ["So, in addition to the active ingredient intended to control the target pest, a formulated product may consist of:"]},
    {"list": [
        "A carrier or diluent, such as an organic solvent of mineral clay.",
        "Surface-active ingredients, such as **stickers** and **spreaders**.",
        "Other additives, such as stabilizers, dyes, and chemicals, which make the product safer or enhance pesticidal activity."]},
])
mc("What is a pesticide formulation?",
   ["A combination of active and inert ingredients that forms an end-use pesticide product",
    "The pure, technical grade active ingredient",
    "Any chemical added to a spray tank by the applicator",
    "The written directions on a pesticide label"], 0,
   "p. 49, chapter introduction", "The manual defines a formulation as active plus inert ingredients forming an end-use product.")
tf("Inert ingredients have no pesticidal activity.", True, "p. 49, chapter introduction",
   "Inert ingredients do not kill pests; some simply serve as diluents or carriers.")
mc("Which of these is NOT a reason the manual gives for why pure (technical grade) active ingredients are not suitable for application?",
   ["Some are extremely toxic in concentrated form", "Many do not mix well with water",
    "Some are unstable", "They have no pesticidal activity"], 3,
   "p. 49, chapter introduction", "Active ingredients are what control the pest; having no pesticidal activity describes inert ingredients.", style="not")
mc("A product label lists a clay that carries the active ingredient but does nothing to the pest itself. What is that clay?",
   ["An inert ingredient serving as a carrier or diluent", "A second active ingredient",
    "A technical grade pesticide", "An emulsifier"], 0,
   "p. 49, chapter introduction", "Inert ingredients with no pesticidal activity can serve as carriers or diluents.", style="scenario")
mc("Stickers and spreaders are examples of which kind of ingredient in a formulated product?",
   ["Surface-active ingredients", "Active ingredients", "Stabilizers", "Dyes"], 0,
   "p. 49, chapter introduction", "The manual lists stickers and spreaders as surface-active ingredients.")

# ---------------------------------------------------------------- p. 50
card("Where active ingredients come from", [50, 50], [
    {"h": "Formulations: an overview"},
    {"p": [
        "The active ingredients in pesticide products come from many sources.",
        "Some, such as **azadirachtin**, **pyrethrum**, and **rotenone**, are extracted from **plants**.",
        "Others are derived from **microbes or insects**, for example, **Bacillus thuringiensis** and insect growth regulators.",
        "Still others have a **mineral origin**, for example, **copper** and **sulfur**.",
        "However, the vast majority of active ingredients used today are **produced in laboratories**.",
        "These **synthetic** active ingredients may have been designed by a chemist or discovered through screening processes by examining chemicals generated by various industries or found in nature."]},
    {"p": [
        "Regardless of where they come from or how they are produced, pesticide active ingredients vary considerably in their physical and chemical properties.",
        "One variable is **solubility**.",
        "Some dissolve in water, but many do not.",
        "Some are soluble in oils or organic solvents.",
        "However, many such solvents are not available to applicators or safe to use.",
        "A few active ingredients do not dissolve readily in any **solvent**.",
        "**Solubility** and the **intended use** of the pesticide are two factors that determine how an active ingredient is formulated, that is, made into an end-use product."]},
])
mc("Azadirachtin, pyrethrum, and rotenone are active ingredients extracted from what source?",
   ["Plants", "Microbes", "Minerals", "Insects"], 0, "p. 50, 'Formulations: An Overview'",
   "The manual names these three as plant extracts.")
mc("Where do the vast majority of active ingredients used today come from?",
   ["They are produced in laboratories", "They are extracted from plants",
    "They are mined minerals", "They are derived from microbes"], 0, "p. 50, 'Formulations: An Overview'",
   "Most active ingredients today are synthetic, produced in laboratories.")
mc("Which of these is NOT an active ingredient of mineral origin named in the manual?",
   ["Copper", "Sulfur", "Bacillus thuringiensis"], 2,
   "p. 50, 'Formulations: An Overview'", "Bacillus thuringiensis is derived from microbes; copper and sulfur are mineral.", style="not")
sh("Name the two factors that determine how an active ingredient is formulated.", "Solubility and the intended use of the pesticide",
   [["solubility", "soluble", "dissolve", "dissolves"], ["use", "uses", "intended use", "used"]], "p. 50, 'Formulations: An Overview'",
   "Solubility and intended use determine how an active ingredient is made into an end-use product.")
mc("A company finds a new active ingredient that does not dissolve in water but does dissolve in an organic solvent. Which property is the manual describing that will shape how it is formulated?",
   ["Solubility", "Signal word", "Toxicity class", "Color"], 0, "p. 50, 'Formulations: An Overview'",
   "Solubility is one of the two factors that determine how an active ingredient is formulated.", style="scenario")

# ---------------------------------------------------------------- p. 50
card("Solutions, suspensions, and emulsions", [50, 50], [
    {"p": ["Liquid pesticide products are usually one of the following:"]},
    {"list": ["A solution.", "A suspension.", "An emulsion."]},
    {"h": "Solution"},
    {"p": [
        "A **solution** is made by dissolving a substance in a liquid.",
        "A true solution is a mixture, but it cannot be separated by filtration or other mechanical means.",
        "Once made, a true solution will not \"settle out\" and does not need shaking or stirring (**agitation**) to keep the mixed components in solution.",
        "Solutions are **transparent**: they will allow light to pass through them.",
        "However, this may not be obvious if one or more components of the mixture are dark in color and the solution is very concentrated.",
        "**Sweetened iced tea** and **saltwater** are examples of solutions."]},
    {"h": "Suspension"},
    {"p": [
        "A **suspension** is also a liquid mixture.",
        "However, a suspension is formed by dispersing fine (very small), **solid particles** in a liquid.",
        "These solid particles do not dissolve in the liquid carrier.",
        "Suspensions must be **agitated** to maintain uniform particle distribution.",
        "Otherwise, the undissolved parts of suspension mixtures will settle (or float to the top).",
        "Most suspensions are **cloudy or opaque**: they will not allow light to pass through them.",
        "Pesticide products formulated as suspensions are not water-soluble; they form more dilute suspensions when mixed with water to make a finished spray.",
        "Label directions for suspension formulations will instruct you to **shake well** before measuring and mixing.",
        "The label will further state to apply these products only with spray equipment that has enough agitation to keep the final mixture evenly distributed in the spray tank during application.",
        "A mixture of **flour and water** is an example of a suspension."]},
    {"h": "Emulsion"},
    {"p": [
        "An **emulsion** is a special kind of suspension: a mixture made by suspending **droplets of one liquid in another**.",
        "Each ingredient retains its unique properties and identity.",
        "To make an emulsion, an active ingredient is dissolved in an oil-based solvent and then further diluted with water.",
        "Some agitation may be necessary to keep an emulsion from separating.",
        "However, most emulsion pesticide product formulations have additives (**emulsifiers** or emulsifying agents) that prevent the product from settling.",
        "As a rule, emulsions have a **\"milky\" appearance**.",
        "An **emulsifiable concentrate (E or EC)** is an emulsion.",
        "**Homogenized milk** is an example of an emulsion."]},
])
mc("Which kind of liquid mixture will not settle out and needs no agitation once made?",
   ["A true solution", "A suspension", "An emulsion", "A flowable"], 0, "p. 50, 'Formulations: An Overview'",
   "A true solution does not settle out and does not need shaking or stirring.")
mc("Which of these is the manual's example of an emulsion?",
   ["Homogenized milk", "Saltwater", "Flour and water", "Sweetened iced tea"], 0, "p. 50, 'Formulations: An Overview'",
   "Homogenized milk is an emulsion; saltwater and iced tea are solutions; flour and water is a suspension.")
mc("Which of these is NOT true of a suspension?",
   ["It is made of fine solid particles dispersed in a liquid", "It must be agitated to keep particles evenly distributed",
    "Most are cloudy or opaque", "It is transparent and lets light pass through"], 3,
   "p. 50, 'Formulations: An Overview'", "Solutions are transparent; most suspensions are cloudy or opaque.", style="not")
mc("A label says to shake well before measuring and to use only spray equipment with enough agitation to keep the mixture evenly distributed in the tank. What kind of formulation is this most likely?",
   ["A suspension", "A true solution", "A fumigant", "A ready-to-use aerosol"], 0, "p. 50, 'Formulations: An Overview'",
   "Labels for suspension formulations give exactly these shake and agitation directions.", style="scenario")
tf("An emulsifiable concentrate (E or EC) is an emulsion.", True, "p. 50, 'Formulations: An Overview'",
   "The manual states that an emulsifiable concentrate is an emulsion.")
mc("What do emulsifiers do in an emulsion formulation?",
   ["Prevent the product from settling", "Kill the target pest", "Make the mixture transparent", "Turn the liquid into a gas"], 0,
   "p. 50, 'Formulations: An Overview'", "Emulsifiers, or emulsifying agents, are additives that prevent the product from settling.")

# ---------------------------------------------------------------- pp. 50-51
card("Dry products, concentrates, and ready-to-use", [50, 51], [
    {"p": [
        "Most **dry products** are made by adhering the active ingredient to some solid carrier, such as **talc**, **clay**, **silica** (the mineral quartz), or **plant residues**, for example, ground corncobs."]},
    {"h": "Concentrates"},
    {"p": [
        "Some pesticide products are sold in concentrate form and must be mixed or diluted before use.",
        "**Concentrates** come in both liquid and solid form.",
        "An emulsifiable concentrate is an example of a **liquid concentrate (LC)**.",
        "**Wettable powders (WP)**, **soluble powders (SP)**, and **water-dispersible granules/dry flowables (WDG/DF)** are examples of concentrated materials sold in **solid form**."]},
    {"h": "Ready-to-use"},
    {"p": [
        "Other formulations are sold **ready-to-use**.",
        "You can apply ready-to-use products with no further dilution or mixing.",
        "Examples include liquids prepared as end-use dilutions and **aerosol (A)**, **dust (D)**, **pellet (P)**, **granule (G)**, and most **bait (B)** formulation products.",
        "Manufacturers package many specialized pesticides, including products intended for residential uses by nonoccupational users, in ready-to-use formulations."]},
    {"h": "Cost versus risk"},
    {"p": [
        "Concentrates are often **less expensive** per treatment/unit area treated than ready-to-use formulations.",
        "However, this cost savings may be offset by other considerations.",
        "For example, concentrates are usually **more toxic** than dilute formulations of the same active ingredient.",
        "**More handling** is required to mix and load them.",
        "As a result, concentrates present a **higher exposure risk** to the user."]},
])
mc("Which of these is a concentrate sold in solid form?",
   ["Wettable powder (WP)", "Aerosol (A)", "Emulsifiable concentrate (EC)", "Granule (G)"], 0, "p. 51, 'Formulations: An Overview'",
   "WP, SP, and WDG/DF are concentrates sold in solid form; granules are ready-to-use.")
mc("Which of these is NOT one of the manual's examples of a ready-to-use formulation?",
   ["Aerosol (A)", "Dust (D)", "Granule (G)", "Soluble powder (SP)"], 3, "p. 51, 'Formulations: An Overview'",
   "Soluble powders are concentrates sold in solid form and must be mixed before use.", style="not")
mc("A crew switches from a ready-to-use product to the concentrate of the same active ingredient to save money. What does the manual say about the trade-off?",
   ["Concentrates are usually more toxic and need more handling, so they present a higher exposure risk",
    "Concentrates are safer because they are used in smaller amounts",
    "There is no difference in risk, only in price",
    "Concentrates cost more per unit area treated"], 0, "p. 51, 'Formulations: An Overview'",
   "Cost savings may be offset because concentrates are more toxic and need more mixing and loading.", style="scenario")
tf("Concentrates are often less expensive per treatment or unit area treated than ready-to-use formulations.", True,
   "p. 51, 'Formulations: An Overview'", "The manual says concentrates are often less expensive per unit area treated.")
mc("Which of these is NOT named as a solid carrier for dry products?",
   ["Talc", "Clay", "Ground corncobs", "Fuel oil"], 3, "p. 50, 'Formulations: An Overview'",
   "Talc, clay, silica, and plant residues such as ground corncobs are solid carriers; fuel oil is a liquid.", style="not")

# ---------------------------------------------------------------- p. 51 + Table 4.1
card("Formulation abbreviations and Table 4.1", [51, 51], [
    {"p": [
        "Abbreviations in trade or brand names are often used to describe the formulation, for example, **WP** for wettable powders.",
        "They may describe how the pesticide is used, for example, **TC** for termiticide concentrate.",
        "Or they may describe the characteristics of the formulation, for example, **LO** for a low-odor formulation.",
        "The amount of active ingredient (**a.i.**) and the kind of formulation are listed on the product label.",
        "Numbers in a product's trade or brand name may also indicate the amount of active ingredient it contains.",
        "For example, **80 WDG** indicates that this dry product contains **80% by weight** of active ingredient and is a water-dispersible granule.",
        "In this case, a **10-pound bag** of product contains **8 pounds of a.i.** and **2 pounds of inert ingredient**.",
        "Liquid formulations usually state the amount of a.i. in **pounds per gallon**.",
        "For example, **4F** means **4 pounds of the a.i. per gallon** in a flowable formulation.",
        "Some common formulation abbreviations are listed in Table 4.1."]},
    {"box": "Table 4.1 Abbreviations for Common Formulations", "list": [
        "A: Aerosol.", "AF: Aqueous flowable.", "B: Bait.", "C: Concentrate.", "D: Dust.",
        "DF: Dry flowables (see WDG).", "E: Emulsifiable concentrate.", "EC: Emulsifiable concentrate.",
        "F: Flowable.", "G: Granules.", "GL: Gel.", "L: Liquid.", "LC: Liquid concentrate.",
        "LV: Low volatile.", "M: Microencapsulated.", "P: Pellets.", "PS: Pellets.", "RTU: Ready-to-use.",
        "S: Solution.", "SP: Soluble powder (or soluble packet; see WSP).", "ULV: Ultra-low volume.",
        "W: Wettable powder.", "WDG: Water-dispersible granules (see DF).", "WP: Wettable powder.",
        "WS: Water soluble.", "WSB: Water-soluble bag (see WSP: water-soluble packet).",
        "WSC: Water-soluble concentrate.", "WSL: Water-soluble liquid.",
        "WSP: Water-soluble powder (or water-soluble packet; see WSB)."]},
])
mc("A 10-pound bag of a product labeled 80 WDG contains how many pounds of active ingredient?",
   ["8 pounds", "2 pounds", "10 pounds", "0.8 pounds"], 0, "p. 51, 'Formulations: An Overview'",
   "80 WDG is 80% active ingredient by weight, so 8 pounds a.i. and 2 pounds inert.")
mc("What does 4F mean on a liquid product?",
   ["4 pounds of active ingredient per gallon in a flowable formulation", "4% active ingredient in a flowable",
    "A fourth-generation formulation", "4 gallons of flowable per acre"], 0, "p. 51, 'Formulations: An Overview'",
   "Liquid formulations state a.i. in pounds per gallon; F is flowable.")
mc("Which of these abbreviation pairs is NOT correct according to Table 4.1?",
   ["LV: Liquid volume", "ULV: Ultra-low volume", "M: Microencapsulated", "GL: Gel"], 0, "p. 51, Table 4.1",
   "In Table 4.1, LV means low volatile.", style="not")
sh("What does the abbreviation WP stand for?", "Wettable powder", [["wettable", "wetable"], ["powder", "powders"]], "p. 51, Table 4.1",
   "WP, and also W, mean wettable powder.")
mc("You pick up a 25-pound bag labeled 80 WDG. Using the manual's rule, how much of the bag is inert ingredient?",
   ["5 pounds", "20 pounds", "8 pounds", "2 pounds"], 0, "p. 51, 'Formulations: An Overview'",
   "80% of 25 pounds is 20 pounds a.i., leaving 5 pounds inert.", style="scenario")
mc("In a brand name, what does TC indicate?",
   ["Termiticide concentrate", "Total coverage", "Toxicity category", "Tank compatible"], 0, "p. 51, 'Formulations: An Overview'",
   "The manual gives TC for termiticide concentrate as an abbreviation describing how the pesticide is used.")

# ---------------------------------------------------------------- pp. 51-52
card("Choosing a formulation", [51, 52], [
    {"p": [
        "A single active ingredient is often sold in several kinds of formulations.",
        "If more than one formulation is available for your pest control site and situation, choose the best one for the job."]},
    {"box": "Base your decision on:", "list": [
        "Legal, labeled uses.", "The signal word.", "Applicator safety.", "Environmental safety.", "Pest biology.",
        "Site characteristics.", "Target (surface to be treated).", "Appropriate and available application equipment."]},
    {"box": "Ask yourself these questions:", "list": [
        "Is the intended use listed on the product label?",
        "Do I have the necessary application equipment?",
        "Can the formulation be applied appropriately under the conditions in the application area?",
        "Will the formulation reach the intended target and stay in place long enough to control the pest?",
        "Is the formulation likely to damage the surface?",
        "Could I choose a less hazardous formulation that would still be as effective?"]},
    {"p": ["**Cost** is always a consideration, but **pesticide and pest management concerns should come first**."]},
])
mc("Which of these is NOT on the manual's list of things to base your formulation choice on?",
   ["The signal word", "Pest biology", "Site characteristics", "The brand name you used last year"], 3,
   "p. 52, 'Formulations: An Overview'", "The list covers labeled uses, signal word, safety, pest biology, site, target, and equipment.", style="not")
tf("When choosing a formulation, cost should come before pest management concerns.", False, "p. 52, 'Formulations: An Overview'",
   "Cost is always a consideration, but pesticide and pest management concerns should come first.")
mc("Two labeled formulations will control your pest equally well. One has a more hazardous profile. What does the manual tell you to ask?",
   ["Could I choose a less hazardous formulation that would still be as effective?", "Which one is cheaper per gallon?",
    "Which one has the strongest odor?", "Which one the supplier recommends most often?"], 0,
   "p. 52, 'Formulations: An Overview'", "The manual's checklist ends with choosing a less hazardous formulation that is still as effective.", style="scenario")
mc("What is the first question on the manual's checklist for choosing a formulation?",
   ["Is the intended use listed on the product label?", "Is the formulation likely to damage the surface?",
    "Do I have the necessary application equipment?", "What does it cost?"], 0, "p. 52, 'Formulations: An Overview'",
   "The first question is whether the intended use is on the label.")

# ---------------------------------------------------------------- pp. 52-53
card("Emulsifiable concentrates (E or EC)", [52, 53], [
    {"h": "Liquid formulations"},
    {"p": [
        "Most liquid formulations are **diluted with water** to make a finished spray.",
        "However, some labels direct users to mix the product with another solvent such as **crop oil** or other light oil as a carrier."]},
    {"h": "Emulsifiable concentrates (E or EC)"},
    {"p": [
        "An emulsifiable concentrate formulation usually contains an **oil-soluble liquid active ingredient**, one or more **petroleum-based solvents**, and a **mixing agent**.",
        "The mixing agent allows the formulation to be mixed with water to form an emulsion.",
        "Most ECs contain between **2 and 6 pounds of active ingredient per gallon**.",
        "ECs are among the **most versatile** formulations.",
        "They are used against pests in agricultural, ornamental and turf, forestry, structural, food processing, livestock, and public health settings.",
        "ECs are adaptable to many types of application equipment, from small, portable sprayers to hydraulic sprayers, low-volume ground sprayers, mist blowers, and low-volume aircraft sprayers."]},
    {"box": "Advantages", "list": [
        "Relatively easy to handle, transport, and store.", "Easy to pour and measure.",
        "Little agitation required; will not settle out or separate when equipment is running.",
        "Not abrasive; does not cause excessive equipment wear.", "Will not usually plug screens or nozzles.",
        "Leave little visible residue on treated surfaces."]},
    {"box": "Disadvantages", "list": [
        "High concentration of active ingredient(s) makes it easy to overdose or underdose through mixing or calibration errors.",
        "May damage treated plants or surfaces (petroleum-based solvents or overdosing may cause **phytotoxicity**).",
        "Easily absorbed through skin of humans or animals.",
        "Splashes and spills are relatively difficult to clean up and/or decontaminate.",
        "Many have a strong odor.",
        "Solvents may cause equipment \"wear and tear.\" For example, rubber or plastic hoses, gaskets, pump parts, and other exposed surfaces may deteriorate.",
        "May cause pitting or discoloration of painted finishes or other treated surfaces.",
        "**Flammable**; should be used and stored away from heat or open flame.",
        "May be corrosive."]},
])
mc("Most emulsifiable concentrates contain how much active ingredient?",
   ["Between 2 and 6 pounds per gallon", "Almost 100%", "1% or less", "Between 15% and 95%"], 0,
   "p. 52, 'Emulsifiable Concentrates (E or EC)'", "Most ECs contain 2 to 6 pounds of active ingredient per gallon.")
mc("Which of these is NOT an advantage of emulsifiable concentrates?",
   ["Easy to pour and measure", "Not abrasive to equipment", "Leave little visible residue",
    "Not flammable, so storage near heat is safe"], 3, "pp. 52–53, 'Emulsifiable Concentrates (E or EC)'",
   "ECs are flammable and should be used and stored away from heat or open flame.", style="not")
mc("While mixing an EC, a worker splashes concentrate on bare forearms. Which EC disadvantage makes this especially serious?",
   ["ECs are easily absorbed through skin of humans or animals", "ECs plug nozzles", "ECs are abrasive", "ECs settle out quickly"], 0,
   "p. 53, 'Emulsifiable Concentrates (E or EC)'", "Easy skin absorption is a listed EC disadvantage.", style="scenario")
sh("What is the term for damage to plants caused by a pesticide, such as from petroleum-based solvents or overdosing?", "Phytotoxicity",
   [["phytotoxicity", "phytotoxic"]], "p. 53, 'Emulsifiable Concentrates (E or EC)'", "Petroleum-based solvents or overdosing may cause phytotoxicity.",
   accept=["phytotoxic"])
mc("Why is it easy to overdose or underdose with an EC?",
   ["Its high concentration of active ingredient makes mixing or calibration errors matter more", "It settles out in the tank",
    "It plugs screens and nozzles", "It cannot be measured by volume"], 0, "p. 52, 'Emulsifiable Concentrates (E or EC)'",
   "The high concentration makes it easy to overdose or underdose through mixing or calibration errors.")

# ---------------------------------------------------------------- p. 53
card("Solutions (S) and ready-to-use solutions", [53, 53], [
    {"h": "Solutions (S)"},
    {"p": [
        "Some pesticide active ingredients dissolve readily in a liquid solvent, such as water or a petroleum-based diluent.",
        "When mixed, they form a solution that **does not settle out or separate**.",
        "Formulations of these pesticides usually contain the active ingredient, solvent (carrier or diluent), and one or more other ingredients.",
        "Solutions are suitable for **any type of sprayer, indoors or outdoors**.",
        "Consequently, they are registered for many sites, including structural, institutional, public health, and household pest control; livestock and poultry pest management; space sprays in barns and warehouses; and treatment of food and fiber crops, turf, and ornamental plants."]},
    {"h": "Ready-to-use (RTU) low-concentrate solutions"},
    {"p": [
        "Ready-to-use formulations require **no further dilution** before application.",
        "They consist of a small amount of active ingredient (often **1% or less** per unit volume).",
        "Some ready-to-use products contain petroleum-based solvents; others are water-based.",
        "Many RTU products are produced for pest management professionals (who treat structural and institutional pests) and for nonoccupational users."]},
    {"box": "Advantages", "list": [
        "Convenient; neither measuring nor mixing is required.",
        "Some are packaged and sold in, or with, an application device. If this is the case, no loading is required.",
        "Less personal exposure risk due to reduced toxicity and handling."]},
    {"box": "Disadvantages", "list": ["Limited availability.", "High cost per unit of active ingredient."]},
    {"p": ["The time saved and convenience of using RTU products may outweigh the product cost."]},
])
mc("Ready-to-use low-concentrate solutions often contain how much active ingredient?",
   ["1% or less per unit volume", "Between 2 and 6 pounds per gallon", "Almost 100%", "At least 50%"], 0,
   "p. 53, 'Ready-to-Use (RTU) Low-Concentrate Solutions'", "RTU solutions consist of a small amount of a.i., often 1% or less.")
mc("Which of these is NOT true of solution (S) formulations?",
   ["They do not settle out or separate", "They are suitable for any type of sprayer, indoors or outdoors",
    "They are registered for many sites", "They must be constantly agitated in the tank"], 3, "p. 53, 'Solutions (S)'",
   "Solutions do not settle out, so they do not need constant agitation.", style="not")
mc("Which is a listed disadvantage of RTU low-concentrate solutions?",
   ["High cost per unit of active ingredient", "High exposure risk from mixing", "They settle in the tank", "They are abrasive"], 0,
   "p. 53, 'Ready-to-Use (RTU) Low-Concentrate Solutions'", "RTU disadvantages are limited availability and high cost per unit of a.i.")
mc("A homeowner wants to treat a few ants on a patio without measuring or mixing anything. Which formulation fits, according to the manual's description?",
   ["A ready-to-use (RTU) low-concentrate solution", "An emulsifiable concentrate", "A wettable powder", "An ultra-low-volume concentrate"], 0,
   "p. 53, 'Ready-to-Use (RTU) Low-Concentrate Solutions'", "RTU products need no measuring or mixing and are made for nonoccupational users.", style="scenario")

# ---------------------------------------------------------------- pp. 53-54
card("Concentrate solutions and liquid baits", [53, 54], [
    {"h": "Concentrate solutions (C, LC, or WSC/WSL)"},
    {"p": [
        "Other solutions are available as concentrates that require dilution with a liquid solvent before you apply them.",
        "Often the solvent is water, but it may also be a refined oil or petroleum-based solvent.",
        "When diluted with the label-specified carrier, these formulations form **true solutions**."]},
    {"box": "Advantages", "list": [
        "Relatively easy to handle, transport, and store; easy to pour and measure.", "No agitation necessary.",
        "Not abrasive; do not cause excessive equipment wear.", "Do not plug screens or nozzles.",
        "Do not usually leave visible residues on treated surfaces."]},
    {"box": "Disadvantages", "list": [
        "Limited availability, especially water-based solutions.",
        "Spills and splashes may be difficult to clean up and/or decontaminate.",
        "Some are easily absorbed through skin of humans or animals."]},
    {"p": ["The other benefits and drawbacks of concentrated solutions vary.",
           "They depend on the concentration of active ingredient, solvent or diluent used, application site, and application equipment."]},
    {"h": "Liquid baits"},
    {"p": [
        "Some insecticides and rodenticides are now formulated as **liquid baits**.",
        "Most liquid insecticides are **concentrated sugar solutions**.",
        "They are packaged in ready-to-use bait stations to kill **ants and cockroaches**.",
        "As a rule, **liquid rodenticide baits** are mixed with water and placed in specially designed bait stations.",
        "They are useful in sites where **sanitation is poor** because traditional food-based baits \"compete\" with other food sources.",
        "As is the case with solid baits, you must place bait stations in safe, strategic locations while following label directions and taking care to protect children and nontarget organisms."]},
    {"box": "Advantages", "list": [
        "Liquid ant baits are very useful in controlling sugar-feeding ants.",
        "Ants that will feed on liquid baits carry this material to the colony.",
        "Liquid rodenticide baits will often control rodents in areas where **food is abundant, but water is scarce** or lacking altogether."]},
    {"box": "Disadvantages", "list": [
        "Not all ants, cockroaches, and rodents will feed on liquid baits.",
        "You must refill or replace liquid-containing bait stations frequently."]},
    {"fig": "p54-baitstation"},
    {"p": ["For information about solid-formulation baits, refer to \"Baits\" in the \"Dry or Solid Formulations\" section."]},
], [img("p54-baitstation", "A bait station used in rodent control in the closed and open positions. Bait formulations are placed inside the tamper-resistant station.", "p. 54")])
mc("A grain warehouse has plenty of spilled food but almost no water. Which formulation does the manual say often controls rodents in this kind of area?",
   ["Liquid rodenticide baits", "Dust formulations", "Granules", "Ultra-low-volume concentrates"], 0, "p. 54, 'Liquid Baits'",
   "Liquid rodenticide baits often control rodents where food is abundant but water is scarce.", style="scenario")
mc("Most liquid insecticide baits are what?",
   ["Concentrated sugar solutions", "Oil-based emulsions", "Microencapsulated powders", "Fumigant gels"], 0, "p. 54, 'Liquid Baits'",
   "Most liquid insecticide baits are concentrated sugar solutions packaged in RTU bait stations.")
mc("Which of these is NOT an advantage of concentrate solutions?",
   ["No agitation necessary", "Do not plug screens or nozzles", "Not abrasive", "Spills are easy to clean up"], 3,
   "p. 53, 'Concentrate Solutions'", "Spills and splashes may be difficult to clean up; that is a disadvantage.", style="not")
tf("Ants that feed on liquid baits carry the material back to the colony.", True, "p. 54, 'Liquid Baits'",
   "This is a listed advantage of liquid ant baits.")
mc("Which is a disadvantage of liquid baits?",
   ["Bait stations must be refilled or replaced frequently", "They are highly abrasive", "They drift easily", "They require a respirator"], 0,
   "p. 54, 'Liquid Baits'", "You must refill or replace liquid-containing bait stations frequently.")

# ---------------------------------------------------------------- p. 54
card("Ultra-low volume (ULV)", [54, 54], [
    {"h": "Ultra-low volume"},
    {"p": [
        "Ultra-low-volume concentrates have **almost 100% active ingredient**.",
        "They are designed to be used \"as is\" or diluted with only small quantities of specified solvents.",
        "These special-purpose formulations are most suitable for **outdoor** applications, such as in agricultural, forestry, ornamental, and **mosquito control** programs.",
        "ULV products are applied as **very fine droplets** at very low rates per unit area (or volume)."]},
    {"box": "Advantages", "list": [
        "Relatively easy to handle, transport, and store.", "Little or no agitation required.", "Not abrasive to equipment.",
        "Do not plug screens and nozzles.", "Leave little visible residue on treated surfaces."]},
    {"box": "Disadvantages", "list": [
        "**High drift hazard** due to small droplet size.", "Specialized equipment required.",
        "Easily absorbed through skin of humans or animals; high dermal and inhalation exposure risk (concentrated product applied as fine droplets).",
        "Products and/or solvents may cause rubber or plastic hoses, gaskets, and pump parts and other surfaces to deteriorate.",
        "Calibration and application must be performed with special care because ULV products are applied in concentrated form."]},
])
mc("How much active ingredient do ultra-low-volume concentrates have?",
   ["Almost 100%", "1% or less", "10% or less", "2 to 6 pounds per gallon"], 0, "p. 54, 'Ultra-Low Volume'",
   "ULV concentrates have almost 100% active ingredient.")
mc("Which of these is NOT an advantage of ULV formulations?",
   ["Little or no agitation required", "Not abrasive to equipment", "Low drift hazard", "Do not plug screens and nozzles"], 2,
   "p. 54, 'Ultra-Low Volume'", "ULV has a high drift hazard because of its small droplet size.", style="not")
mc("What causes the high drift hazard of ULV products?",
   ["Small droplet size", "Large, heavy droplets", "Abrasive particles", "Their sugar content"], 0, "p. 54, 'Ultra-Low Volume'",
   "ULV is applied as very fine droplets, which drift.")
mc("A county mosquito program is switching to a ULV product. Why must calibration be done with special care?",
   ["ULV products are applied in concentrated form", "ULV products settle in the tank", "ULV products plug nozzles", "ULV products are mixed with large volumes of water"], 0,
   "p. 54, 'Ultra-Low Volume'", "Calibration needs special care because ULV is applied in concentrated form.", style="scenario")

# ---------------------------------------------------------------- p. 55
card("Invert emulsions", [55, 55], [
    {"h": "Invert emulsions"},
    {"p": [
        "**Invert emulsions** contain a **water-soluble pesticide dispersed in an oil carrier**.",
        "These products require a special kind of emulsifier that allows the pesticide to be mixed with a large volume of petroleum-based carrier, usually **fuel oil**.",
        "Invert emulsions are **less susceptible to drift** because **oil evaporates more slowly than water**.",
        "When applied on a hot, dry day, a water-based droplet will become smaller as the water portion of the droplet evaporates.",
        "Invert emulsion droplets do not \"shrink\" as rapidly when applied in the same weather conditions.",
        "This means less drift and more pesticide on target.",
        "Invert emulsions are thick mixtures, with the consistency of **mayonnaise**.",
        "In addition, invert emulsions are applied as **very large droplets**, which reduce drift."]},
    {"p": [
        "The oil phase of this kind of formulation also serves as a **sticker-spreader**.",
        "This quality improves rainfast properties and surface coverage.",
        "It also increases **absorption** and/or penetration.",
        "This, in turn, reduces loss due to runoff.",
        "Invert emulsions are relatively uncommon.",
        "They are most often used in **weed control on rights-of-way** to reduce the chance of drift to susceptible nontarget plants or sensitive areas."]},
    {"box": "Advantages", "list": ["Low drift.", "Increased rate of penetration and/or absorption.", "Increased rainfastness and reduced runoff."]},
    {"box": "Disadvantages", "list": [
        "Difficult to treat the underside of foliage or other targets because droplets are large and heavy.", "Limited availability."]},
])
mc("What does an invert emulsion contain?",
   ["A water-soluble pesticide dispersed in an oil carrier", "An oil-soluble pesticide dispersed in water",
    "Solid particles suspended in water", "A gas under pressure"], 0, "p. 55, 'Invert Emulsions'",
   "Invert emulsions are the reverse of an EC: water-soluble pesticide in an oil carrier, usually fuel oil.")
mc("Why are invert emulsions less susceptible to drift?",
   ["Oil evaporates more slowly than water, and the droplets are very large", "They are applied as very fine droplets",
    "They contain almost 100% active ingredient", "They dissolve completely in water"], 0, "p. 55, 'Invert Emulsions'",
   "Oil droplets do not shrink as fast as water droplets, and invert emulsions are applied as very large droplets.")
mc("A road crew must control weeds along a right-of-way next to a sensitive vineyard. Which formulation does the manual say is most often used for this purpose?",
   ["Invert emulsion", "Ultra-low-volume concentrate", "Dust", "Smoke or fog formulation"], 0, "p. 55, 'Invert Emulsions'",
   "Invert emulsions are most often used in rights-of-way weed control to reduce drift to nontarget plants.", style="scenario")
mc("Which of these is NOT an advantage of invert emulsions?",
   ["Low drift", "Increased rainfastness", "Easy coverage of the underside of foliage", "Increased penetration and/or absorption"], 2,
   "p. 55, 'Invert Emulsions'", "Large, heavy droplets make the underside of foliage difficult to treat.", style="not")
tf("Invert emulsions are thick mixtures with the consistency of mayonnaise.", True, "p. 55, 'Invert Emulsions'",
   "The manual compares their consistency to mayonnaise.")

# ---------------------------------------------------------------- p. 55
card("Flowables (F or AF)", [55, 55], [
    {"h": "Flowables (F or AF)"},
    {"p": [
        "Some active ingredients are **insoluble solids**: substances that will not dissolve in either water or oil.",
        "These may be formulated as **flowables**.",
        "Most manufacturers use the letter **\"F\"** by the trade name to designate that the formulation is a flowable.",
        "However, some use the letter **\"L,\"** meaning that an insoluble material is presented in \"liquid\" form.",
        "Most flowables are prepared by first impregnating them onto a dry carrier, such as clay.",
        "Then, the active ingredient plus carrier (or the active ingredient alone) are ground into a fine powder.",
        "Next, the fine powder is suspended in a very small amount of liquid (and perhaps other inert ingredients).",
        "The resulting product is a **thick liquid suspension**."]},
    {"p": [
        "Flowables combine many of the characteristics of **liquid emulsifiable concentrates and dry wettable powders**.",
        "They appear in the \"Liquid Formulations\" section because the end-use product is a thick liquid.",
        "Flowables are often used for the same types of pest control operations as ECs."]},
    {"box": "Advantages", "list": [
        "Easy to handle and apply; low exposure risk.", "Generally not phytotoxic.", "Seldom clog nozzles.",
        "Splashes are less likely than with other liquid formulations."]},
    {"box": "Disadvantages", "list": [
        "May settle; need shaking before measuring and mixing.",
        "Difficult to remove all of product from the container. Containers may be difficult to rinse.",
        "Require moderate agitation.",
        "May be **abrasive**; contribute to \"wear and tear\" of spray application equipment.",
        "Spills may be harder to clean up.", "May leave a visible residue on treated surfaces."]},
])
mc("Flowables are made from active ingredients that are what?",
   ["Insoluble solids that will not dissolve in water or oil", "Liquids that dissolve in water",
    "Gases under pressure", "Oils that dissolve in fuel oil"], 0, "p. 55, 'Flowables (F or AF)'",
   "Flowables are used for insoluble solids.")
mc("Flowables combine many of the characteristics of which two formulations?",
   ["Emulsifiable concentrates and wettable powders", "Dusts and granules", "Aerosols and fumigants", "Baits and pellets"], 0,
   "p. 55, 'Flowables (F or AF)'", "Flowables combine characteristics of liquid ECs and dry WPs.")
mc("Which of these is NOT a disadvantage of flowables?",
   ["May settle and need shaking", "Containers may be difficult to rinse", "May be abrasive", "Usually phytotoxic"], 3,
   "p. 55, 'Flowables (F or AF)'", "Flowables are generally not phytotoxic; that is an advantage.", style="not")
mc("You open a jug of flowable that has been sitting in storage. What does the manual say to do before measuring?",
   ["Shake it, because flowables may settle", "Heat it to thin the liquid", "Add a buffer first", "Nothing; flowables never settle"], 0,
   "p. 55, 'Flowables (F or AF)'", "Flowables may settle and need shaking before measuring and mixing.", style="scenario")
tf("Some manufacturers use the letter L for a flowable, meaning an insoluble material is presented in liquid form.", True,
   "p. 55, 'Flowables (F or AF)'", "Most use F, but some use L.")

# ---------------------------------------------------------------- pp. 55-56
card("Aerosols and smoke or fog generators", [55, 56], [
    {"h": "Aerosols (A)"},
    {"p": [
        "Aerosol formulations contain one or more active ingredients and a solvent.",
        "Most aerosols contain a **low percentage** of active ingredient.",
        "There are two types of aerosol formulations:"]},
    {"list": [
        "The ready-to-use type (often sold in pressurized sealed containers that serve as application devices).",
        "Those made for use in electric or gasoline-powered aerosol generators that release the formulated product as a smoke or fog."]},
    {"h": "Ready-to-use aerosols"},
    {"p": [
        "Ready-to-use aerosol formulations are usually small, self-contained units that release pesticide when the nozzle valve is triggered.",
        "An inert pressurized gas pushes the pesticide through a fine opening when the gas is released, creating fine droplets.",
        "These products are effective in greenhouses, in small areas inside buildings, or in localized outdoor areas.",
        "Commercial models, which hold **5 to 10 pounds** of pesticide, are usually **refillable**."]},
    {"box": "Advantages", "list": [
        "Easy to use; convenient.", "Portable.", "Easily stored.", "Convenient way to buy and apply a small amount of pesticide.",
        "Retain potency for some time."]},
    {"box": "Disadvantages", "list": [
        "Practical for only a few limited or specialized uses.", "Risk of inhalation exposure.",
        "Hazardous if punctured, overheated, or used near an open flame.",
        "May be difficult to direct material released to a single target site or pest."]},
    {"h": "Formulations for smoke or fog generators"},
    {"p": [
        "Formulations for smoke or fog generators are **not packaged and sold under pressure**.",
        "They are used in machines that break the liquid formulation into a fine mist or fog (aerosol).",
        "Using a rapidly whirling disk or heated surface, the machines produce and distribute very fine droplets.",
        "These formulations are used mainly for **insect control in structures** such as greenhouses, barns, and warehouses and for **outdoor mosquito and biting fly control**."]},
    {"box": "Advantages", "list": ["Easy way to fill an entire space with pesticide."]},
    {"box": "Disadvantages", "list": [
        "Highly specialized use sites and equipment.", "Difficult to confine to target site or pest.",
        "Spills and splashes may be difficult to clean up and/or decontaminate.",
        "May require **respiratory protection** to prevent inhalation exposure."]},
])
mc("Commercial ready-to-use aerosol models hold how much pesticide?",
   ["5 to 10 pounds", "1 to 2 pounds", "20 to 50 pounds", "Less than 1 ounce"], 0, "p. 56, 'Ready-to-Use Aerosols'",
   "Commercial models hold 5 to 10 pounds and are usually refillable.")
mc("Which of these is NOT true of formulations for smoke or fog generators?",
   ["They are packaged and sold under pressure", "They are used in machines that make a fine mist or fog",
    "They are used mainly for insect control in structures", "They may require respiratory protection"], 0,
   "p. 56, 'Formulations for Smoke or Fog Generators'", "Smoke and fog formulations are not packaged and sold under pressure.", style="not")
mc("You are fogging the inside of a warehouse for insects. Which disadvantage of fog formulations matters most for your own safety?",
   ["They may require respiratory protection to prevent inhalation exposure", "They plug screens and nozzles",
    "They settle in the tank", "They are phytotoxic"], 0, "p. 56, 'Formulations for Smoke or Fog Generators'",
   "Fog formulations may require respiratory protection.", style="scenario")
mc("Which is a disadvantage of ready-to-use aerosols?",
   ["Hazardous if punctured, overheated, or used near an open flame", "Require constant agitation",
    "Very high percentage of active ingredient", "Abrasive to pumps"], 0, "p. 56, 'Ready-to-Use Aerosols'",
   "RTU aerosol cans are hazardous if punctured, overheated, or near open flame.")
tf("Most aerosols contain a high percentage of active ingredient.", False, "p. 55, 'Aerosols (A)'",
   "Most aerosols contain a low percentage of active ingredient.")

# ---------------------------------------------------------------- pp. 56-57
card("Dry formulations: dusts (D)", [56, 57], [
    {"h": "Dry or solid formulations"},
    {"p": [
        "There are two general types of dry formulations.",
        "Some are ready-to-use.",
        "Others are concentrates, which must be mixed with water and applied as a spray."]},
    {"h": "Dusts (D)"},
    {"p": [
        "Most dust formulations are ready-to-use and contain a low percentage of active ingredient (usually **10% or less** by weight).",
        "A few dust formulations, however, are concentrates and contain a much higher percentage of active ingredient.",
        "These concentrates must be mixed with dry inert carriers before application."]},
    {"p": [
        "Dusts have one or more active ingredients plus a very fine, dry inert carrier made from **talc, chalk, clay, nut hulls, or volcanic ash**.",
        "The size of individual dust particles varies, but all are quite small.",
        "Due to their small size, dusts need careful handling to prevent nontarget exposure, including **drift**.",
        "They are **not water-soluble**.",
        "Therefore, do not mix them with a liquid solvent."]},
    {"p": [
        "**Dusts are always used dry.**",
        "They are often used as **seed treatments** and in some other agricultural operations.",
        "Some ornamental and garden pest management products aimed at homeowners are dust formulations.",
        "In structures, dust formulations are useful to treat **cracks and crevices** and for spot treatments to control insect pests.",
        "Dusts are also a good tool to control lice, fleas, and other external parasites on pets and livestock."]},
    {"fig": "p57-dust"},
    {"p": [
        "Special dusts known as **tracking powders** are effective for insect and rodent monitoring and control.",
        "These products are finely ground dusts with an adsorbed **stomach poison**.",
        "Insects and rodents walk through the dust, pick it up on their legs and bodies or feet and fur, and ingest the poisonous dust when grooming.",
        "Tracking powders are effective in sites and situations where **bait acceptance is poor** (for example, where food is abundant).",
        "NOTE: Another option is to use a nontoxic powder, such as **talc or flour**, to monitor and track rodent activity in buildings."]},
    {"fig": "p57-bulbduster"},
    {"box": "Advantages", "list": [
        "Usually ready-to-use; no mixing.", "A good alternative where moisture from a spray might cause damage.",
        "Applied with simple application equipment.", "Effective in hard-to-reach indoor areas."]},
    {"box": "Disadvantages", "list": [
        "Easily drift off target during application.",
        "Residues do not adhere to treated surfaces, including foliage, as well as liquids do; may easily wash off or blow away.",
        "May irritate eyes, nose, throat, and skin; pose a relatively high inhalation exposure risk to handlers.",
        "Dampness may cause product to clump and equipment to clog; difficult to apply in damp or humid environments.",
        "Some kinds of application equipment and devices are hard to calibrate.",
        "Difficult to get an even distribution of particles."]},
], [img("p57-dust", "Dust formulations are always used dry.", "p. 57"),
    img("p57-bulbduster", "A bulb duster used for applying dust formulations to cracks, crevices, and voids in buildings.", "p. 57")])
mc("Most ready-to-use dust formulations contain how much active ingredient?",
   ["Usually 10% or less by weight", "Usually 50% or more", "1% to 15%", "Almost 100%"], 0, "p. 56, 'Dusts (D)'",
   "Most dusts are RTU with usually 10% or less a.i. by weight.")
mc("How do tracking powders work?",
   ["Pests walk through the dust, pick it up, and ingest it when grooming", "They release a gas that fills the space",
    "They attract pests with food", "They are absorbed through plant roots"], 0, "p. 57, 'Dusts (D)'",
   "Tracking powders carry an adsorbed stomach poison that pests swallow while grooming.")
mc("Which of these is NOT an advantage of dusts?",
   ["Usually ready-to-use", "Effective in hard-to-reach indoor areas",
    "Residues adhere to foliage better than liquids", "A good alternative where moisture from a spray might cause damage"], 2,
   "p. 57, 'Dusts (D)'", "Dust residues do not adhere as well as liquids and may wash off or blow away.", style="not")
mc("A restaurant has a rodent problem, but the rodents ignore bait because food is everywhere. Which dust product does the manual describe for this situation?",
   ["Tracking powder", "Seed treatment dust", "Wettable powder", "Talc mixed with water"], 0, "p. 57, 'Dusts (D)'",
   "Tracking powders are effective where bait acceptance is poor, for example, where food is abundant.", style="scenario")
tf("Dusts may be mixed with a liquid solvent before application.", False, "p. 57, 'Dusts (D)'",
   "Dusts are not water-soluble, are always used dry, and should not be mixed with a liquid solvent.")
mc("What nontoxic powders does the manual suggest for monitoring rodent activity in buildings?",
   ["Talc or flour", "Clay or silica", "Chalk or volcanic ash", "Sugar or salt"], 0, "p. 57, 'Dusts (D)'",
   "The NOTE suggests a nontoxic powder such as talc or flour.")

# ---------------------------------------------------------------- pp. 57-58
card("Granules (G)", [57, 58], [
    {"h": "Granules (G)"},
    {"p": [
        "Granular formulations are similar to dust formulations; however, granular particles are **larger and heavier**.",
        "Like dusts, they are **not water-soluble**.",
        "They are ready-to-use, not intended to be mixed with water and applied as a liquid suspension.",
        "The coarse particles that serve as carriers for granular formulations are adsorptive substances like clay or absorptive plant material such as ground corncobs or walnut shells.",
        "The active ingredient either coats the outside of the granules or is absorbed into them.",
        "The amount of active ingredient is relatively low, usually ranging from **1% to 15%**."]},
    {"p": [
        "Because many granular formulations use carriers that absorb moisture, **humidity** will affect particle size and mass.",
        "This, in turn, will affect flow rate.",
        "Also, different \"batches\" of the same formulation may differ slightly in size or shape and density.",
        "For these reasons, you must **calibrate granular application devices often**."]},
    {"fig": "p58-granules"},
    {"p": [
        "Once applied, granules **slowly release** the adsorbed or absorbed active ingredient.",
        "Some require soil moisture, rain, or watering to initiate the release of the active ingredient.",
        "Other granules do so as they decompose.",
        "Granular pesticides are mostly used to apply chemicals to the **soil**, where they control weeds, nematodes, and insects or are absorbed by plant roots.",
        "Most granular formulations are used to deliver **systemic pesticides**.",
        "Granules are a common choice in many sites and situations.",
        "Aerial applicators sometimes use granular formulations to reduce drift or penetrate dense vegetation.",
        "Granular formulations are also useful in aquatic situations to control mosquito larvae and aquatic weeds."]},
    {"box": "Advantages", "list": [
        "Ready-to-use; no mixing.", "Drift hazard is low, and particles settle quickly.", "Low applicator hazard: no spray; little dust.",
        "Weight carries the formulation through foliage to soil or water target.",
        "Applied with simple application equipment, such as seeders or fertilizer spreaders.",
        "May break down more slowly than WPs or ECs because of a slow-release coating."]},
    {"box": "Disadvantages", "list": [
        "Application equipment needs frequent calibration.",
        "Application equipment is not as convenient to calibrate as spray equipment. Released particles are measured by **weight instead of by volume**.",
        "Uniform application may be difficult with some devices, for example, rotary spreaders.",
        "Granules do not stick to foliage or other uneven surfaces. For this reason, **contact products are rarely formulated this way**.",
        "May need to be incorporated into soil or planting medium.",
        "May need moisture to release the active ingredient; may not be effective in **drought** conditions.",
        "May be hazardous to nontarget species, especially **waterfowl and other birds**. This is because birds may feed on grain- or seed-like granules or mistake them for \"grit\" they need to grind up their food.",
        "Bulky; low percentage of active ingredient per unit volume."]},
], [img("p58-granules", "Granular formulations are larger and heavier than dust formulations.", "p. 58")])
mc("The amount of active ingredient in granules usually ranges from what?",
   ["1% to 15%", "10% or less", "5% to 95%", "Almost 100%"], 0, "p. 57, 'Granules (G)'",
   "Granules are relatively low in a.i., usually 1% to 15%.")
mc("Why must granular application devices be calibrated often?",
   ["Humidity changes particle size and mass, and batches differ slightly in size, shape, and density",
    "Granules dissolve in the hopper", "Granules are abrasive to spray nozzles", "Granules are measured by volume"], 0,
   "pp. 57–58, 'Granules (G)'", "Moisture and batch differences change flow rate, so calibrate often.")
mc("Which of these is NOT an advantage of granules?",
   ["Low drift hazard", "Ready-to-use; no mixing", "They stick well to foliage", "Applied with simple equipment such as fertilizer spreaders"], 2,
   "p. 58, 'Granules (G)'", "Granules do not stick to foliage, so contact products are rarely formulated this way.", style="not")
mc("Why are granules hazardous to waterfowl and other birds?",
   ["Birds may eat them as food or mistake them for grit", "The granules release a gas birds inhale",
    "The granules drift onto nests", "The granules make water toxic only at night"], 0, "p. 58, 'Granules (G)'",
   "Birds may feed on grain- or seed-like granules or mistake them for grit.")
mc("A turf manager applies a granular product during a long dry spell and gets poor control. What is the most likely reason, according to the manual?",
   ["Granules may need moisture to release the active ingredient", "Granules drift badly in dry air",
    "Granules are phytotoxic in drought", "Granules must be mixed with water first"], 0, "p. 58, 'Granules (G)'",
   "Granules may need moisture and may not be effective in drought conditions.", style="scenario")
tf("Most granular formulations are used to deliver systemic pesticides.", True, "p. 58, 'Granules (G)'",
   "The manual states this directly.")

# ---------------------------------------------------------------- p. 58
card("Pellets (P or PS)", [58, 58], [
    {"h": "Pellets (P or PS)"},
    {"p": [
        "Most pellet formulations are very similar to granular formulations in their uses, advantages, and disadvantages.",
        "However, in pellet formulations, all the particles are **more or less the same weight and shape**.",
        "They are produced by combining the active ingredient with inert materials to form a **\"slurry\"**, a thick liquid mixture.",
        "This mixture is then **extruded under pressure**.",
        "As a result, pellets are **round in cross section** and cut to a specific length.",
        "Because pellet particles are more uniform, you can apply them with **precision**.",
        "However, in many cases, pellets are applied as **spot treatments**.",
        "A few **fumigants** are formulated as pellets and are clearly labeled as such to avoid confusing them with nonfumigant pellets."]},
    {"fig": "p58-pellets"},
], [img("p58-pellets", "In pellet formulations, all particles are the same weight and shape.", "p. 58")])
mc("What is the key difference between pellets and granules?",
   ["In pellets, all particles are more or less the same weight and shape", "Pellets dissolve in water",
    "Pellets have almost 100% active ingredient", "Pellets are always fumigants"], 0, "p. 58, 'Pellets (P or PS)'",
   "Pellets are uniform; granules can vary in size, shape, and density.")
mc("How are pellets produced?",
   ["A slurry of active and inert ingredients is extruded under pressure and cut to length",
    "Active ingredient is sprayed onto corncobs", "A powder is compressed into dust-free granules", "Droplets are coated with plastic"], 0,
   "p. 58, 'Pellets (P or PS)'", "Pellets are extruded from a slurry, so they are round in cross section.")
mc("Which of these is NOT true of pellets, according to the manual?",
   ["They can be applied with precision", "In many cases they are applied as spot treatments",
    "A few fumigants are formulated as pellets", "Fumigant pellets look and are labeled the same as nonfumigant pellets"], 3,
   "p. 58, 'Pellets (P or PS)'", "Fumigant pellets are clearly labeled to avoid confusing them with nonfumigant pellets.", style="not")
mc("You find two pellet products in a shed. One label says it is a fumigant. Why does the manual stress that label?",
   ["To avoid confusing fumigant pellets with nonfumigant pellets", "Because fumigant pellets are always green",
    "Because fumigant pellets must be dissolved in water", "Because only fumigant pellets need calibration"], 0,
   "p. 58, 'Pellets (P or PS)'", "Fumigant pellets are clearly labeled so they are not confused with ordinary pellets.", style="scenario")

# ---------------------------------------------------------------- pp. 58-59
card("Wettable powders (WP or W)", [58, 59], [
    {"h": "Wettable powders (WP or W)"},
    {"p": [
        "Wettable powders are dry, finely ground solid materials.",
        "Most include **wetting and/or dispersing agents**.",
        "Usually, they must be mixed with water and applied as a spray.",
        "A few products, however, may be applied dry or as a liquid suspension."]},
    {"p": [
        "Wettable powders contain **5% to 95%** active ingredient, usually **50% or more**.",
        "Wettable powder particles **do not dissolve** in water.",
        "When mixed with water, they form a **suspension**.",
        "They will settle out quickly without constant agitation to keep them suspended."]},
    {"p": [
        "To prepare a spray suspension, you must form a **slurry**.",
        "Mix a WP with a small amount of water, and then dilute this slurry mixture further."]},
    {"p": [
        "Wettable powders are effective for most pest problems and in most types of spray equipment where agitation is possible.",
        "They have **excellent residual activity** and do not usually harm treated surfaces.",
        "When you apply a WP spray suspension to a target, most of the pesticide **remains on the surface**.",
        "This is true even for porous materials, such as concrete, plaster, and untreated wood.",
        "In such cases, only the water carrier penetrates the porous material.",
        "Wettable powder particles remain on the treated surface."]},
    {"fig": "p59-wp"},
    {"box": "Advantages", "list": [
        "Easy to store, transport, and handle.",
        "Less likely than ECs and other petroleum-based formulations to harm treated plants, animals, and surfaces.",
        "As a rule, not phytotoxic.",
        "Less risk of skin and eye absorption than ECs and other liquid formulations."]},
    {"box": "Disadvantages", "list": [
        "Not easy to measure; must be weighed.", "Not easy to mix.",
        "**Inhalation hazard** to applicator while measuring and mixing the concentrated powder.",
        "Suspended particles require good and constant agitation (usually mechanical) in the spray tank and quickly settle out if agitation ceases.",
        "Abrasive to pumps and nozzles; cause equipment wear.", "Difficult to mix in very hard or very alkaline water.",
        "If not mixed properly, may clog nozzles and screens.", "Residues may be visible on treated surfaces."]},
], [img("p59-wp", "Wettable powders are dry, finely ground formulations that look like dusts.", "p. 59")])
mc("Wettable powders contain how much active ingredient?",
   ["5% to 95%, usually 50% or more", "1% to 15%", "Usually 10% or less", "Usually less than 5%"], 0, "p. 59, 'Wettable Powders (WP or W)'",
   "WPs contain 5% to 95% a.i., usually 50% or more.")
mc("How do you prepare a wettable powder spray suspension?",
   ["Form a slurry with a small amount of water, then dilute it further", "Dump the powder into a full tank with no agitation",
    "Dissolve it in fuel oil", "Apply it dry, then water it in"], 0, "p. 59, 'Wettable Powders (WP or W)'",
   "You must form a slurry first, then dilute.")
mc("You spray a WP on an untreated wood wall to control insects. What happens to the pesticide?",
   ["Only the water carrier soaks in; most of the pesticide stays on the surface", "The pesticide soaks deep into the wood",
    "The pesticide dissolves and evaporates", "Nothing stays on the surface"], 0, "p. 59, 'Wettable Powders (WP or W)'",
   "On porous surfaces, only the water penetrates and WP particles remain on the surface.", style="scenario")
mc("Which of these is NOT a disadvantage of wettable powders?",
   ["Inhalation hazard while measuring and mixing", "Abrasive to pumps and nozzles",
    "Phytotoxic as a rule", "Difficult to mix in very hard or very alkaline water"], 2, "p. 59, 'Wettable Powders (WP or W)'",
   "As a rule, WPs are not phytotoxic; that is an advantage.", style="not")
tf("Wettable powder particles dissolve in water.", False, "p. 59, 'Wettable Powders (WP or W)'",
   "WP particles do not dissolve; they form a suspension that needs constant agitation.")

# ---------------------------------------------------------------- pp. 59-60
card("Water-dispersible granules and soluble powders", [59, 60], [
    {"h": "Water-dispersible granules (WDG) or dry flowables (DF)"},
    {"p": [
        "Water-dispersible granular formulations are **wettable powder formulations compressed into dust-free, granule-sized particles**.",
        "Most come with a product-specific measuring device, with dry ounce (or pound) increment marks based on product density (weight per unit volume).",
        "Because of this and the fact that they readily flow or pour out of their containers, they are easier to measure and cleaner to handle than WPs.",
        "Like wettable powders, water-dispersible granules are mixed with water and applied as a spray suspension.",
        "Once in water, the granules break apart into fine powder.",
        "The formulation requires **constant agitation** to keep it suspended in water.",
        "Water-dispersible granules share the advantages and disadvantages of wettable powders.",
        "However, WDGs have one added benefit: **reduced handler exposure risk**.",
        "This is because WDGs/DFs are:"]},
    {"list": ["Made of larger, less \"dusty\" particles.", "Easier to remove from their container and measure."]},
    {"gallery": ["p59-wdg-before", "p59-wdg-after"]},
    {"h": "Soluble powders (SP or WSP)"},
    {"p": [
        "Soluble powder formulations look like wettable powders.",
        "However, when mixed with water, soluble powders **dissolve readily** in water and form a **true solution**.",
        "After a thorough mixing, **no additional agitation** is necessary.",
        "The amount of active ingredient in soluble powders ranges from **15% to 95%**; it usually is **more than 50%**.",
        "Soluble powders have all the advantages of WPs but only one of the disadvantages: **inhalation hazard during mixing**.",
        "Not many pesticides are available in this formulation because very few active ingredients dissolve in water."]},
], [img("p59-wdg-before", "Water-dispersible granule before mixing.", "p. 59"),
    img("p59-wdg-after", "Water-dispersible granule after mixing.", "p. 59")])
mc("What are water-dispersible granules?",
   ["Wettable powder formulations compressed into dust-free, granule-sized particles", "Granules that dissolve into a true solution",
    "Ready-to-use granules spread dry on soil", "Granules coated in plastic"], 0, "p. 59, 'Water-Dispersible Granules (WDG) or Dry Flowables (DF)'",
   "WDGs are compressed wettable powders.")
mc("What one added benefit do WDGs have over wettable powders?",
   ["Reduced handler exposure risk", "No agitation needed", "They form a true solution", "They are not abrasive"], 0,
   "p. 59, 'Water-Dispersible Granules (WDG) or Dry Flowables (DF)'", "Larger, less dusty particles that are easier to measure reduce handler exposure.")
mc("Which of these is NOT true of soluble powders?",
   ["They form a true solution in water", "No additional agitation is needed after thorough mixing",
    "Many pesticides are available in this formulation", "Their one WP disadvantage is inhalation hazard during mixing"], 2,
   "p. 60, 'Soluble Powders (SP or WSP)'", "Not many pesticides come as soluble powders because very few active ingredients dissolve in water.", style="not")
mc("A crew mixes a WDG into the spray tank, then shuts off the agitator during a long lunch break. What does the manual predict?",
   ["The product will not stay suspended, because WDGs need constant agitation", "Nothing; WDGs form a true solution",
    "The product will turn into a gas", "The product will become phytotoxic"], 0,
   "p. 59, 'Water-Dispersible Granules (WDG) or Dry Flowables (DF)'", "WDGs break into fine powder in water and need constant agitation to stay suspended.", style="scenario")
mc("Soluble powders contain how much active ingredient?",
   ["15% to 95%, usually more than 50%", "5% to 95%, usually 50% or more", "1% to 15%", "Usually less than 5%"], 0,
   "p. 60, 'Soluble Powders (SP or WSP)'", "Soluble powders range from 15% to 95% a.i., usually more than 50%.")

# ---------------------------------------------------------------- p. 60
card("Baits (B) and pastes, gels, and injectable baits", [60, 60], [
    {"h": "Baits (B)"},
    {"p": [
        "A **bait** formulation is an active ingredient mixed with **food or another attractive substance**.",
        "The bait either attracts the pests or is placed where the pests will find it.",
        "Many baits are solid (blocks, granules, or pellets), but some are liquids, pastes, or gels.",
        "The amount of active ingredient in most bait formulations is quite low, usually **less than 5%**."]},
    {"p": [
        "Baits are used inside buildings to control ants, cockroaches, flies, and other insects.",
        "Outdoors, they can control **vertebrate pests**, such as rodents, other mammals, and birds as well as snails, slugs, and some insects.",
        "Applicators must place bait stations in safe, strategic locations while following label directions to protect children and nontarget organisms."]},
    {"box": "Advantages", "list": [
        "Ready-to-use.", "Entire area need not be covered because pest goes to bait.", "Control pests that move in and out of an area."]},
    {"box": "Disadvantages", "list": [
        "May be attractive to children and pets.", "May kill domestic animals and nontarget wildlife.",
        "Require careful placement and inspection.", "Pest may prefer the crop or other food to the bait.",
        "Dead vertebrate pests may cause odor problems.",
        "If baits are not removed after the pesticide stops working, they may serve as a food supply for the target pest or other pests.",
        "May not work in situations where pests have many other food or water sources."]},
    {"p": ["For information about liquid baits, see \"Liquid Formulations\" above."]},
    {"h": "Pastes, gels, and other injectable baits"},
    {"p": [
        "Pastes and gel baits are mainly used in the pest control industry for **ants and cockroaches**.",
        "In fact, insecticides formulated as pastes and gels are now the **primary formulations used in cockroach control**.",
        "They are designed to be injected or placed as either a bead or dot inside small cracks and crevices of building elements where insects tend to hide or travel.",
        "Two basic types of tools are used to apply pastes and gels: **syringes and bait guns**.",
        "The bait is forced out of the tip of the device by applying pressure to a plunger or trigger."]},
    {"fig": "p60-baitgun"},
    {"box": "Advantages", "list": [
        "Odorless; no vapors.", "Low human toxicity.", "Last for long periods.", "Low applicator exposure risk.",
        "Hidden placements minimize human and pet exposure.", "Very accurate in their placement and dosage.",
        "Easily placed where insects shelter for maximum effectiveness."]},
    {"box": "Disadvantages", "list": [
        "Can become contaminated from exposure to other pesticides and cleaning products.",
        "When exposed to high temperatures, gels can run and drip.", "May stain porous surfaces.",
        "Repeated applications can cause an unsightly buildup."]},
], [img("p60-baitgun", "A bait gun used by the pest control industry to treat small cracks and crevices.", "p. 60")])
mc("The amount of active ingredient in most bait formulations is usually what?",
   ["Less than 5%", "10% or less", "1% to 15%", "More than 50%"], 0, "p. 60, 'Baits (B)'",
   "Most baits are quite low in a.i., usually less than 5%.")
mc("What are now the primary formulations used in cockroach control?",
   ["Pastes and gels", "Dusts", "Fumigants", "Ultra-low-volume sprays"], 0, "p. 60, 'Pastes, Gels, and Other Injectable Baits'",
   "Insecticides formulated as pastes and gels are now the primary cockroach control formulations.")
mc("Which of these is NOT a disadvantage of baits?",
   ["May be attractive to children and pets", "Pest may prefer the crop or other food", "The entire area must be covered",
    "Dead vertebrate pests may cause odor problems"], 2, "p. 60, 'Baits (B)'",
   "The entire area need not be covered because the pest goes to the bait; that is an advantage.", style="not")
mc("A technician leaves rodent bait out for months after it stops working. What does the manual warn can happen?",
   ["The old bait may serve as a food supply for the target pest or other pests", "The bait turns into a fumigant",
    "The bait becomes more toxic over time", "Nothing; old bait is harmless"], 0, "p. 60, 'Baits (B)'",
   "Baits not removed after they stop working may feed the target pest or other pests.", style="scenario")
mc("Which is a disadvantage of gel baits?",
   ["When exposed to high temperatures, gels can run and drip", "They have strong vapors", "High human toxicity", "Inaccurate placement"], 0,
   "p. 60, 'Pastes, Gels, and Other Injectable Baits'", "Gels can run and drip in heat, stain porous surfaces, and build up.")
sh("Name the two basic types of tools used to apply pastes and gels.", "Syringes and bait guns",
   [["syringe", "syringes"], ["gun", "guns"]], "p. 60, 'Pastes, Gels, and Other Injectable Baits'", "Pastes and gels are applied with syringes and bait guns.")

# ---------------------------------------------------------------- p. 61
card("Other formulations: fumigants", [61, 61], [
    {"h": "Other formulations"},
    {"p": ["This section describes other formulations that:"]},
    {"list": [
        "Are not easily classified as liquid or dry/solid.", "Are formulated and/or applied as gases.",
        "Have some special packaging or delivery method."]},
    {"h": "Fumigants"},
    {"p": [
        "**Fumigants** are pesticides that deliver the active ingredient to the target site in the form of a **gas**.",
        "Some active ingredients are liquids when packaged under high pressure but become gases when released.",
        "Other active ingredients are **volatile** liquids.",
        "They may be enclosed in an ordinary container and not packaged under pressure.",
        "Still others are solids that release gases after application in humid conditions or in the presence of water or water vapor.",
        "Fumigants are used for structural pest control, in food- and grain-storage facilities, and in regulatory pest control at **ports of entry** and state and national borders.",
        "In agricultural pest control, fumigants are effective in soil, greenhouses, and commodity storage areas (such as grain bins)."]},
    {"fig": "p61-fumigants"},
    {"box": "Advantages", "list": [
        "Toxic to a wide range of pests.",
        "Can penetrate cracks, crevices, wood, and tightly packed areas (such as soil or grains).",
        "A single treatment will usually kill most pests in the treated space."]},
    {"box": "Disadvantages", "list": [
        "The target site must be **enclosed or covered** to prevent the gas from escaping.",
        "**Nonspecific** and highly toxic to humans and all other organisms.", "**High inhalation exposure risk.**",
        "Most require the use of specialized personal protective equipment.",
        "May require the use of specialized application equipment.", "Some have specific temperature requirements."]},
], [img("p61-fumigants", "Fumigants are packaged in liquid and solid forms. Both turn into poisonous gases when applied.", "p. 61")])
mc("What is a fumigant?",
   ["A pesticide that delivers the active ingredient to the target site in the form of a gas", "A fine dust blown into cracks",
    "A smoke made by a fog generator", "A liquid bait in a station"], 0, "p. 61, 'Fumigants'",
   "Fumigants deliver the active ingredient as a gas.")
mc("Which of these is NOT an advantage of fumigants?",
   ["Toxic to a wide range of pests", "Can penetrate tightly packed areas such as grain",
    "A single treatment usually kills most pests in the space", "Low inhalation exposure risk"], 3, "p. 61, 'Fumigants'",
   "Fumigants carry a high inhalation exposure risk.", style="not")
mc("You must fumigate a grain bin. What must be done to the site for the fumigant to work?",
   ["Enclose or cover it to prevent the gas from escaping", "Leave doors open for airflow",
    "Wet the grain first so the gas dissolves", "Spread granules on top"], 0, "p. 61, 'Fumigants'",
   "The target site must be enclosed or covered to keep the gas in.", style="scenario")
tf("Fumigants are nonspecific and highly toxic to humans and all other organisms.", True, "p. 61, 'Fumigants'",
   "This is a listed fumigant disadvantage.")
mc("Where does the manual say fumigants are used in regulatory pest control?",
   ["At ports of entry and state and national borders", "In home gardens", "On pets and livestock", "In mosquito larvae habitats"], 0,
   "p. 61, 'Fumigants'", "Regulatory fumigation happens at ports of entry and state and national borders.")

# ---------------------------------------------------------------- pp. 61-62
card("Microencapsulated pesticides (M)", [61, 62], [
    {"h": "Microencapsulated pesticides (M)"},
    {"p": [
        "**Microencapsulated** pesticides are dry particles or liquid droplets surrounded by a **coating**.",
        "Coatings may be plastic, starch, or some other material.",
        "Microencapsulated pesticides are mixed with water and applied as a spray.",
        "Once applied, the pesticide is released from the capsule.",
        "In some situations, the encapsulation process can provide **\"timed\" slow release** of the active ingredient.",
        "Depending on the physical properties of the coating, release of the pesticide active ingredient may be **weather-dependent**.",
        "If the release is slower than normal (for example, due to dry or cool weather), residues may remain on treated plants or surfaces longer than expected.",
        "As a result, some microencapsulated products have relatively long **restricted-entry or preharvest intervals**."]},
    {"p": [
        "Some microencapsulated pesticide products contain highly toxic materials with a coating to increase handler safety.",
        "Others are microencapsulated for different reasons; for example, to reduce staining or odor or to protect the active ingredient from photodegradation.",
        "Highly toxic microencapsulated pesticides may be very hazardous to **bees** if the particles do not break down quickly and are the **same size as pollen grains**.",
        "Foraging bees may collect them and carry them back to the hive.",
        "Later, when the coatings break down and release the pesticide, the colony may be poisoned.",
        "Some microencapsulated soil-applied products may be more prone to **leaching**."]},
    {"box": "Advantages", "list": [
        "Coatings help protect the applicator.", "Easy to mix, handle, and apply.",
        "Timed release of active ingredient prolongs effectiveness (that is, may result in fewer applications; application timing may be less critical).",
        "Reduced volatility.", "Reduced odor.", "Less likely to stain or otherwise damage treated surfaces.", "Reduced phytotoxicity."]},
    {"box": "Disadvantages", "list": [
        "Constant agitation may be necessary in spray tank (depending on the properties of the coating).",
        "Risk of injuring or killing bees (if the microencapsulated product is toxic to them).",
        "Long restricted-entry or preharvest intervals for highly toxic products."]},
])
mc("Why can highly toxic microencapsulated pesticides be very hazardous to bees?",
   ["Particles the same size as pollen grains may be carried back to the hive and later poison the colony",
    "The coating attracts bees like nectar", "They release a gas inside the hive immediately", "They kill flowers"], 0,
   "p. 61, 'Microencapsulated Pesticides (M)'", "Pollen-sized capsules that do not break down quickly can be carried to the hive.")
mc("A microencapsulated product is applied during a cool, dry week. What does the manual warn may happen?",
   ["Release may be slower, so residues may remain on plants or surfaces longer than expected", "The capsules explode and drift",
    "The product becomes a fumigant", "The active ingredient is released all at once"], 0,
   "p. 61, 'Microencapsulated Pesticides (M)'", "Release may be weather-dependent, so dry or cool weather can leave residues longer.", style="scenario")
mc("Which of these is NOT an advantage of microencapsulated pesticides?",
   ["Coatings help protect the applicator", "Reduced odor", "Reduced volatility", "Short restricted-entry intervals for highly toxic products"], 3,
   "p. 62, 'Microencapsulated Pesticides (M)'", "Highly toxic microencapsulated products can have long restricted-entry or preharvest intervals.", style="not")
tf("Microencapsulated pesticides are mixed with water and applied as a spray.", True, "p. 61, 'Microencapsulated Pesticides (M)'",
   "The manual states this directly.")
mc("Some microencapsulated soil-applied products may be more prone to what?",
   ["Leaching", "Drift", "Phytotoxicity", "Freezing"], 0, "p. 61, 'Microencapsulated Pesticides (M)'",
   "The manual says some soil-applied microencapsulated products may be more prone to leaching.")

# ---------------------------------------------------------------- pp. 62-63
card("Water-soluble packaging, impregnates, and animal systemics", [62, 63], [
    {"h": "Water-soluble packaging (WSB or WSP)"},
    {"p": [
        "More and more pesticide products are available in **water-soluble bags** (WSBs).",
        "A special film packages a precise amount of wettable powder, soluble powder, or gel containing the pesticide active ingredient(s).",
        "When added to water in a spray tank, the bag dissolves and releases the contents, which then are suspended or dissolved.",
        "This packaging method **reduces handler exposure risk**.",
        "It also simplifies measuring.",
        "However, water-soluble packaging is just that: as a rule, it **will not dissolve in organic solvents or undiluted ECs**.",
        "As a result, mixers and loaders must follow label instructions when preparing a spray mixture.",
        "Store water-soluble products in a **dry place**, and **do not handle them with damp or wet gloves**."]},
    {"fig": "p62-wsp"},
    {"box": "Advantages", "list": [
        "Accurate premeasured unit doses.", "Increased handler safety; greatly reduced exposure risk.", "Lower risk of spills."]},
    {"box": "Disadvantages", "list": [
        "Package size may not match volume of prepared solution needed and/or spray tank volume.",
        "May not be suitable for products applied in pounds or gallons of active ingredient per acre, due to the size or number of packets required.",
        "Must be kept dry, away from water or high humidity, until ready to use."]},
    {"h": "Impregnates"},
    {"p": [
        "Some pesticide products consist of a pesticide active ingredient incorporated into a solid material, usually some kind of **plastic**.",
        "The pesticide evaporates or is released over time, and the vapors control nearby pests.",
        "Common examples include:"]},
    {"list": ["Livestock ear tags.", "Plastic pest strips and adhesive tapes.", "Pet collars."]},
    {"p": ["Fertilizers may also be impregnated with pesticides."]},
    {"h": "Animal systemics"},
    {"p": [
        "**Animal systemics** are absorbed by, enter the tissues of, and move within the treated animal.",
        "Usually, these pesticides are applied **externally or orally**.",
        "They can control fleas and other external blood-feeding insects as well as worms and other internal parasites.",
        "External application methods include **pour-on liquids**, sprays, and dusts.",
        "Oral applications include food additives and premeasured capsules, pastes, or liquids."]},
    {"h": "Pesticide-fertilizer combinations"},
    {"p": [
        "Many pesticide products, usually **granule and pellet** formulations, are combinations of fertilizers and pesticides.",
        "Such products are convenient because they allow the applicator to control pests and apply nutrients at the same time.",
        "Some are prepackaged: homeowners commonly use these for their lawns.",
        "Dealers or growers may custom mix pesticides with fertilizers to meet specific crop requirements."]},
], [img("p62-wsp", "Adding water-soluble packet to a spray tank.", "p. 62")])
mc("A mixer reaches for a water-soluble packet while wearing wet gloves. What does the manual say?",
   ["Do not handle water-soluble products with damp or wet gloves", "Wet gloves are fine because the bag is waterproof",
    "Wet the bag first so it dissolves faster", "Water-soluble bags must be cut open before use"], 0,
   "p. 62, 'Water-Soluble Packaging (WSB or WSP)'", "Store them dry and do not handle them with damp or wet gloves.", style="scenario")
mc("Water-soluble packaging, as a rule, will NOT dissolve in what?",
   ["Organic solvents or undiluted ECs", "Water in a spray tank", "Warm water", "Water with a buffer"], 0,
   "p. 62, 'Water-Soluble Packaging (WSB or WSP)'", "WSBs dissolve in water but not in organic solvents or undiluted ECs.")
mc("Which of these is NOT an example of an impregnate?",
   ["Livestock ear tags", "Pet collars", "Plastic pest strips", "A wettable powder in a spray tank"], 3, "p. 62, 'Impregnates'",
   "Impregnates are solid materials, usually plastic, that release pesticide over time.", style="not")
mc("What are animal systemics?",
   ["Pesticides absorbed by, entering the tissues of, and moving within the treated animal", "Baits placed for wild animals",
    "Fumigants used in barns", "Repellents sprayed on fences"], 0, "p. 62, 'Animal Systemics'",
   "Animal systemics move within the treated animal and can control external and internal parasites.")
mc("Pesticide-fertilizer combinations are usually which formulations?",
   ["Granule and pellet formulations", "Aerosols and fogs", "Emulsifiable concentrates", "Gels and pastes"], 0,
   "p. 62, 'Pesticide-Fertilizer Combinations'", "Most pesticide-fertilizer products are granules and pellets.")
mc("Which is a disadvantage of water-soluble packaging?",
   ["Package size may not match the spray tank volume needed", "High handler exposure", "High risk of spills", "Inaccurate doses"], 0,
   "p. 62, 'Water-Soluble Packaging (WSB or WSP)'", "Packets are premeasured, so they may not match the volume you need.")

# ---------------------------------------------------------------- p. 63
card("Pesticide mixtures and tank mixing", [63, 63], [
    {"h": "Pesticide mixtures"},
    {"p": [
        "Sometimes, product manufacturers combine pesticides with other pesticides or fertilizers for sale as **premixes**.",
        "However, when premixes are not available (or are not offered in the desired combination), you may combine products at the time of application.",
        "**Tank mixing**, combining two or more crop-production products (pesticides and/or fertilizers) and applying them at the same time, is convenient and cost-effective.",
        "This practice can save the time, labor, fuel, and equipment wear involved in multiple applications.",
        "Tank mixing also reduces soil compaction and the risk of mechanical damage to crops or treated areas.",
        "Situations appropriate for tank mixing include combining fungicides and insecticides to treat fruit trees or field crops.",
        "Another common example is combining herbicides to increase the number of weed species controlled (**control spectrum**).",
        "However, products must be **compatible** in order to be tank-mixed."]},
    {"p": [
        "**Federal law allows applicators to combine pesticides unless the labeling** of one or more components of the intended tank mix **specifically prohibits it**.",
        "If no prohibitions exist, applicators may mix:"]},
    {"list": ["Pesticide with fertilizer.", "Two or more pesticides."]},
    {"p": [
        "When pesticides are tank-mixed, all of the dosages must be **at or below the label rate** for each separate component of the mixture.",
        "For more information about the causes and effects of incompatibility, how to do a compatibility test, and how to prepare a tank mix, see Chapter 10, Planning the Pesticide Application."]},
    {"fig": "p63-incompat"},
], [img("p63-incompat", "Incompatibility is a condition that prevents pesticides from mixing together properly to form a uniform solution or suspension.", "p. 63")])
mc("When does federal law allow applicators to combine pesticides in a tank mix?",
   ["Unless the labeling of one or more components specifically prohibits it", "Only when the EPA issues a special permit",
    "Only when all labels specifically list the tank mix", "Never; only premixes are legal"], 0, "p. 63, 'Pesticide Mixtures'",
   "Tank mixing is allowed unless a component's labeling specifically prohibits it.")
mc("When pesticides are tank-mixed, what rule applies to the dosage of each component?",
   ["Each must be at or below its label rate", "Each may be 10% above the label rate", "Only the total must match one label", "Dosage no longer matters"], 0,
   "p. 63, 'Pesticide Mixtures'", "All dosages must be at or below the label rate for each separate component.")
mc("You want to tank-mix an insecticide and a fungicide for an orchard. The fungicide label says it must not be tank-mixed with that insecticide. What should you do?",
   ["Do not tank-mix them; the label prohibition controls", "Mix them anyway, because federal law allows tank mixing",
    "Mix them at half rates", "Add an adjuvant and mix them"], 0, "p. 63, 'Pesticide Mixtures'",
   "Federal law allows mixing only when no component's labeling prohibits it.", style="scenario")
mc("Which of these is NOT a benefit of tank mixing named in the manual?",
   ["Saves time, labor, and fuel", "Reduces soil compaction", "Allows exceeding label rates", "Reduces equipment wear"], 2,
   "p. 63, 'Pesticide Mixtures'", "Dosages must stay at or below each label rate.", style="not")
sh("What is the term for a condition that prevents pesticides from mixing together properly to form a uniform solution or suspension?",
   "Incompatibility", [["incompatibility", "incompatible"]], "p. 63, photo caption", "The caption defines incompatibility.", accept=["incompatible"])

# ---------------------------------------------------------------- pp. 63-64
card("Adjuvants: what they are and how to use them", [63, 64], [
    {"h": "Adjuvants"},
    {"p": ["An **adjuvant** is a chemical that can affect how a pesticide works.", "Adjuvants:"]},
    {"list": [
        "Improve the action of a pesticide.",
        "Change the characteristics of a pesticide formulation or a spray mixture (suspension or solution)."]},
    {"p": [
        "Most end-use pesticide products, especially those that are applied to foliage, contain adjuvants.",
        "However, in some situations, applicators may add them to a tank mix when making a finished spray mixture.",
        "Many adjuvants increase effectiveness and/or safety.",
        "Although they enhance the action of a pesticide or modify the properties of a spray solution, **adjuvants alone have no pesticidal activity**.",
        "Use them to customize the product or formulation for specific needs or to compensate for local conditions."]},
    {"p": [
        "Because adjuvants lack pesticidal properties, the U.S. Environmental Protection Agency **does not register them**.",
        "As a result, there are **no standards** for composition, quality, or performance.",
        "If you have questions about an adjuvant, **contact the manufacturer**.",
        "Companies that produce these products can provide labels, technical data sheets, Safety Data Sheets (SDSs), supplemental labeling, and promotional literature."]},
    {"p": [
        "Before using any adjuvant, **consult the pesticide product label**.",
        "Some products have very specific adjuvant recommendations or prohibitions.",
        "If a label instructs you to use an adjuvant, use the **type called for at the directed rate**.",
        "As noted, many products already contain those adjuvants deemed necessary or useful by the manufacturer or formulator.",
        "Adding others may actually **decrease efficacy** or result in unintended, and possibly undesirable, effects."]},
])
mc("Why does the U.S. EPA not register adjuvants?",
   ["Because adjuvants lack pesticidal properties", "Because adjuvants are too toxic", "Because states register them instead",
    "Because they are always included in the pesticide"], 0, "p. 63, 'Adjuvants'",
   "Adjuvants lack pesticidal properties, so EPA does not register them and there are no standards.")
tf("Adjuvants alone have no pesticidal activity.", True, "p. 63, 'Adjuvants'",
   "They enhance a pesticide or modify a spray solution but do not kill pests on their own.")
mc("A pesticide label tells you to add a surfactant. What does the manual say to do?",
   ["Use the type called for at the directed rate", "Use any adjuvant you have on hand",
    "Double the rate for better coverage", "Skip it, because adjuvants are not registered"], 0, "pp. 63–64, 'Adjuvants'",
   "If the label calls for an adjuvant, use that type at the directed rate.", style="scenario")
mc("Which of these is NOT true about adjuvants, according to the manual?",
   ["EPA sets standards for their quality and performance", "They can change the characteristics of a spray mixture",
    "Most end-use products applied to foliage already contain them", "Adding extra ones may decrease efficacy"], 0,
   "pp. 63–64, 'Adjuvants'", "Because EPA does not register adjuvants, there are no standards for composition, quality, or performance.", style="not")
mc("If you have questions about an adjuvant, whom does the manual tell you to contact?",
   ["The manufacturer", "The U.S. EPA", "The state police", "Your neighbor"], 0, "p. 63, 'Adjuvants'",
   "The manufacturer can provide labels, technical data sheets, and SDSs.")

# ---------------------------------------------------------------- p. 64
card("Types of adjuvants", [64, 64], [
    {"h": "Types of adjuvants"},
    {"p": ["There are many types of adjuvants.", "Here are some that are commonly used:"]},
    {"list": [
        "**Antifoaming (defoaming) agents**: reduce foaming of spray mixtures that may result from using some surfactants and/or from vigorous agitation.",
        "**Buffers or pH modifiers**: allow pesticides to be mixed with diluents or other pesticides of different acidity or alkalinity. Most pesticide solutions or suspensions are stable between **pH 5.5 and 7.0** (slightly acidic to neutral). Water outside this range may cause pesticides to degrade, very rapidly in some cases. If you use a buffer, **add it to the spray tank water first** and mix well. The water must be pH neutral or slightly acidic to start, **before** adding pesticides or other adjuvants.",
        "**Compatibility agents**: help combine pesticides (or pesticides and fertilizers) effectively; reduce or eliminate incompatibility.",
        "**Drift control additives (deposition aids)**: reduce drift; increase average droplet size and/or lower the number of \"fines\" (very small droplets) produced.",
        "**Emulsifiers**: allow petroleum-based pesticides (ECs) to mix with water.",
        "**Extenders**: keep pesticides active on a target for an extended period. Some adjuvant manufacturers use this name for stickers. (See \"Stickers\" below.)",
        "**Invert emulsifiers**: allow water-based pesticides to mix with petroleum carrier.",
        "**Plant penetrants**: allow the pesticide to pass through (penetrate) the outer surface to the inside of treated foliage. Certain plant penetrants may increase penetration on some, but not all, plant species.",
        "**Safeners**: reduce the toxicity of a pesticide formulation to the pesticide handler or to the treated surface.",
        "**Spreader**: allow pesticide to form a uniform coating layer over the treated surface.",
        "**Stickers**: allow pesticide to stay on a treated surface. Some types of stickers increase adhesion of solid particles to a treated surface. This reduces the amount of pesticide that washes off due to rain or irrigation. Others reduce evaporation and/or slow photodegradation. (See \"Extenders\" above.)",
        "**Surfactant**: see \"Surfactants\" below.",
        "**Thickeners**: increase viscosity (thickness) of spray mixtures. Thickeners may reduce drift and/or slow evaporation. (Slowing evaporation is useful when applying systemic pesticides. It increases the time during which the active ingredient can be absorbed by or penetrate plant foliage.)",
        "**Wetting agents**: allow wettable powders to mix with water."]},
    {"box": "Types of adjuvants (sidebar)", "list": [
        "Surfactants: wetting agents and spreaders.", "Stickers.", "Extenders.", "Plant penetrants.", "Compatibility agents.",
        "Buffers or pH modifiers.", "Drift retardants.", "Defoaming agents.", "Thickeners."]},
])
mc("Most pesticide solutions or suspensions are stable within what pH range?",
   ["pH 5.5 to 7.0", "pH 7.0 to 9.0", "pH 3.0 to 5.0", "pH 8.5 to 10.0"], 0, "p. 64, 'Types of Adjuvants'",
   "Most are stable between pH 5.5 and 7.0, slightly acidic to neutral.")
mc("Your well water is strongly alkaline. You plan to use a buffer. When do you add it?",
   ["To the spray tank water first, and mix well, before adding pesticides or other adjuvants", "After all the pesticides are in the tank",
    "Only after spraying, to clean the tank", "At the same time as the pesticide concentrate"], 0, "p. 64, 'Types of Adjuvants'",
   "Add the buffer to the water first so the water is neutral or slightly acidic before anything else goes in.", style="scenario")
mc("Which adjuvant allows wettable powders to mix with water?",
   ["Wetting agents", "Emulsifiers", "Invert emulsifiers", "Thickeners"], 0, "p. 64, 'Types of Adjuvants'",
   "Wetting agents let WPs mix with water; emulsifiers do this for ECs.")
mc("Which of these adjuvant descriptions is NOT correct?",
   ["Safeners reduce toxicity to the handler or the treated surface", "Drift control additives increase average droplet size",
    "Stickers help pesticide stay on a treated surface", "Antifoaming agents increase foaming in the tank"], 3,
   "p. 64, 'Types of Adjuvants'", "Antifoaming (defoaming) agents reduce foaming.", style="not")
mc("Which adjuvant increases the viscosity of a spray mixture and may reduce drift and slow evaporation?",
   ["Thickeners", "Spreaders", "Plant penetrants", "Compatibility agents"], 0, "p. 64, 'Types of Adjuvants'",
   "Thickeners increase viscosity, which may reduce drift and slow evaporation.")
mc("Which adjuvant allows petroleum-based pesticides (ECs) to mix with water?",
   ["Emulsifiers", "Invert emulsifiers", "Wetting agents", "Buffers"], 0, "p. 64, 'Types of Adjuvants'",
   "Emulsifiers mix ECs with water; invert emulsifiers mix water-based pesticides with petroleum carrier.")

# ---------------------------------------------------------------- pp. 64-65
card("Surfactants", [64, 65], [
    {"h": "Surfactants"},
    {"p": [
        "Some of the most common adjuvants are **surfactants** (**surf**ace **act**ive ingred**ients**), which alter the dispersing, spreading, and wetting properties of spray droplets.",
        "Examples of surfactants are **wetting agents and spreaders**.",
        "These products physically change the **surface tension** of a spray droplet.",
        "In order to perform well, some pesticide sprays must be able to wet treated foliage thoroughly and evenly.",
        "Surfactants that reduce surface tension enable droplets to **spread out instead of bead up**.",
        "This results in better coverage and increases the odds that the pest will contact the pesticide.",
        "Surfactants are particularly helpful when treating plants with **waxy or hairy leaves** (see Figure 4.1)."]},
    {"fig": "fig-4-1"},
    {"p": ["Surfactants are classified by how they split apart into charged atoms or molecules, called **ions**."]},
    {"list": [
        "**Anionic** surfactants have a **negative** charge. They are most often used with **contact pesticides**, which control the pest by direct contact instead of being absorbed systemically.",
        "**Cationic** surfactants have a **positive** charge. Do not use them as \"stand-alone\" surfactants: often, they are **phytotoxic**.",
        "**Nonionic** surfactants have **no electrical charge**. They are often used with **systemic** products and help sprays penetrate plant cuticles. They are compatible with most pesticide products."]},
    {"p": [
        "A pesticide can behave very differently in the presence of an anionic, cationic, or nonionic surfactant.",
        "For this reason, you must **follow label directions** when choosing one of these additives.",
        "Selecting the wrong surfactant can reduce efficacy and damage treated plants or surfaces."]},
    {"p": [
        "The terms used when talking about pesticide additives can be confusing.",
        "People sometimes use the words \"adjuvant\" and \"surfactant\" interchangeably.",
        "However, an adjuvant is **ANY substance** added to modify properties of a pesticide formulation or finished spray.",
        "A surfactant is a specific kind of adjuvant: one that affects the interaction of a spray droplet and a treated surface.",
        "**All surfactants are adjuvants, but not all adjuvants are surfactants.**",
        "For example, drift control additives and safeners are not surfactants."]},
], [{"id": "fig-4-1", "title": "Figure 4.1: Surfactants increase the ability of the pesticide to spread evenly over the surface of a leaf or fruit.",
     "page": "p. 65", "svgFile": "fig-4-1.svg",
     "explain": ["The figure shows a side view of a leaf.",
                 "Without surfactant, the spray droplets bead up on the leaf surface.",
                 "With surfactant, the droplets spread out into an even layer over the leaf."]}])
mc("Which kind of surfactant has no electrical charge, is often used with systemic products, and is compatible with most pesticide products?",
   ["Nonionic", "Anionic", "Cationic", "Ionic"], 0, "p. 65, 'Surfactants'",
   "Nonionic surfactants have no charge and help sprays penetrate plant cuticles.")
mc("Why should cationic surfactants not be used as stand-alone surfactants?",
   ["They are often phytotoxic", "They have no electrical charge", "They only work with fumigants", "They increase foaming"], 0,
   "p. 65, 'Surfactants'", "Cationic surfactants have a positive charge and are often phytotoxic.")
mc("Which of these is NOT a surfactant, according to the manual?",
   ["A wetting agent", "A spreader", "A drift control additive", "A nonionic surfactant"], 2, "p. 65, 'Surfactants'",
   "Drift control additives and safeners are adjuvants but not surfactants.", style="not")
mc("You are spraying a contact insecticide on plants with waxy leaves, and the spray beads up. Which surfactant type does the manual say is most often used with contact pesticides?",
   ["Anionic", "Cationic", "Nonionic", "None; contact pesticides never use surfactants"], 0, "p. 65, 'Surfactants'",
   "Anionic surfactants, with a negative charge, are most often used with contact pesticides; always follow the label.", style="scenario")
tf("All adjuvants are surfactants.", False, "p. 65, 'Surfactants'",
   "All surfactants are adjuvants, but not all adjuvants are surfactants.")
mc("How do surfactants that reduce surface tension improve coverage?",
   ["They let droplets spread out instead of bead up", "They make droplets larger so they fall faster",
    "They kill the pest directly", "They slow the release of the active ingredient"], 0, "p. 64, 'Surfactants'",
   "Spreading droplets give better coverage and raise the odds the pest contacts the pesticide.")

# ---------------------------------------------------------------- p. 65
card("Choosing the right adjuvant", [65, 65], [
    {"h": "Choosing the right adjuvant"},
    {"p": ["Here are some factors to consider when deciding whether to use an adjuvant and how to choose the right one for a particular site and situation."]},
    {"list": [
        "**Read and follow the label.** Is an adjuvant recommended? If so, what type? **Do not make substitutions.** Note that some product labels may recommend an adjuvant for one type of use or site but prohibit any kind of adjuvant for another labeled use or site. Many end-use formulated products already have adjuvants, and adding adjuvants \"on the fly\" can **decrease efficacy**. Suppose, for example, that a certain product is formulated with a wetting agent. If you add another wetting agent when you mix and load a foliar-applied spray, the product may not give better spreading and coverage. Instead, the extra adjuvant may increase runoff, reduce deposition, and even damage the target plant.",
        "Use only those adjuvants manufactured for **agricultural or horticultural uses**. Do not use industrial products or **household detergents** in pesticide spray mixes.",
        "Remember that **no adjuvant is a substitute for good application practices**.",
        "Take adjuvant performance claims \"with a grain of salt.\" Be skeptical of claims such as \"improves root uptake\" or \"keeps spray equipment clean\" unless a reliable source can provide **research-based evidence** to support them. Only use adjuvant products that have been tested and found effective for your intended use.",
        "**Test spray mixes with adjuvants on a small area** before proceeding with full-scale use."]},
])
mc("A product is already formulated with a wetting agent. A worker adds another wetting agent to the foliar spray. What does the manual say may happen?",
   ["Increased runoff, reduced deposition, and even damage to the target plant", "Twice the spreading and coverage",
    "Nothing, because adjuvants have no effect", "The pesticide turns into a fumigant"], 0, "p. 65, 'Choosing the Right Adjuvant'",
   "Adding adjuvants on the fly can decrease efficacy; the extra wetting agent may increase runoff and damage the plant.", style="scenario")
mc("Which of these is NOT acceptable according to the manual's adjuvant guidelines?",
   ["Reading the label to see if an adjuvant is recommended", "Using household detergent in a pesticide spray mix",
    "Testing a spray mix with adjuvant on a small area first", "Using adjuvants made for agricultural or horticultural uses"], 1,
   "p. 65, 'Choosing the Right Adjuvant'", "Do not use industrial products or household detergents in pesticide spray mixes.", style="not")
tf("A good adjuvant can make up for poor application practices.", False, "p. 65, 'Choosing the Right Adjuvant'",
   "No adjuvant is a substitute for good application practices.")
mc("An adjuvant ad claims it \"improves root uptake.\" What does the manual tell you to do?",
   ["Be skeptical unless a reliable source provides research-based evidence", "Trust it, because adjuvants are EPA registered",
    "Double the label rate to be safe", "Use it only on waxy leaves"], 0, "p. 65, 'Choosing the Right Adjuvant'",
   "Take performance claims with a grain of salt unless research-based evidence supports them.")

# ---------------------------------------------------------------- p. 66
card("Chapter 4 summary", [66, 66], [
    {"h": "Summary"},
    {"p": [
        "The ingredients of a formulated pesticide include both **active and inert** components.",
        "The active ingredient controls the pest.",
        "Inert ingredients include carriers or diluents and adjuvants.",
        "The type of formulation may be provided in the identifying information on the **front panel of the label**.",
        "(The **SDS** for a product will describe the formulation and also provide information about hazardous inert ingredients.)"]},
    {"p": [
        "Learn what formulations are available for the pesticide active ingredients you will use.",
        "To decide which formulation is best for a specific site and situation, you must know the properties, and be able to evaluate the pros and cons, of various formulation types.",
        "You must be familiar with formulation types and active ingredient properties in order to understand the characteristics of the products you use and apply them properly."]},
    {"p": [
        "Most end-use pesticide products contain adjuvants.",
        "Although adjuvants themselves lack any direct pesticidal activity, they are added to pesticide formulations to improve product performance.",
        "You should know when and how to use an adjuvant."]},
    {"p": [
        "In summary, you must consider several factors when choosing a pesticide formulation.",
        "These include the risks and benefits associated with the options available, the practicality of using a specific formulation in a particular site to control the target pest, and whether the formulated product will provide effective control.",
        "Understanding the properties of common formulations before choosing a pesticide will help you avoid problems and apply your product in an effective and efficient manner."]},
])
mc("Which document does the summary say will describe a product's formulation and give information about hazardous inert ingredients?",
   ["The Safety Data Sheet (SDS)", "The restricted-use permit", "The bill of sale", "The application record"], 0,
   "p. 66, 'Summary'", "The SDS describes the formulation and hazardous inert ingredients.")
mc("Where on the label may the type of formulation be provided?",
   ["In the identifying information on the front panel", "Only in the storage and disposal section",
    "In the first aid section", "It is never on the label"], 0, "p. 66, 'Summary'",
   "The formulation type may be in the identifying information on the front panel.")
mc("Which of these is NOT one of the inert components named in the summary?",
   ["Carriers", "Diluents", "Adjuvants", "The ingredient that controls the pest"], 3, "p. 66, 'Summary'",
   "The active ingredient controls the pest; inert ingredients include carriers or diluents and adjuvants.", style="not")
mc("You must choose between two formulations of the same active ingredient for a school lawn. Which set of factors does the summary say to weigh?",
   ["Risks and benefits of the options, practicality at the site, and whether it will give effective control",
    "Only the price per gallon", "Only the brand name", "Only how fast it can be applied"], 0, "p. 66, 'Summary'",
   "The summary lists risks and benefits, practicality at the site, and effective control.", style="scenario")

def merge(t1, t2, title):
    i = next(k for k, x in enumerate(sections) if x["title"] == t1)
    A, B = sections[i], sections[i + 1]
    assert B["title"] == t2
    A["title"] = title; A["pages"] = [A["pages"][0], B["pages"][1]]
    A["body"] += B["body"]; A["figures"] += B["figures"]; A["questions"] += B["questions"]
    del sections[i + 1]

merge("Ultra-low volume (ULV)", "Invert emulsions", "Ultra-low volume and invert emulsions")
merge("Pellets (P or PS)", "Wettable powders (WP or W)", "Pellets and wettable powders")
for n, x in enumerate(sections, 1):
    x["id"] = f"c04-s{n:02d}"
    for k, q in enumerate(x["questions"], 1):
        q["id"] = f"{x['id']}-t{k}"

# ---------------------------------------------------------------- p. 67 review questions (manual's order within each card)
# Answers taken from the chapter text; check against Appendix A when it arrives.
def rv(title, k, q, choices, ans, ref, why):
    x = next(c for c in sections if c["title"] == title)
    r = [i for i, y in enumerate(x["questions"]) if y["src"] == "review"]
    x["questions"].insert(len(r), {"id": f"{x['id']}-r{k}", "src": "review", "kind": "mc", "q": q, "choices": choices,
                                   "answer": ans, "ref": ref + f"; p. 67, Review question {k}", "why": why})

rv("Formulation abbreviations and Table 4.1", 1, "The name \"X-Pest 5G\" on a pesticide label indicates a:",
   ["Granular pesticide with 5% active ingredient.", "Granular pesticide with 5% inert ingredients.", "Gel pesticide with 5% active ingredient."], 0,
   "p. 51, 'Formulations: An Overview' and Table 4.1", "Numbers in a brand name can give percent active ingredient, and G means granules (GL is gel).")
rv("Solutions, suspensions, and emulsions", 2, "Which is the pesticide formulation process by which solid particles are dispersed in a liquid?",
   ["Emulsion.", "Solution.", "Suspension."], 2, "p. 50, 'Formulations: An Overview'",
   "A suspension is fine solid particles dispersed in a liquid; an emulsion is droplets of one liquid in another.")
rv("Solutions (S) and ready-to-use solutions", 3, "Which liquid pesticide formulation consists of a small amount of active ingredient (often 1% or less per unit volume)?",
   ["Microencapsulated (M).", "Ready-to-use (low-concentrate) solution (RTU).", "Ultra-low volume (ULV)."], 1,
   "p. 53, 'Ready-to-Use (RTU) Low-Concentrate Solutions'", "RTU low-concentrate solutions are often 1% or less active ingredient.")
rv("Ultra-low volume and invert emulsions", 4, "Which liquid pesticide formulation may approach 100% active ingredient?",
   ["Aerosol (A).", "Emulsifiable concentrate (EC).", "Ultra-low volume (ULV)."], 2, "p. 54, 'Ultra-Low Volume'",
   "ULV concentrates have almost 100% active ingredient.")
rv("Ultra-low volume and invert emulsions", 5, "Which is a disadvantage of both EC and ULV formulations?",
   ["Difficult to handle, transport, and store.", "Require constant agitation to keep in suspension.",
    "Solvents may cause rubber or plastic hoses, gaskets, pump parts, and other surfaces to deteriorate."], 2,
   "pp. 53–54, 'Emulsifiable Concentrates' and 'Ultra-Low Volume'",
   "Both list hose, gasket, and pump deterioration; both are easy to handle and need little agitation.")
rv("Water-dispersible granules and soluble powders", 6, "Which dry/solid formulation is mixed in water and reduces the risk of inhalation exposure during mixing and loading?",
   ["Soluble powder (SP).", "Water-dispersible granule (WDG) or dry flowable (DF).", "Wettable powder (WP)."], 1,
   "p. 59, 'Water-Dispersible Granules (WDG) or Dry Flowables (DF)'",
   "WDGs have larger, less dusty particles, so handler exposure is reduced; SPs and WPs keep the inhalation hazard.")
rv("Pellets and wettable powders", 7, "Which type of dry/solid pesticide formulation consists of particles that are the same weight and shape?",
   ["Bait.", "Granule.", "Pellet."], 2, "p. 58, 'Pellets (P or PS)'", "In pellet formulations, all particles are more or less the same weight and shape.")
rv("Microencapsulated pesticides (M)", 8, "Which is an advantage of microencapsulated materials?",
   ["Delayed or slow release of the active ingredient prolongs their effectiveness.", "Their pesticidal activity is independent of weather conditions.",
    "They usually require only short restricted-entry intervals."], 0, "pp. 61–62, 'Microencapsulated Pesticides (M)'",
   "Timed release prolongs effectiveness; release can be weather-dependent and some have long restricted-entry intervals.")
rv("Surfactants", 9, "Which type of adjuvant functions as a wetting agent and spreader (that is, physically altering the surface tension of spray droplets)?",
   ["Buffer.", "Extender.", "Surfactant."], 2, "p. 64, 'Surfactants'",
   "Surfactants, such as wetting agents and spreaders, change the surface tension of spray droplets.")
rv("Types of adjuvants", 10, "Which type of adjuvant increases the viscosity of spray mixtures?",
   ["Sticker.", "Extender.", "Thickener."], 2, "p. 64, 'Types of Adjuvants'", "Thickeners increase viscosity (thickness) of spray mixtures.")

out = {"chapter": CH, "pages": [49, 67], "sections": sections}
json.dump(out, open(sys.argv[1], "w"), ensure_ascii=False, indent=1)
print(len(sections), "cards", sum(len(s["questions"]) for s in sections), "questions")
