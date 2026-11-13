# Generates content/chapters/ch08.json. Run from the repo root: python3 tools/gen_ch08.py
import json
CH = "Chapter 8 · Transportation, Storage, and Security"
S = []
def card(n, title, pages, body, figures, questions):
    sid = f"c08-s{n:02d}"
    qs = []
    t = r = 0
    for q in questions:
        q = dict(q)
        if q["src"] == "review":
            r += 0; qid = f"{sid}-r{q.pop('rn')}"
        else:
            t += 1; qid = f"{sid}-t{t}"
        qs.append({"id": qid, **q})
    S.append({"id": sid, "chapter": CH, "title": title, "pages": pages, "body": body, "figures": figures, "questions": qs})
def img(id, title, page): return {"id": id, "title": title, "page": f"p. {page}", "imgFile": id + ".jpg"}
def mc(q, choices, answer, ref, why, style=None, src="test", rn=None, fixed=False):
    d = {"src": src, "kind": "mc"}
    if style: d["style"] = style
    if rn: d["rn"] = rn
    d.update({"q": q, "choices": choices, "answer": answer, "ref": ref, "why": why})
    if fixed: d["fixed"] = True
    return d
def tf(q, answer, ref, why, style=None):
    d = {"src": "test", "kind": "tf"}
    if style: d["style"] = style
    d.update({"q": q, "answer": answer, "ref": ref, "why": why}); return d
def sh(q, answer, accept, keys, ref, why, style=None):
    d = {"src": "test", "kind": "short"}
    if style: d["style"] = style
    d.update({"q": q, "answer": answer, "accept": accept})
    if keys: d["keys"] = keys
    d.update({"ref": ref, "why": why}); return d
def rv(n, q, choices, answer, ref, why):
    return mc(q, choices, answer, ref, why, src="review", rn=n)

# ---------- 1
card(1, "Chapter goals and transportation hazards", [123, 123], [
  {"box": "Learning objectives", "p": ["After studying this chapter, you should be able to do the following."], "list": [
    "State what precautions to take before transporting pesticides.",
    "Summarize what the label says about legally disposing of unwanted pesticides.",
    "List the steps to take to restrict access to pesticides.",
    "Explain how to create a safe and secure storage area.",
    "Describe how to properly store pesticides.",
    "Discuss how to reduce the amounts stored by controlling inventory.",
    "Explain how to maintain the integrity of pesticide containers."]},
  {"fig": "p123-danger"},
  {"p": ["This chapter discusses safety and security issues that may arise when pesticides are moved or stored.",
    "Serious accidents involving pesticides are **more likely to occur while they are in transit**.",
    "Securing pesticides in a vehicle or in storage is a critical step to **prevent vandalism or theft** of product.",
    "You can reduce pesticide transport and storage problems by being aware of conditions that lead to increased security risks."]},
  {"h": "Transportation"},
  {"p": ["Every pesticide applicator should understand the hazards of transporting pesticides and the procedures for minimizing those risks.",
    "Pesticides are moved by manufacturers to distributors, from retailers to end users, and from storage sites to job sites.",
    "Transportation-related accidents can happen at **any point in the distribution chain**, from the manufacturer to the job site.",
    "Your **first line of defense** is recognizing how to prevent these transportation mishaps.",
    "When accidents occur, the **timing of your response** could determine the size of the spill."]},
 ], [img("p123-danger", "Sign: Danger, Peligro. Fire will cause toxic fumes. Pesticide storage area. All unauthorized persons keep out. Keep door locked when not in use.", 123)], [
  mc("According to the manual, when are serious accidents involving pesticides more likely to occur?",
     ["While the pesticides are in storage", "While the pesticides are in transit", "While the pesticides are being mixed", "While the pesticides are being disposed of"], 1,
     "p. 123, chapter introduction", "Serious accidents are more likely to occur while pesticides are in transit."),
  mc("What does the manual call your first line of defense against transportation accidents?",
     ["Carrying a spill kit", "Calling first responders", "Recognizing how to prevent these transportation mishaps", "Buying vehicle insurance"], 2,
     "p. 123, 'Transportation'", "Your first line of defense is recognizing how to prevent these transportation mishaps."),
  mc("Which of these is NOT named as a point where pesticides are moved in the distribution chain?",
     ["Manufacturers to distributors", "Retailers to end users", "Storage sites to job sites", "Job sites back to manufacturers"], 3,
     "p. 123, 'Transportation'", "The manual names manufacturers to distributors, retailers to end users, and storage sites to job sites.", style="not"),
  mc("A tank of pesticide tips over on a truck. According to the manual, what could determine the size of the spill?",
     ["The timing of your response", "The brand of the pesticide", "The weather forecast", "The size of the truck"], 0,
     "p. 123, 'Transportation'", "When accidents occur, the timing of your response could determine the size of the spill.", style="scenario"),
  tf("Transportation-related accidents can happen only on public highways, not at other points in the distribution chain.", False,
     "p. 123, 'Transportation'", "They can happen at any point in the distribution chain, from the manufacturer to the job site."),
])

# ---------- 2
card(2, "The transport vehicle and securing the load", [124, 124], [
  {"fig": "p124-secure"},
  {"h": "Transport vehicle"},
  {"p": ["Transport vehicles should be in **good mechanical condition**.",
    "Make sure **brakes, tires, and steering** are in proper working order.",
    "Repair all fluid leaks before putting a truck on the road or leaving the job site.",
    "Regularly inspect application equipment to be transported and used.",
    "Inspect **hoses under pressure for wear and cracks** and **hose clamps for rust**.",
    "Always carry **supplies and replacement parts** to make emergency repairs if a leak should develop while going to and from the job site."]},
  {"p": ["**Never carry liquid pesticides in the passenger area**, because spilled chemicals may cause harmful fumes that can be inhaled.",
    "A pesticide spilled in the cab is difficult to remove and may lead to **long-term inhalation exposure**."]},
  {"fig": "p124-passenger"},
  {"p": ["It is best to keep pesticide containers in the **original shipping box**.",
    "Depending on the material, many of these boxes meet the **U.S. Department of Transportation (DOT)** packaging standards to give added protection to the contents.",
    "Try to carry a **minimum amount** of pesticide products on a vehicle at any one time."]},
  {"p": ["Secure and protect pesticide containers against **punctures and impacts** from items packed closely together.",
    "**Enclosed cargo boxes** provide extra security from curious children, thieves, or vandals.",
    "**Never stack pesticide containers higher than the sides of the vehicle.**",
    "Make sure flatbed trucks have **tie-down rings or racks** to simplify the job of securing the load."]},
  {"fig": "p124-cargo"},
 ], [img("p124-secure", "Secure pesticides while transporting them even for short distances.", 124),
     img("p124-passenger", "Never carry pesticides in the passenger compartment of a vehicle.", 124),
     img("p124-cargo", "Cargo boxes allow for secure transport of pesticides and help prevent theft and vandalism.", 124)], [
  rv(1, "Which statement about transporting pesticides is true?",
     ["Carry pesticides in the passenger compartment to prevent unauthorized access.", "Enclosed and lockable cargo boxes offer the greatest protection.", "The operator (driver) is not held responsible if a pesticide spill or accident occurs."], 1,
     "p. 124, 'Transport Vehicle' and 'Vehicle Operator'", "Enclosed cargo boxes provide extra security, pesticides never go in the passenger area, and the driver is accountable."),
  mc("Why does the manual say never to carry liquid pesticides in the passenger area?",
     ["The cab is too warm for pesticides", "Spilled chemicals may cause harmful fumes that can be inhaled", "It voids the vehicle warranty", "Labels fade in sunlight"], 1,
     "p. 124, 'Transport Vehicle'", "A spill in the cab can cause harmful fumes and long-term inhalation exposure."),
  mc("Which of these is NOT a transport vehicle check named in the manual?",
     ["Brakes, tires, and steering in proper working order", "Hoses under pressure inspected for wear and cracks", "Hose clamps inspected for rust", "Tire pressure set 10% above normal"], 3,
     "p. 124, 'Transport Vehicle'", "The manual lists brakes, tires, steering, fluid leaks, hoses, and hose clamps, nothing about extra tire pressure.", style="not"),
  mc("You are loading a pickup with jugs of pesticide. The stack would rise above the sides of the bed. What should you do?",
     ["Stack them anyway and drive slowly", "Do not stack them higher than the sides of the vehicle", "Put the extra jugs in the cab", "Cover the stack with a tarp"], 1,
     "p. 124, 'Transport Vehicle'", "Never stack pesticide containers higher than the sides of the vehicle.", style="scenario"),
  tf("It is best to move pesticide containers out of their original shipping boxes before transport.", False,
     "p. 124, 'Transport Vehicle'", "It is best to keep them in the original shipping box, which may meet DOT packaging standards."),
  sh("What should flatbed trucks have to simplify the job of securing the load?", "tie-down rings or racks", ["tie down rings", "racks", "tie-downs", "tie downs"],
     [["tie-down", "tie down", "tiedown", "rack", "racks", "rings"]],
     "p. 124, 'Transport Vehicle'", "Flatbed trucks should have tie-down rings or racks."),
])

# ---------- 3
card(3, "The vehicle operator and Safety Data Sheets", [124, 125], [
  {"h": "Vehicle operator"},
  {"p": ["The person driving the vehicle and/or the owner of the company is **accountable for injuries to people and any pesticide release** into the environment.",
    "The vehicle operator (driver) is the **first person who can contain the spill** and prevent it from spreading.",
    "By the time first responders arrive on the scene, the spill may already be contained.",
    "Therefore, it is important that the driver know **basic emergency response procedures** to contain the spill, **company guidelines**, and **who will notify local, state, and federal authorities**.",
    "Chapter 9, Emergency or Incident Response, explains in detail how to respond to a fire, spill, or leak involving pesticides."]},
  {"p": ["It should be noted that some drivers transporting pesticides regulated as **hazardous materials** will be required to follow **DOT regulations** regarding **commercial driver licenses, placarding, shipping papers, and annual inspections**."]},
  {"h": "Other safety precautions"},
  {"p": ["Always carry **product labels and Safety Data Sheets (SDSs)** when transporting pesticides on highways.",
    "The SDS contains critical information for the driver and emergency responders after a pesticide spill.",
    "It lists steps to safely deal with the spill, including the **personal protective equipment (PPE)** to use, whether the spill carries an **inhalation or explosion risk**, **decontamination procedures**, and **emergency telephone numbers**.",
    "Have the labels and SDSs well organized and **alphabetically arranged by product name** to allow quick access in the event of a spill."]},
 ], [], [
  mc("Who does the manual say is the first person who can contain a spill during transport?",
     ["The first responders", "The vehicle operator (driver)", "The state lead agency", "The pesticide manufacturer"], 1,
     "p. 124, 'Vehicle Operator'", "The driver is the first person who can contain the spill and prevent it from spreading."),
  mc("Which of these is NOT listed as SDS information that helps after a spill?",
     ["The PPE to use", "Whether the spill carries an inhalation or explosion risk", "Decontamination procedures", "The retail price of the product"], 3,
     "p. 125, 'Other Safety Precautions'", "The SDS lists PPE, inhalation or explosion risk, decontamination procedures, and emergency phone numbers.", style="not"),
  mc("A driver for a pest control company spills a pesticide on the highway. Who is accountable for injuries to people and the release into the environment?",
     ["Only the pesticide manufacturer", "Only the state highway department", "The driver and/or the owner of the company", "No one, if it was an accident"], 2,
     "p. 124, 'Vehicle Operator'", "The person driving and/or the owner of the company is accountable.", style="scenario"),
  mc("How should labels and SDSs carried in the vehicle be organized?",
     ["By purchase date", "Alphabetically by product name", "By signal word", "By EPA registration number"], 1,
     "p. 125, 'Other Safety Precautions'", "Have them well organized and alphabetically arranged by product name for quick access."),
  sh("Name two things DOT regulations cover for some drivers transporting pesticides regulated as hazardous materials.", "commercial driver licenses, placarding, shipping papers, and annual inspections",
     [], [["commercial driver", "cdl", "driver license", "drivers license", "placard", "placarding", "shipping papers", "annual inspection", "inspections"]],
     "p. 124, 'Vehicle Operator'", "DOT covers commercial driver licenses, placarding, shipping papers, and annual inspections."),
])

# ---------- 4
card(4, "Spill kits, container checks, and temperature in transit", [125, 125], [
  {"p": ["Always carry a **spill kit** with the items you will need to handle a spill during transport.",
    "The contents of a spill kit are discussed in Chapter 9."]},
  {"fig": "p125-spillkit"},
  {"p": ["Inspect containers to ensure they have **legible and attached labels**, **tight closures**, and **pesticide-free outside surfaces**.",
    "Secure application equipment, such as hand sprayers, backpack sprayers, and spreaders, during transport."]},
  {"p": ["Protect pesticides from **extreme temperature and moisture** during transit.",
    "Depending on the pesticide, **either extremely low or extremely high temperatures** can alter the stability of certain pesticide formulations."]},
  {"fig": "p125-feedseed"},
 ], [img("p125-spillkit", "Always secure the load and carry in the truck a spill kit that includes a broom and shovel.", 125),
     img("p125-feedseed", "Pesticides stored incorrectly with feed, seed, and fertilizers increase the risk of contaminating non-pesticide products.", 125)], [
  mc("Which of these is NOT something to check when inspecting containers before transport?",
     ["Legible and attached labels", "Tight closures", "Pesticide-free outside surfaces", "A purchase receipt taped to the lid"], 3,
     "p. 125, 'Other Safety Precautions'", "Check for legible and attached labels, tight closures, and pesticide-free outside surfaces.", style="not"),
  tf("Only extremely high temperatures, not low temperatures, can alter the stability of pesticide formulations.", False,
     "p. 125, 'Other Safety Precautions'", "Either extremely low or extremely high temperatures can alter stability, depending on the pesticide."),
  mc("You are hauling a backpack sprayer and a spreader to a job. What does the manual say to do with them?",
     ["Carry them in the cab", "Secure them during transport", "Fill them before leaving", "Leave them loose so they are easy to reach"], 1,
     "p. 125, 'Other Safety Precautions'", "Secure application equipment, such as hand sprayers, backpack sprayers, and spreaders, during transport.", style="scenario"),
  mc("According to the photo caption, what two tools should the truck's spill kit include?",
     ["A broom and shovel", "A rake and hose", "A bucket and mop", "A fire extinguisher and flashlight"], 0,
     "p. 125, photo caption", "The caption says to carry a spill kit that includes a broom and shovel."),
  mc("What risk does the manual say comes from storing pesticides incorrectly with feed, seed, and fertilizers?",
     ["The pesticides lose strength", "Contaminating non-pesticide products", "Attracting rodents", "Voiding the label"], 1,
     "p. 125, photo caption", "It increases the risk of contaminating non-pesticide products."),
])

# ---------- 5
card(5, "Vehicle placards and the transportation security plan", [125, 126], [
  {"h": "Vehicle placards"},
  {"p": ["DOT requires diamond-shaped signs called **placards** to be placed on vehicles that transport certain types and quantities of hazardous materials.",
    "Most **distributors** will give you any required placards to place on your transportation vehicle.",
    "Hazardous materials include some pesticides, fertilizers such as **anhydrous ammonia or ammonium nitrate**, and fuels such as **gasoline, diesel, and propane**.",
    "Placards provide emergency responders with the information necessary to **quickly assess an accident situation**."]},
  {"fig": "fig-8-placards"},
  {"p": ["If you ship or transport materials in quantities that require placards, you must develop and implement a **transportation security plan**.",
    "Vehicles must be placarded when transporting pesticides in any of these ways."]},
  {"list": ["Bearing a **DOT poison label**.", "In containers **larger than 119 gallons**.", "In quantities **greater than 1,000 pounds**."]},
  {"p": ["The security plan must include measures to **prevent unauthorized access**, a **security check of employees** who pick up and transport placarded hazardous materials, and the **intended route of travel**.",
    "For further details on the transportation security plan, contact the **Hazardous Materials Information Center**."]},
 ], [{"id": "fig-8-placards", "title": "Examples of placards placed on vehicles that transport certain types of hazardous materials.", "page": "p. 125",
      "svgFile": "fig-8-placards.svg",
      "explain": ["The six example placards are: Dangerous 4, Gasoline 3, Oxidizer 5.1, Poison 6, Inhalation Hazard 2, and Flammable 3.",
                  "Each one is a diamond-shaped sign with the hazard name and a number."]}], [
  mc("Vehicles must be placarded when transporting pesticides in containers larger than how many gallons?",
     ["55 gallons", "100 gallons", "119 gallons", "1,000 gallons"], 2,
     "p. 126, 'Vehicle Placards'", "Placards are required for containers larger than 119 gallons."),
  mc("Vehicles must be placarded when transporting pesticides in quantities greater than how many pounds?",
     ["119 pounds", "500 pounds", "1,000 pounds", "10,000 pounds"], 2,
     "p. 126, 'Vehicle Placards'", "Placards are required for quantities greater than 1,000 pounds."),
  mc("Which of these is NOT a required part of a transportation security plan?",
     ["Measures to prevent unauthorized access", "A security check of employees who transport placarded hazardous materials", "The intended route of travel", "A copy of each employee's driving record from the last 10 years"], 3,
     "p. 126, 'Vehicle Placards'", "The plan covers unauthorized access, employee security checks, and the intended route of travel.", style="not"),
  mc("You will haul 1,500 pounds of a pesticide. What must you develop and implement?",
     ["A pest management plan", "A transportation security plan", "A drift management plan", "A groundwater protection plan"], 1,
     "pp. 125–126, 'Vehicle Placards'", "Quantities that require placards also require a transportation security plan.", style="scenario"),
  mc("Who does the manual say will give you most required placards?",
     ["The state police", "Most distributors", "The EPA", "The local fire department"], 1,
     "p. 125, 'Vehicle Placards'", "Most distributors will give you any required placards."),
  tf("Placards give emergency responders the information they need to quickly assess an accident situation.", True,
     "p. 125, 'Vehicle Placards'", "That is the stated purpose of placards."),
])

# ---------- 6
card(6, "Storing pesticides in buildings and securing the site", [126, 126], [
  {"h": "Storage of pesticides in buildings"},
  {"p": ["Although existing buildings are often used for pesticide storage, it is best to have a **separate storage facility** for pesticides, fertilizers, and other similar products.",
    "Storing pesticides separately gives emergency response crews **more options in dealing with fires and spills**.",
    "Keeping **equipment, employees, and records away from pesticides** is always recommended where possible."]},
  {"fig": "p126-shed"},
  {"p": ["A well-designed pesticide storage site does the following."]},
  {"list": ["**Limits access.**", "Permits better **inventory control**.", "Protects people from exposure.", "Reduces the chance of environmental contamination.",
    "Prevents damage to pesticides from **temperature extremes and excess moisture**.", "Safeguards pesticides from **theft, vandalism, and unauthorized use**.",
    "Allows **fire departments to know the location** of products."]},
  {"h": "Secure the site"},
  {"p": ["Whether the designated storage area is a **cabinet, an entire room, or a separate building**, **keep it locked when not in use**.",
    "**Post warning signs on doors and windows** to alert others that pesticides are stored inside.",
    "Pesticide security is covered in detail later in this chapter."]},
 ], [img("p126-shed", "Maintain a well designed, secure pesticide storage facility with highly visible warning signs. Keep it well ventilated and located where water damage is not likely to occur.", 126)], [
  mc("Why does the manual say it is best to store pesticides in a separate facility?",
     ["It lowers property taxes", "It gives emergency response crews more options in dealing with fires and spills", "It keeps pesticides warmer", "It is required for all private applicators"], 1,
     "p. 126, 'Storage of Pesticides in Buildings'", "Separate storage gives emergency crews more options with fires and spills."),
  mc("Which of these is NOT listed as something a well-designed storage site does?",
     ["Limits access", "Permits better inventory control", "Allows fire departments to know the location of products", "Speeds up the breakdown of old pesticides"], 3,
     "p. 126, 'Storage of Pesticides in Buildings'", "The list includes limiting access, inventory control, and letting fire departments know where products are.", style="not"),
  mc("Your company stores pesticides in a single locked cabinet, not a building. What does the manual say about securing it?",
     ["A cabinet does not need to be locked", "Keep it locked when not in use and post warning signs", "Only rooms and buildings need signs", "Lock it only at night"], 1,
     "p. 126, 'Secure the Site'", "Whether a cabinet, room, or building, keep it locked when not in use and post warning signs.", style="scenario"),
  sh("Where does the manual say to post warning signs at a pesticide storage site?", "on doors and windows", ["doors and windows"],
     [["door", "doors"], ["window", "windows"]],
     "p. 126, 'Secure the Site'", "Post warning signs on doors and windows."),
  tf("The manual recommends keeping equipment, employees, and records away from pesticides where possible.", True,
     "p. 126, 'Storage of Pesticides in Buildings'", "That is always recommended where possible."),
])

# ---------- 7
card(7, "Preventing water damage", [126, 126], [
  {"h": "Prevent water damage"},
  {"p": ["Pesticide storage facilities should **not be located in a flood zone**.",
    "Carefully consider **soil and land surface characteristics** when selecting a storage site to prevent contamination of surface water or groundwater.",
    "Do not locate the storage facility **near a stream likely to flood** or where **runoff water flows toward the facility**.",
    "If flooding is likely, consider **building dikes** around the storage facility.",
    "Work with local **zoning and building code professionals** to determine how best to protect the environment if high water were to enter the storage facility."]},
  {"p": ["Consider storing pesticides on a **raised pallet or on shelves** to prevent high water from damaging pesticide containers or flowing water from moving them offsite."]},
  {"fig": "p126-damp"},
  {"p": ["Water or excess moisture may damage pesticide containers and their contents and cause the following."]},
  {"list": ["**Metal containers to rust.**", "**Paper and cardboard containers to split or crumble.**", "Pesticide labeling to peel, smear, or otherwise become unreadable.",
    "Dry pesticides to clump, degrade, or dissolve.", "Slow-release products to release their active ingredients."]},
 ], [img("p126-damp", "Do not store pesticides in locations that can become damp or wet.", 126)], [
  rv(2, "Which statement about pesticide storage facilities is true?",
     ["A ventilation system may reduce noxious vapors by venting air into an adjoining area.", "Carefully consider the terrain when selecting a storage site.", "The floor should remain as bare soil to absorb any spilled material."], 1,
     "p. 126, 'Prevent Water Damage'", "Consider soil and land surface characteristics. Venting to an adjoining room does little, and floors should be impervious."),
  mc("Which of these is NOT listed as damage that water or excess moisture may cause?",
     ["Metal containers to rust", "Dry pesticides to clump, degrade, or dissolve", "Slow-release products to release their active ingredients", "Liquid pesticides to freeze solid"], 3,
     "p. 126, 'Prevent Water Damage'", "Freezing is not on the moisture list.", style="not"),
  mc("A farm's best spot for a new pesticide shed sits where runoff water flows toward it. What does the manual say?",
     ["Build there, but raise the door", "Do not locate the storage facility where runoff water flows toward it", "Build there if the floor is soil", "Build there if it is near a stream"], 1,
     "p. 126, 'Prevent Water Damage'", "Do not locate it near a stream likely to flood or where runoff flows toward it.", style="scenario"),
  mc("If flooding is likely at a storage site, what does the manual say to consider building?",
     ["A second floor", "Dikes around the storage facility", "A sump pump", "A drainage ditch to the nearest stream"], 1,
     "p. 126, 'Prevent Water Damage'", "If flooding is likely, consider building dikes around the facility."),
  tf("Storing pesticides on raised pallets or shelves helps keep high water from damaging containers.", True,
     "p. 126, 'Prevent Water Damage'", "Raised pallets or shelves keep high water from damaging or moving containers."),
])

# ---------- 8
card(8, "Temperature, ventilation, lighting, and floors", [126, 127], [
  {"h": "Control the temperature"},
  {"p": ["Choose a **well-ventilated room where temperatures are controlled**.",
    "**Exhaust fans directed to the outside** of the building reduce the buildup of noxious vapors from many of the solvents used in pesticide formulations.",
    "**Ventilating the pesticide storage room into an adjoining room does little to solve the problem.**",
    "Pesticide labeling often gives **temperature limits** for storing a product."]},
  {"p": ["Consider installing an exhaust fan **on a timer** to automatically turn on at a certain temperature.",
    "If the exhaust fan is not on a timer, **turn on the fan switch before entering** the storage room.",
    "**Wait a few minutes** to allow any vapors to clear."]},
  {"h": "Provide adequate lighting"},
  {"p": ["Be sure the pesticide storage facility is **well-lighted**.",
    "Pesticide handlers entering the building must be able to **read the product labels** and determine whether **containers are leaking**."]},
  {"h": "Use nonporous materials"},
  {"p": ["Use **cement or other impervious materials** for flooring to retain the spilled material on the surface.",
    "Such surfaces are easy to clean and decontaminate in the event of a release.",
    "A floor that **slopes into a sump** helps collect and contain the spill.",
    "Consider using shelving and pallets made of **nonabsorbent materials, such as plastic or metal**, for the same reasons as impervious floors."]},
  {"fig": "p127-floor"},
 ], [img("p127-floor", "Be sure the floor of the pesticide containment site is made of non-porous materials such as sealed cement. A recessed floor helps control spills or leaking pesticides.", 127)], [
  mc("Where should exhaust fans in a pesticide storage room be directed?",
     ["Into an adjoining room", "To the outside of the building", "Toward the floor", "Into the office"], 1,
     "p. 126, 'Control the Temperature'", "Fans directed to the outside reduce noxious vapor buildup. An adjoining room does little."),
  mc("The storage room's exhaust fan is not on a timer. What should you do before going in?",
     ["Open a window after you are inside", "Turn on the fan switch before entering, then wait a few minutes for vapors to clear", "Hold your breath and work quickly", "Spray air freshener"], 1,
     "p. 127, 'Control the Temperature'", "Turn on the fan before entering and wait a few minutes for vapors to clear.", style="scenario"),
  mc("Which of these is NOT a recommended material for a storage floor or shelving?",
     ["Sealed cement", "Plastic shelving", "Metal shelving", "Wood shelving"], 3,
     "p. 127, 'Use Nonporous Materials'", "Use impervious floors and nonabsorbent shelving such as plastic or metal. Wood absorbs spills.", style="not"),
  sh("What two things must pesticide handlers be able to do because the storage facility is well-lighted?", "read the product labels and see whether containers are leaking", [],
     [["label", "labels"], ["leak", "leaking", "leaks"]],
     "p. 127, 'Provide Adequate Lighting'", "Handlers must be able to read labels and determine whether containers are leaking."),
  tf("A floor that slopes into a sump helps collect and contain a spill.", True,
     "p. 127, 'Use Nonporous Materials'", "A floor sloping into a sump helps collect and contain the spill."),
])

# ---------- 9
card(9, "What belongs in storage and keeping labels legible", [127, 127], [
  {"h": "Maintain the storage site"},
  {"p": ["Store **only pesticide containers, pesticide equipment, and a spill cleanup kit** at the storage site.",
    "Keep **food, drink, tobacco, feed, medication, medical or veterinary supplies, seed (treated and untreated), clothing, and PPE** (other than that necessary for emergency response) out of the storage location."]},
  {"h": "Keep labels legible"},
  {"p": ["Store pesticide containers with the **labels in plain sight**.",
    "Costly errors may result if the wrong pesticide is chosen.",
    "Be sure labels are always legible.",
    "If the label is destroyed or damaged, **immediately mark the container** with some basic labeling information, such as the **trade name, the U.S. Environmental Protection Agency (EPA) registration number, signal word, and use classification**.",
    "Go online to find a product replacement label or get a **new label from the manufacturer**."]},
 ], [], [
  mc("Which of these does the manual say SHOULD be stored at the pesticide storage site?",
     ["Treated seed", "A spill cleanup kit", "Livestock feed", "Everyday work clothing"], 1,
     "p. 127, 'Maintain the Storage Site'", "Store only pesticide containers, pesticide equipment, and a spill cleanup kit."),
  mc("Which of these is NOT allowed at the storage site, according to the manual?",
     ["Pesticide containers", "Pesticide equipment", "Untreated seed", "A spill cleanup kit"], 2,
     "p. 127, 'Maintain the Storage Site'", "Seed, treated and untreated, stays out of the storage location.", style="not"),
  mc("A label on a jug in storage has torn off and is unreadable. What should you do first?",
     ["Throw the jug away", "Immediately mark the container with basic labeling information such as trade name, EPA registration number, signal word, and use classification", "Pour it into a labeled container of a similar product", "Use it up quickly"], 1,
     "p. 127, 'Keep Labels Legible'", "Immediately mark the container with basic labeling information, then get a replacement label.", style="scenario"),
  tf("PPE needed for emergency response may be kept at the storage site.", True,
     "p. 127, 'Maintain the Storage Site'", "PPE stays out except that necessary for emergency response."),
  sh("Name two places the manual says you can get a replacement label for a damaged one.", "online, or from the manufacturer", ["online and the manufacturer"],
     [["online", "internet", "web", "website"], ["manufacturer", "maker", "company"]],
     "p. 127, 'Keep Labels Legible'", "Go online to find a replacement label or get a new label from the manufacturer."),
])

# ---------- 10
card(10, "Storing pesticide containers safely", [127, 128], [
  {"h": "Store pesticide containers safely"},
  {"p": ["Store pesticides in their **original containers** or, if allowed by state law, in a **properly labeled service container**.",
    "Never use any other container to store a product.",
    "Besides being illegal, serious injury may result when using **food containers, such as milk jugs or soft drink bottles**.",
    "Children will associate the shape, size, and color of the container with its usual contents.",
    "Never use a pesticide product from an unmarked or unlabeled container unless you are certain what it is.",
    "Guessing wrong can cause serious damage at the application site."]},
  {"fig": "p127-foodjars"},
  {"p": ["Keep pesticide containers **securely closed** when not in use.",
    "Just like bagged fertilizer, **dry pesticide formulations can clump** together under high humidity.",
    "Consider placing partially used bags of wettable and soluble powders, dry flowables, dusts, and granules in a **plastic trash bag or tub with a cover** to reduce clumping."]},
  {"p": ["Place **drums and bags on plastic pallets**.",
    "Store other pesticides on **metal shelving**, placing the **heaviest containers on lower shelves**.",
    "Do not allow containers to **extend beyond the edge of the shelving**. They could be knocked off or torn open."]},
  {"fig": "p127-shelving"},
  {"p": ["Place **bulk and mini-bulk tanks on a reinforced concrete pad**.",
    "**Diking** around bulk tanks keeps leaking pesticides inside a contained area.",
    "Make the area inside a dike large enough to contain **the volume of the liquid in the tank plus at least an additional 10%**.",
    "Keep **valves and pumps as well as transfer hoses within the diked area** when not in use.",
    "Contact your state, tribe, or territory pesticide regulatory agency for guidance on what constitutes bulk pesticides and to learn specific rules for building containment structures."]},
 ], [img("p127-foodjars", "Do not store pesticides in food containers.", 127),
     img("p127-shelving", "Store pesticides on metal shelving, with the heaviest containers and liquids stored on the lower shelves. Never extend beyond the edge of the shelving.", 127)], [
  mc("How large should the area inside a dike around a bulk tank be?",
     ["Equal to the volume of the liquid in the tank", "The volume of the liquid in the tank plus at least an additional 10%", "Twice the volume of the tank", "The volume of the tank plus 119 gallons"], 1,
     "pp. 127–128, 'Store Pesticide Containers Safely'", "The dike must hold the tank's liquid volume plus at least an additional 10%."),
  mc("A coworker pours leftover insecticide into an empty soft drink bottle to store it. What does the manual say?",
     ["That is fine if the cap is tight", "It is illegal and can cause serious injury, because people associate the container with its usual contents", "It is fine if the bottle is stored up high", "It is fine for less than a week"], 1,
     "p. 127, 'Store Pesticide Containers Safely'", "Using food containers is illegal and may cause serious injury.", style="scenario"),
  mc("Which of these is NOT a correct storage practice from the manual?",
     ["Place drums and bags on plastic pallets", "Place the heaviest containers on lower shelves", "Let containers extend past the shelf edge to save space", "Place bulk tanks on a reinforced concrete pad"], 2,
     "p. 127, 'Store Pesticide Containers Safely'", "Containers must not extend beyond the shelf edge, where they could be knocked off or torn open.", style="not"),
  tf("Valves, pumps, and transfer hoses for a bulk tank should be kept within the diked area when not in use.", True,
     "p. 128, 'Store Pesticide Containers Safely'", "Keep valves, pumps, and transfer hoses within the diked area when not in use."),
  sh("What does the manual suggest putting partially used bags of dry formulations in to reduce clumping?", "a plastic trash bag or tub with a cover", ["plastic bag", "covered tub", "trash bag"],
     [["bag", "tub", "bin"]],
     "p. 127, 'Store Pesticide Containers Safely'", "A plastic trash bag or tub with a cover reduces clumping."),
])

# ---------- 11
card(11, "Damaged containers, shelf life, and safety tips", [128, 128], [
  {"h": "Look for damage"},
  {"p": ["Regularly inspect pesticide containers to detect problems at the outset.",
    "If you find a damaged container, **put on appropriate PPE** and **place it into a larger container, such as a 5-gallon bucket**.",
    "Clean up spilled pesticide and place any contaminated materials in the bucket.",
    "If possible, **use the pesticide immediately** on a site and at a rate allowed by the label, or **dispose of it according to label directions**."]},
  {"fig": "p128-damaged"},
  {"h": "Note shelf life of pesticides"},
  {"p": ["Keep an **inventory** of all pesticides in storage, **marking each container or box with the year it was purchased**.",
    "In this way, you can **use the oldest product first**.",
    "Remember to use it as it was meant to be used. A replacement product may have different label directions and uses.",
    "If you have questions about the shelf life of a product, contact the **dealer or manufacturer**.",
    "Avoid storing large quantities of pesticides for long periods. **Buy only as much as you need for the season.**"]},
  {"fig": "p128-dates"},
  {"box": "Follow these safety tips", "p": ["For best results, do the following."], "list": [
    "Have **duplicate copies of pesticide labels and SDSs** available in case of an emergency.",
    "Wear appropriate protective clothing when handling pesticide containers.",
    "**Label items such as measuring utensils and protective equipment** to prevent their use for other purposes.",
    "Have **absorbent materials** readily available to soak up leaks in the storage room. Keep a **shovel, broom, and heavy-duty plastic bags** on hand to remove the contaminated absorbent material.",
    "Check the **SDS** for materials that will **deactivate a contaminated surface**. When in doubt, contact the pesticide manufacturer for a recommendation."]},
  {"p": ["Have readily accessible **clean water for decontamination, an eyewash station, personal protective equipment, a fire extinguisher rated for chemical fires, first aid equipment, and emergency telephone numbers**.",
    "Additionally, keep plenty of **soap, water, and paper towels** available near the storage facility."]},
 ], [img("p128-damaged", "Place damaged pesticide containers in secondary containment.", 128),
     img("p128-dates", "Mark each container with its purchase date.", 128)], [
  rv(3, "What is the first thing to do if a pesticide container is leaking?",
     ["Put on personal protective equipment.", "Transfer contents into another container.", "Clean up any spilled material."], 0,
     "p. 128, 'Look for Damage'", "If you find a damaged container, put on appropriate PPE first."),
  rv(4, "Which recommended practice will minimize pesticide storage problems?",
     ["Purchase quantities based on previous usage.", "Purchase more than you need to ensure availability of the product.", "Store metal pesticide containers on the higher shelves to prevent rusting."], 0,
     "p. 128, 'Note Shelf Life of Pesticides'", "Buy only as much as you need for the season. Heaviest containers go on lower shelves."),
  mc("Why should you mark each container or box with the year it was purchased?",
     ["So you can use the oldest product first", "Because the EPA requires it", "So you can return it for a refund", "So the fire department knows its age"], 0,
     "p. 128, 'Note Shelf Life of Pesticides'", "Marking the purchase year lets you use the oldest product first."),
  mc("Which of these is NOT on the manual's list of things to keep readily accessible near pesticide storage?",
     ["An eyewash station", "A fire extinguisher rated for chemical fires", "Emergency telephone numbers", "A garden hose connected to a storm drain"], 3,
     "p. 128, 'Follow These Safety Tips'", "The list includes clean water, an eyewash station, PPE, a chemical-rated extinguisher, first aid, and emergency numbers.", style="not"),
  mc("You find a cracked jug in storage and have put on PPE. What do you do with the jug?",
     ["Place it into a larger container, such as a 5-gallon bucket", "Pour it down the floor drain", "Tape the crack and put it back", "Leave it for the next inspection"], 0,
     "p. 128, 'Look for Damage'", "Place it into a larger container, such as a 5-gallon bucket, and clean up the spill.", style="scenario"),
  sh("Where should you check to find materials that will deactivate a contaminated surface?", "the SDS", ["safety data sheet", "the safety data sheet", "SDS"],
     None, "p. 128, 'Follow These Safety Tips'", "Check the SDS. When in doubt, contact the manufacturer."),
])

# ---------- 12
card(12, "Unwanted, waste, and canceled products", [128, 129], [
  {"h": "Isolate unwanted or waste products"},
  {"p": ["**Do not accumulate outdated or unwanted pesticide products.**",
    "Not only will you lose money by not using the product, but you may have to **pay a disposal service**.",
    "If you **use the product up according to the label**, you will avoid both problems."]},
  {"p": ["Sometimes **EPA will cancel a product registration**.",
    "When this occurs, EPA usually either **allows the continued use of the product until it has cleared the distribution chain** or **issues a federal notice prohibiting use after a specific date**.",
    "If you keep such products after that date, you may have to **dispose of them as hazardous waste**.",
    "Be sure to **follow label directions for disposal** of any excess or leftover product."]},
  {"p": ["If you are holding pesticides or emptied pesticide containers for disposal or recycling, keep them in a **special section of the storage area**.",
    "See Chapter 10 (Planning the Pesticide Application) for information on pesticide container rinsing procedures."]},
  {"fig": "p129-rinsed"},
  {"p": ["Some states sponsor **pesticide disposal programs** that collect unwanted pesticides from growers and applicators **free or at reduced cost**.",
    "Contact your state, tribe, or territory pesticide regulatory agency to see if a program is available in your area."]},
 ], [img("p129-rinsed", "Have a designated area for properly rinsed containers.", 129)], [
  mc("When EPA cancels a product registration, what does EPA usually do?",
     ["Orders all stocks destroyed within 24 hours", "Either allows use until the product clears the distribution chain or issues a federal notice prohibiting use after a specific date", "Refunds the purchase price", "Lets applicators use it forever"], 1,
     "p. 128, 'Isolate Unwanted or Waste Products'", "EPA usually allows use until the product clears the distribution chain, or bans use after a specific date."),
  mc("You still have a canceled pesticide after EPA's prohibition date. What may you have to do?",
     ["Return it to EPA", "Dispose of it as hazardous waste", "Sell it to another applicator", "Dilute it and pour it out"], 1,
     "p. 128, 'Isolate Unwanted or Waste Products'", "Products kept past that date may have to be disposed of as hazardous waste.", style="scenario"),
  mc("Which of these is NOT a reason the manual gives for avoiding a buildup of unwanted pesticides?",
     ["You lose money by not using the product", "You may have to pay a disposal service", "Old pesticides become more toxic every year", "Using it up according to the label avoids both problems"], 2,
     "p. 128, 'Isolate Unwanted or Waste Products'", "The manual cites lost money and disposal costs, not rising toxicity.", style="not"),
  tf("Pesticides and empty containers held for disposal or recycling should be kept in a special section of the storage area.", True,
     "p. 129, 'Isolate Unwanted or Waste Products'", "Keep them in a special section of the storage area."),
  sh("Who should you contact to learn whether a pesticide disposal program is available in your area?", "your state, tribe, or territory pesticide regulatory agency",
     ["state pesticide regulatory agency", "state agency", "state lead agency"],
     [["state", "tribe", "territory", "regulatory agency"]],
     "p. 129, 'Isolate Unwanted or Waste Products'", "Contact your state, tribe, or territory pesticide regulatory agency."),
])

# ---------- 13
card(13, "Pesticide site security and risk assessment", [129, 130], [
  {"h": "Pesticide site security"},
  {"p": ["Minimizing risks for the safety of employees, customers, and communities should always be a top priority when it comes to storing pesticides.",
    "Every pesticide storage facility should examine its security efforts and **plan for worst-case scenarios**.",
    "Routinely review your security measures to determine whether all risks have been accounted for in the plan.",
    "Without effective security procedures, you may be vulnerable to both **internal (employee theft)** and **external (terrorism, theft, and vandalism)** threats.",
    "This puts both employees and the community at risk."]},
  {"h": "Benefits of security efforts"},
  {"p": ["By developing a strong and workable security plan, managers, employees, and emergency responders can reduce the likelihood of theft or other mishaps.",
    "In addition, effective security avoids costly losses.",
    "An incident of any magnitude can seriously disrupt operations and result in lawsuits, costly remediation actions, employee fear and uncertainty, and damage to the company's reputation.",
    "A well-planned security program can do the following."]},
  {"list": ["Safeguard employees and the community.", "Maintain the integrity of operations.", "**Reduce insurance costs.**", "Prevent theft.", "Reduce vandalism and sabotage.",
    "Protect confidential business information.", "Improve relationships with local authorities and community leaders."]},
  {"h": "Risk assessment"},
  {"p": ["**The first step in developing a security program is to conduct a risk assessment** of your business or farm's vulnerabilities.",
    "Make a list of **assets that need protecting, possible threats, and steps** that can be taken to protect them.",
    "Any place that stores or transports pesticides shares similar assets, which are broadly defined as **people, information, and property**.",
    "\"People\" includes employees, visitors, customers, contractors, and neighbors.",
    "\"Information\" includes business, proprietary, and employee material deemed confidential.",
    "\"Property\" may include the following."]},
  {"list": ["Pesticide storage facilities.", "Vehicles.", "Application equipment.", "Bulk storage tanks.", "Mixing and loading sites.",
    "All utilities, such as telephone, water, gas, and electric."]},
  {"fig": "p129-visitors"},
 ], [img("p129-visitors", "Be sure to guard against unauthorized entry.", 129)], [
  rv(5, "What is the first step a business should take to develop an effective pesticide security program?",
     ["Coordinate planned actions with authorities.", "Conduct a risk assessment of business vulnerabilities.", "Train employees on security measures."], 1,
     "p. 129, 'Risk Assessment'", "The first step in developing a security program is a risk assessment."),
  mc("The manual broadly defines the assets of any place that stores or transports pesticides as which three things?",
     ["People, information, and property", "Money, equipment, and buildings", "Employees, customers, and vehicles", "Pesticides, records, and land"], 0,
     "p. 129, 'Risk Assessment'", "Assets are broadly defined as people, information, and property."),
  mc("Which of these is NOT listed as a benefit of a well-planned security program?",
     ["Reduce insurance costs", "Prevent theft", "Protect confidential business information", "Eliminate the need for a pesticide license"], 3,
     "p. 129, 'Benefits of Security Efforts'", "Security does not replace licensing. The other three are on the list.", style="not"),
  mc("An employee steals pesticides from the storage building. What kind of threat is this, according to the manual?",
     ["An external threat", "An internal threat", "A regulatory threat", "An environmental threat"], 1,
     "p. 129, 'Pesticide Site Security'", "Internal threats are employee theft. External threats are terrorism, theft, and vandalism.", style="scenario"),
  tf("Under the manual's definition, neighbors count as part of the \"people\" asset.", True,
     "p. 129, 'Risk Assessment'", "People includes employees, visitors, customers, contractors, and neighbors."),
])

# ---------- 14
card(14, "Employee training and evaluating security", [130, 130], [
  {"h": "Employee training and security awareness"},
  {"p": ["Train employees to be **vigilant in detecting security threats**.",
    "Employees are familiar with what occurs in and around a pesticide storage facility or at the job site.",
    "They can provide an **early warning** when something seems out of place or someone is acting suspiciously.",
    "At a minimum, instruct all employees on **pesticide inventory control, security of storage facilities and application equipment, and emergency preparedness and response**."]},
  {"h": "Evaluating pesticide security"},
  {"p": ["Fundamental security tasks include the following."]},
  {"p": ["**Secure buildings, manufacturing facilities, storage areas, and surrounding property.**",
    "Prevent the unauthorized entry of persons into areas used to manufacture or store pesticides.",
    "Elements of an effective security plan may range from **log sheets, identification badges, fencing, lighting, and locks** to **detection systems, cameras, and trained guards**."]},
  {"fig": "p130-lights"},
  {"p": ["**Secure pesticide application equipment and vehicles.**",
    "Keep unauthorized people away from equipment used for storing, mixing, loading, transferring, transporting, and applying pesticides.",
    "Secure and disable equipment in the field to prevent misuse.",
    "For example, **do not leave keys in the ignition**, and lock doors and cabinets.",
    "**Reclaim keys from employees when they terminate employment.**"]},
  {"fig": "p130-sprayers"},
 ], [img("p130-lights", "Outside lights on a pesticide storage building help prevent theft and vandalism.", 130),
     img("p130-sprayers", "Lock backpack sprayers securely onto the transport vehicle.", 130)], [
  rv(6, "Which of the following is considered a good security practice?",
     ["Instruct employees on pesticide inventory control.", "Allow employees access to inventory.", "Back up confidential data daily and keep it at the facility."], 0,
     "p. 130, 'Employee Training and Security Awareness'", "At a minimum, instruct all employees on pesticide inventory control."),
  mc("Which of these is NOT one of the minimum topics to instruct all employees on?",
     ["Pesticide inventory control", "Security of storage facilities and application equipment", "Emergency preparedness and response", "Pesticide sales techniques"], 3,
     "p. 130, 'Employee Training and Security Awareness'", "The minimum topics are inventory control, security, and emergency preparedness and response.", style="not"),
  mc("An employee quits your company. What does the manual say to do?",
     ["Reclaim keys from the employee", "Change the pesticide labels", "Move all pesticides to a new building", "Nothing, if they left on good terms"], 0,
     "p. 130, 'Evaluating Pesticide Security'", "Reclaim keys from employees when they terminate employment.", style="scenario"),
  mc("According to the photo caption, what do outside lights on a pesticide storage building help prevent?",
     ["Fires and spills", "Theft and vandalism", "Temperature extremes", "Flooding"], 1,
     "p. 130, photo caption", "Outside lights help prevent theft and vandalism."),
  tf("Leaving keys in the ignition of field equipment is acceptable if the field is fenced.", False,
     "p. 130, 'Evaluating Pesticide Security'", "Do not leave keys in the ignition. Secure and disable equipment in the field."),
])

# ---------- 15
card(15, "Security procedures, authorities, and prevention steps", [130, 131], [
  {"p": ["**Protect confidential information.**",
    "As safety and security systems become more reliant on computers and other technology, it is important to secure them from hackers and intruders.",
    "Such efforts include **contingency planning for power disruptions, adherence to password and backup procedures**, and other measures to ensure that only authorized personnel have access."]},
  {"p": ["**Develop procedures and policies that support security needs.**",
    "Recommended practices include effective **hiring and labor policies, inventory management, and planning for emergencies**.",
    "Hiring and labor policies should include **employee training, background checks, and workplace violence prevention**.",
    "Inventory management is necessary to keep track of pesticides stored at the facility.",
    "Planning for emergency response is critical. It helps to ensure that managers and employees know how to respond in the unlikely event of pesticide release, bomb threat, or terrorist activity."]},
  {"p": ["**Coordinate with authorities in a timely manner.**",
    "If you believe a security breach or suspicious activity has occurred, **contact local authorities immediately**.",
    "In addition to alerting the police department, call the **local emergency planning commission, fire departments**, and other emergency response agencies.",
    "The **Federal Bureau of Investigation (FBI)** cautions that any suspicious activity related to the use, training, or acquisition of pesticides should be immediately reported to management and local authorities."]},
  {"box": "Steps to prevent security problems", "p": ["To minimize risks, do the following."], "list": [
    "Adopt security measures to deter tampering with chemicals, equipment, or the facility itself.",
    "Include local authorities, for example police and firefighters, in developing the security plan.",
    "Keep an accurate inventory of all chemicals.",
    "Keep chemical storage areas locked when not in use.",
    "Update your emergency response plan and practice the procedures.",
    "Post telephone numbers of law enforcement and emergency response agencies in a prominent location.",
    "Be cautious of **unknown persons who want to pay cash for large quantities** of pesticides.",
    "Ask employees to report any unusual incidents or requests.",
    "Restrict access of nonemployees to your pesticide storage facilities."]},
 ], [], [
  mc("A stranger asks to buy a large quantity of pesticide and wants to pay cash. What does the manual say?",
     ["Sell it; cash sales are safest", "Be cautious of unknown persons who want to pay cash for large quantities of pesticides", "Require them to show a driver license only", "Refer them to the manufacturer"], 1,
     "p. 131, 'Steps to Prevent Security Problems'", "Be cautious of unknown persons who want to pay cash for large quantities.", style="scenario"),
  mc("According to the manual, the FBI says suspicious activity related to the use, training, or acquisition of pesticides should be immediately reported to whom?",
     ["The EPA only", "Management and local authorities", "The pesticide manufacturer", "The state department of agriculture only"], 1,
     "p. 130, 'Evaluating Pesticide Security'", "Report it immediately to management and local authorities."),
  mc("Which of these is NOT listed as part of good hiring and labor policies?",
     ["Employee training", "Background checks", "Workplace violence prevention", "Hiring only family members"], 3,
     "p. 130, 'Evaluating Pesticide Security'", "Hiring and labor policies include training, background checks, and workplace violence prevention.", style="not"),
  tf("The manual says local authorities, such as police and firefighters, should be included in developing the security plan.", True,
     "p. 130, 'Steps to Prevent Security Problems'", "Include local authorities in developing the security plan."),
  sh("Besides the police department, name one other group to call if you believe a security breach has occurred.", "the local emergency planning commission or fire departments",
     ["fire department", "local emergency planning commission", "LEPC", "emergency response agencies"],
     [["emergency planning", "fire", "lepc", "emergency response"]],
     "p. 130, 'Evaluating Pesticide Security'", "Also call the local emergency planning commission, fire departments, and other emergency response agencies."),
])

# ---------- 16
card(16, "Chapter 8 summary", [131, 131], [
  {"h": "Summary"},
  {"p": ["It is essential to establish safety and security practices for moving pesticides on the highways and at storage and job sites.",
    "Because spills and accidents are **more likely to occur while transporting or applying pesticides**, drivers and pesticide applicators must be **trained to respond quickly to a spill**.",
    "**Pesticide labels and SDSs** for the pesticide carried in the vehicle can provide important information in the event of a spill."]},
  {"p": ["Attention to pesticide site security and managing pesticides should be a **top priority**.",
    "Develop **security and emergency management plans** for every pesticide-handling and storage facility to safeguard employees and the community.",
    "Design security plans to reduce the risk of **theft, vandalism, and deliberate misuse** of pesticides by those wanting to harm others.",
    "Train employees in security and emergency response procedures and to coordinate efforts with **local police, emergency response personnel, and the FBI**."]},
 ], [], [
  mc("According to the summary, when are spills and accidents more likely to occur?",
     ["While storing pesticides", "While transporting or applying pesticides", "While buying pesticides", "While disposing of containers"], 1,
     "Chapter 8 Summary", "Spills and accidents are more likely while transporting or applying pesticides."),
  mc("Which of these is NOT a risk the summary says security plans should be designed to reduce?",
     ["Theft", "Vandalism", "Deliberate misuse of pesticides by those wanting to harm others", "Pest resistance"], 3,
     "Chapter 8 Summary", "Security plans target theft, vandalism, and deliberate misuse.", style="not"),
  mc("A driver hauling pesticides has a spill and needs product information fast. Per the summary, what in the vehicle provides it?",
     ["The vehicle registration", "The pesticide labels and SDSs", "The placard", "The shipping invoice"], 1,
     "Chapter 8 Summary", "Labels and SDSs for the pesticides carried provide important spill information.", style="scenario"),
  tf("The summary says employees should coordinate security efforts with local police, emergency response personnel, and the FBI.", True,
     "Chapter 8 Summary", "That is the summary's closing point."),
])

json.dump({"chapter": CH, "pages": [123, 131], "sections": S}, open("content/chapters/ch08.json", "w"), ensure_ascii=False, indent=1)
print(len(S), sum(len(s["questions"]) for s in S))

# merge short cards so each is roughly 2 to 3 minutes of reading
merges = {3: "Vehicle operator, SDSs, spill kits, and temperature", 6: "Storage buildings, site security, and water damage", 8: "Ventilation, lighting, floors, and what belongs in storage"}
out = []
i = 0
while i < len(S):
    s = S[i]; n = i + 1
    if n in merges:
        t = S[i + 1]
        s = {**s, "title": merges[n], "pages": [s["pages"][0], t["pages"][1]], "body": s["body"] + t["body"],
             "figures": s["figures"] + t["figures"], "questions": s["questions"] + t["questions"]}
        i += 2
    else:
        i += 1
    out.append(s)
for k, s in enumerate(out, 1):
    sid = f"c08-s{k:02d}"; s["id"] = sid
    rq = [q for q in s["questions"] if q["src"] == "review"]; tq = [q for q in s["questions"] if q["src"] == "test"]
    keep = {3: [0, 1, 2, 6, 8], 4: [0, 1, 2, 3, 4], 5: [0, 2, 3, 5, 7], 6: [0, 1, 2, 5, 7]}.get(k)
    if keep: tq = [tq[x] for x in keep]
    for q in rq: q["id"] = sid + "-r" + q["id"].split("-r")[-1]
    for j, q in enumerate(tq, 1): q["id"] = f"{sid}-t{j}"
    s["questions"] = rq + tq
json.dump({"chapter": CH, "pages": [123, 131], "sections": out}, open("content/chapters/ch08.json", "w"), ensure_ascii=False, indent=1)
print("merged", len(out), sum(len(s["questions"]) for s in out))
