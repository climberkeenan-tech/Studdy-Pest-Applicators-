#!/usr/bin/env python3
import json, pathlib
"""Generate content/chapters/ch06.json (Chapter 6, Personal Protective Equipment, pp. 89-103).
Cards are written in their original 24-card order, then three short pairs are merged and
test questions trimmed to 5 per card (see MERGE and DROP at the bottom). Run, then tools/build.py."""
CH = "Chapter 6 · Personal Protective Equipment"
def mc(i, q, choices, ans, ref, why, style=None, src="test", fixed=False):
    d = {"id": i, "src": src, "kind": "mc", "q": q, "choices": choices, "answer": ans, "ref": ref, "why": why}
    if style: d["style"] = style
    if fixed: d["fixed"] = True
    return d
def tf(i, q, ans, ref, why, style=None):
    d = {"id": i, "src": "test", "kind": "tf", "q": q, "answer": ans, "ref": ref, "why": why}
    if style: d["style"] = style
    return d
def short(i, q, ans, ref, why, keys=None, accept=None, style=None):
    d = {"id": i, "src": "test", "kind": "short", "q": q, "answer": ans, "ref": ref, "why": why}
    if keys: d["keys"] = keys
    if accept: d["accept"] = accept
    if style: d["style"] = style
    return d
def img(i, title, page, f, explain=None):
    d = {"id": i, "title": title, "page": page, "imgFile": f + ".jpg"}
    if explain: d["explain"] = explain
    return d
S = []
def card(n, title, pages, body, questions, figures=None):
    s = {"id": f"c06-s{n:02d}", "chapter": CH, "title": title, "pages": pages, "body": body}
    if figures: s["figures"] = figures
    s["questions"] = questions
    S.append(s)

# ---------- s01 ----------
card(1, "What PPE is, and what it cannot do", [89, 90], [
  {"box": "Learning objectives", "p": ["After studying this chapter, you should be able to do the following."], "list": [
    "Identify where on the label to find the minimum clothing and personal protective equipment (PPE) required to handle a given pesticide product.",
    "State the criteria to properly select skin, eye, and respiratory protection required by the pesticide label based upon your expected use and exposure.",
    "List three work practices each for correct use of gloves, footwear, and eyewear that minimize pesticide exposure and contamination.",
    "List the signs of wear and tear, damage, or other PPE failures that may expose you to pesticides.",
    "Explain the importance of wearing respiratory protection devices approved by the National Institute for Occupational Safety and Health.",
    "Tell when to replace particulate filters and chemical cartridges or canisters on your respirator.",
    "Distinguish between a fit test and a seal check for tight-fitting respirators.",
    "Describe how to clean and maintain pesticide-contaminated work clothes and PPE.",
    "Describe how to dispose of PPE when necessary."]},
  {"h": "Personal protective equipment"},
  {"p": [
    "The pesticide label prescribes handling precautions, **personal protective equipment (PPE)**, and other safety measures to minimize your exposure while handling pesticides.",
    "PPE comprises the clothing and devices you wear to protect your body from contact with pesticides.",
    "Wearing PPE can reduce exposure (**dermal, inhalation, ocular, or oral**) and thereby lower the chances of pesticide injury, illness, or poisoning."]},
  {"p": [
    "**Basic protective work clothing** consists of a long-sleeved shirt, long pants, closed-toed shoes, and socks.",
    "PPE, as defined by the U.S. Environmental Protection Agency (EPA), includes **coveralls, apron, gloves, footwear, headgear, eyewear, and respirators**."]},
  {"p": [
    "It is important that all pesticide applicators and handlers understand the protections and limitations of PPE.",
    "Although PPE may reduce your exposure to pesticides, it **does not necessarily eliminate it**.",
    "Proper PPE selection, use, and care are essential.",
    "The following are some good work practices that you should always follow when using pesticides."]},
], [
  mc("c06-s01-t1", "Which of these is NOT on EPA's list of what PPE includes?", ["Coveralls", "Headgear", "Respirators", "Sunscreen"], 3,
     "p. 90, 'Personal Protective Equipment'", "EPA lists coveralls, apron, gloves, footwear, headgear, eyewear, and respirators.", "not"),
  tf("c06-s01-t2", "Wearing the right PPE eliminates your exposure to pesticides.", False,
     "p. 90, 'Personal Protective Equipment'", "PPE may reduce exposure, but it does not necessarily eliminate it."),
  short("c06-s01-t3", "Name the four routes of exposure that wearing PPE can reduce.", "Dermal, inhalation, ocular, and oral.",
     "p. 89, 'Personal Protective Equipment'", "Skin, breathing, eyes, and mouth: dermal, inhalation, ocular, oral.",
     keys=[["dermal", "skin"], ["inhalation", "inhaling", "breathing", "lungs"], ["ocular", "eye", "eyes"], ["oral", "mouth", "swallowing"]],
     accept=["skin, lungs, eyes, mouth", "dermal inhalation ocular oral"]),
  mc("c06-s01-t4", "Basic protective work clothing consists of:", [
     "A long-sleeved shirt, long pants, closed-toed shoes, and socks",
     "Coveralls, chemical-resistant gloves, and goggles",
     "A short-sleeved shirt, long pants, and boots",
     "Any clean clothing plus a respirator"], 0,
     "p. 89-90, 'Personal Protective Equipment'", "Basic work clothing is long sleeves, long pants, closed-toed shoes, and socks."),
  mc("c06-s01-t5", "A new crew member says, \"I have all the label PPE on, so I can't be exposed.\" What is the correct response?", [
     "Right. Label PPE makes exposure impossible.",
     "PPE reduces exposure but does not necessarily eliminate it, so proper selection, use, and care still matter.",
     "Only a respirator eliminates exposure.",
     "PPE only matters for dermal exposure."], 1,
     "p. 90, 'Personal Protective Equipment'", "PPE lowers exposure but does not necessarily eliminate it.", "scenario"),
])

# ---------- s02 ----------
card(2, "Good work practices for every job", [90, 90], [
  {"h": "Good work practices"},
  {"p": [
    "It is important to take basic steps to reduce exposure when you handle pesticides or work in pesticide-treated areas.",
    "Remember to use common sense. No guidelines cover all situations."]},
  {"box": "Prevent oral exposure", "list": [
    "Never eat, drink, chew gum, use tobacco products, or handle cellphones while working with pesticides.",
    "Contaminated hands are a source of oral exposure to pesticides."]},
  {"box": "Prevent dermal exposure", "list": [
    "Wash your hands before using the toilet. The **groin area readily absorbs pesticide**.",
    "Wear a minimum of a long-sleeved shirt, long pants, and closed-toed shoes.",
    "Do not wipe contaminated gloves on your clothing. The pesticide may seep through."]},
  {"box": "Prevent ocular exposure", "list": [
    "Wear protective eyewear to protect from splashes, sprays, mists, fogs and aerosols."]},
  {"box": "Prevent inhalation exposure", "list": [
    "Avoid breathing in dusts, spray droplets, or vapors.",
    "Wear a respirator when needed, **even if the label does not require it**."]},
  {"box": "Decontaminate yourself and your PPE", "list": [
    "**Wash your gloves with soap and water before you take them off.** Remove them and wash your hands and face.",
    "Immediately wash off any pesticide that gets directly on you.",
    "Remove and replace damaged or contaminated clothing or PPE. Have spare clothing available.",
    "At the end of the day, wash or replace contaminated PPE.",
    "Shower at the end of the workday. Wash your hair and scalp and under your fingernails.",
    "Put on a complete change of clothing after you shower.",
    "Launder your work clothes separately from non-work and other clothes at the end of each workday."]},
], [
  mc("c06-s02-t1", "Why should you wash your hands before using the toilet when working with pesticides?", [
     "Soap residue can react with pesticides",
     "The groin area readily absorbs pesticide",
     "Toilets are a common source of pesticide spills",
     "It is required only for restricted use pesticides"], 1,
     "p. 90, 'Good Work Practices', Prevent dermal exposure", "The groin area readily absorbs pesticide."),
  mc("c06-s02-t2", "Which of these is NOT on the manual's list of things to never do while working with pesticides?", [
     "Chew gum", "Handle a cellphone", "Use tobacco products", "Wear protective eyewear"], 3,
     "p. 90, 'Good Work Practices', Prevent oral exposure", "Never eat, drink, chew gum, use tobacco, or handle cellphones. Eyewear is protection.", "not"),
  tf("c06-s02-t3", "You only need to wear a respirator when the label requires one.", False,
     "p. 90, 'Good Work Practices', Prevent inhalation exposure", "Wear a respirator when needed, even if the label does not require it."),
  mc("c06-s02-t4", "You finish mixing and are wearing contaminated gloves. What is the correct order?", [
     "Take gloves off, then wash the gloves and your hands",
     "Wash gloves with soap and water, take them off, then wash your hands and face",
     "Wipe gloves on your pants, take them off, then wash your hands",
     "Take gloves off and put them straight into a bag"], 1,
     "p. 90, 'Good Work Practices', Decontaminate yourself and your PPE", "Wash gloves before you take them off, then wash hands and face.", "scenario"),
  mc("c06-s02-t5", "Why should you never wipe contaminated gloves on your clothing?", [
     "It ruins the gloves", "The pesticide may seep through", "It voids the label", "It spreads pesticide to the gloves"], 1,
     "p. 90, 'Good Work Practices', Prevent dermal exposure", "Pesticide wiped on clothing may seep through to your skin."),
])

# ---------- s03 ----------
card(3, "The label sets the minimum PPE", [90, 91], [
  {"h": "Protect yourself from pesticides"},
  {"p": [
    "A pesticide label lists the **minimum PPE** that an applicator, handler, and early-entry worker must wear.",
    "Wearing anything less is **illegal and dangerous**.",
    "All pesticide handlers (for example, applicators, mixers and loaders, and flaggers) are responsible for following the pesticide label, including wearing PPE."]},
  {"p": [
    "PPE requirements are typically listed under the **\"Precautionary Statements\"** section of the pesticide label.",
    "If you work in or on a farm, forest, nursery, or greenhouse, look for additional PPE requirements listed in the **\"Agricultural Use Requirements\"** box on the label."]},
  {"p": [
    "Also, always check to see if state regulations are more restrictive than label requirements.",
    "For example, a label may allow you to wear less PPE when engineering controls (for example, an enclosed cab) are used, but the state, tribal, or territorial pesticide regulatory agency may prohibit this practice.",
    "Additionally, some states have more restrictive occupational health and safety regulations specific to pesticide applicators or to protect commercial sector workers, such as landscapers or pest management professionals.",
    "When a state, tribal, or local regulation is **more restrictive** than federal pesticide laws, it **must** be followed."]},
  {"p": [
    "Under EPA's **Worker Protection Standard (WPS, 40 CFR Part 170)**, agricultural employers are legally required to provide PPE that is in good working order.",
    "They also must train pesticide handlers on the proper use and maintenance of label-required PPE."]},
], [
  mc("c06-s03-t1", "Where on a pesticide label are PPE requirements typically listed?", [
     "Directions for Use", "Precautionary Statements", "Storage and Disposal", "Active ingredient statement"], 1,
     "p. 90, 'Protect Yourself from Pesticides'", "PPE is typically under the Precautionary Statements section."),
  mc("c06-s03-t2", "You work in a greenhouse. Where on the label do you look for additional PPE requirements?", [
     "The \"Agricultural Use Requirements\" box", "The signal word", "The EPA registration number", "The first aid statement"], 0,
     "p. 90, 'Protect Yourself from Pesticides'", "Farms, forests, nurseries, and greenhouses: check the Agricultural Use Requirements box.", "scenario"),
  mc("c06-s03-t3", "The label lets you wear less PPE in an enclosed cab, but your state agency prohibits that. What do you do?", [
     "Follow the label, because federal law is the label",
     "Follow the state rule, because a more restrictive state regulation must be followed",
     "Choose whichever is more practical that day",
     "Ask the dealer to decide"], 1,
     "p. 91, 'Protect Yourself from Pesticides'", "When a state rule is more restrictive than federal law, it must be followed.", "scenario"),
  tf("c06-s03-t4", "Wearing less PPE than the label lists is legal if you are only mixing and loading.", False,
     "p. 90, 'Protect Yourself from Pesticides'", "The label lists the minimum PPE. Wearing anything less is illegal and dangerous."),
  mc("c06-s03-t5", "Under the Worker Protection Standard (40 CFR Part 170), agricultural employers must:", [
     "Provide PPE in good working order and train handlers on its proper use and maintenance",
     "Only recommend PPE to workers",
     "Provide PPE only for restricted use pesticides",
     "Have workers buy their own PPE"], 0,
     "p. 91, 'Protect Yourself from Pesticides'", "WPS: employers must provide working PPE and train handlers on it."),
  mc("c06-s03-t6", "Which of these is NOT given as an example of a pesticide handler responsible for following the label?", [
     "Applicator", "Mixer and loader", "Flagger", "The dealer who sold the product"], 3,
     "p. 90, 'Protect Yourself from Pesticides'", "The manual names applicators, mixers and loaders, and flaggers.", "not"),
])

# ---------- s04 ----------
card(4, "Why PPE rules vary, and example label statements", [91, 91], [
  {"p": [
    "PPE label requirements vary, depending upon the **toxicity, formulation, dilution, and route of exposure** of the pesticide product and activity.",
    "For example, a single label may have one set of PPE requirements for applicators and a **different set for agricultural early-entry workers** going into areas during the restricted-entry interval.",
    "Even very low hazard pesticides require a long-sleeved shirt, long pants, shoes, and socks."]},
  {"fig": "p91-posted"},
  {"p": [
    "Consider all work situations where using PPE may be hazardous.",
    "Be careful around moving equipment parts (such as a **power takeoff unit**) that can catch **apron strings**.",
    "Protective clothing can restrict evaporation of sweat, thus impeding the body's natural cooling system and causing heat-related illnesses, including **heat stress** (see Chapter 5, Pesticide Hazards and First Aid, for more information)."]},
  {"box": "Example PPE statements on a label: Personal Protective Equipment", "p": ["All mixers, loaders, applicators, and other handlers must wear:"], "list": [
    "Long-sleeved shirt and long pants.",
    "Shoes and socks.",
    "Nitrile rubber, butyl rubber, barrier laminate, or Viton® gloves.",
    "Protective eyewear (goggles or face shield).",
    "Chemical-resistant apron when mixing or loading, cleaning up spills or equipment, or otherwise exposed to the concentrate."]},
  {"box": "Example PPE statements on a label: Agricultural Use Requirements", "p": ["PPE required for early entry to treated areas as permitted under the Worker Protection Standard and that involves contact with anything that has been treated (such as plants, soil, or water) includes:"], "list": [
    "Coveralls over short-sleeved shirt and short pants.",
    "Nitrile rubber, butyl rubber, barrier laminate, or Viton® gloves.",
    "Shoes plus socks.",
    "Protective eyewear."]},
  {"fig": "p91-ppe"},
], [
  mc("c06-s04-r1", "Which statement about PPE requirements listed on the pesticide label is true?", [
     "A label may have different PPE requirements for pesticide handlers and early-entry workers.",
     "You are not required to wear all the PPE listed on the label.",
     "Wearing the PPE listed on the label eliminates your exposure to pesticides."], 0,
     "p. 91, 'Protect Yourself from Pesticides'", "One label can set one PPE list for applicators and another for early-entry workers.", src="review"),
  mc("c06-s04-t1", "PPE label requirements vary depending on the product's:", [
     "Toxicity, formulation, dilution, and route of exposure",
     "Price, brand, and container size",
     "Color, odor, and package type",
     "Date of manufacture only"], 0,
     "p. 91, 'Protect Yourself from Pesticides'", "Toxicity, formulation, dilution, and route of exposure set the PPE."),
  tf("c06-s04-t2", "Very low hazard pesticides require no particular clothing.", False,
     "p. 91, 'Protect Yourself from Pesticides'", "Even very low hazard pesticides require long sleeves, long pants, shoes, and socks."),
  mc("c06-s04-t3", "You are mixing next to a tractor while wearing an apron. What specific hazard does the manual warn about?", [
     "The apron can melt from engine heat",
     "Apron strings can be caught by moving parts such as a power takeoff unit",
     "The apron blocks your view of the gauges",
     "Aprons are not allowed near tractors"], 1,
     "p. 91, 'Protect Yourself from Pesticides'", "Moving parts like a power takeoff unit can catch apron strings.", "scenario"),
  mc("c06-s04-t4", "Why can protective clothing lead to heat stress?", [
     "It absorbs sunlight",
     "It restricts evaporation of sweat, impeding the body's natural cooling",
     "It traps pesticide vapors against the skin",
     "It reduces blood flow"], 1,
     "p. 91, 'Protect Yourself from Pesticides'", "Clothing that restricts sweat evaporation impedes the body's cooling."),
  mc("c06-s04-t5", "In the example label box, which glove type is NOT listed?", [
     "Nitrile rubber", "Barrier laminate", "Viton®", "Leather"], 3,
     "p. 91, 'Example PPE Statements on a Label'", "The example lists nitrile rubber, butyl rubber, barrier laminate, or Viton® gloves.", "not"),
], [
  img("p91-posted", "Posted field during the restricted-entry interval.", "p. 91", "p91-posted"),
  img("p91-ppe", "Wearing appropriate types of personal protective equipment (PPE) can greatly reduce the risk of pesticide exposure.", "p. 91", "p91-ppe",
      ["The labels on the drawing are: goggles, respirator, coveralls, chemically resistant gloves, wide brim hat, chemically resistant boots, and a chemically resistant apron hanging beside the worker."]),
])

# ---------- s05 ----------
card(5, "Protect your body: what makes PPE protective", [92, 92], [
  {"h": "Protect your body"},
  {"p": [
    "Different types of clothing, aprons, hats, boots, and gloves are not equally protective against all pesticides and under all conditions.",
    "For PPE to be protective, it must do three things."]},
  {"ol": [
    "Shield your skin (head, face, neck, trunk, arms, legs, and feet) from exposure throughout the pesticide-handling activity.",
    "Be durable and resist punctures and tears during normal use.",
    "Be comfortable enough without restricting your movement so you will wear it."]},
  {"p": [
    "To protect your skin, your normal work clothing must cover most of your body.",
    "Depending on the product's toxicity and use, other PPE (such as coveralls, apron, hat, boots, and gloves) may also be required.",
    "Protective clothing, gloves, and boots must provide a barrier **for the duration of the task** when you are exposed to a pesticide.",
    "Labels may require **waterproof** gloves or boots.",
    "Additionally, **chemical-resistant** gloves, aprons, hats, boots, or suits are required on some labels."]},
  {"box": "Chemical resistant", "p": [
    "EPA defines **\"chemical resistant\"** as preventing any measurable amount of material from moving through (**breaking through**) the fabric or material."]},
  {"p": [
    "Things that can affect the extent of **breakthrough** are **contact time, concentration, temperature, and the product itself**.",
    "When selected correctly, protective clothing reduces the risk of dermal exposure but does not eliminate it."]},
  {"fig": "p92-minimum"},
], [
  short("c06-s05-t1", "How does EPA define \"chemical resistant\"?",
     "Preventing any measurable amount of material from moving through (breaking through) the fabric or material.",
     "p. 92, 'Protect Your Body'", "Chemical resistant means no measurable amount breaks through the material.",
     keys=[["measurable", "any amount", "any material", "any pesticide"], ["through", "breakthrough", "penetrate", "penetrating"]],
     accept=["no measurable amount of material moves through the fabric", "prevents any measurable amount from breaking through"]),
  mc("c06-s05-t2", "Which of these is NOT listed as affecting the extent of breakthrough?", [
     "Contact time", "Concentration", "Temperature", "The color of the fabric"], 3,
     "p. 92, 'Protect Your Body'", "Breakthrough depends on contact time, concentration, temperature, and the product.", "not"),
  mc("c06-s05-t3", "For PPE to be protective, it must:", [
     "Shield your skin, be durable, and be comfortable enough that you will wear it",
     "Be disposable, white, and loose",
     "Be made of cotton, be washable, and be cheap",
     "Cover only the hands and face"], 0,
     "p. 92, 'Protect Your Body'", "The three musts: shield skin, durable, comfortable enough to wear."),
  mc("c06-s05-t4", "A suit is highly protective but so stiff and hot that the applicator takes it off by noon. Which requirement for protective PPE does it fail?", [
     "Shield your skin", "Be durable", "Be comfortable enough without restricting movement so you will wear it", "Be chemical resistant"], 2,
     "p. 92, 'Protect Your Body'", "PPE you will not keep on does not protect you.", "scenario"),
  tf("c06-s05-t5", "Protective clothing must provide a barrier for the duration of the task when you are exposed.", True,
     "p. 92, 'Protect Your Body'", "Clothing, gloves, and boots must hold up for the whole task."),
], [
  img("p92-minimum", "At a minimum wear a long-sleeved shirt, long pants, shoes, and socks when working around pesticides.", "p. 92", "p92-minimum"),
])

# ---------- s06 ----------
card(6, "Work clothing", [92, 92], [
  {"h": "Work clothing"},
  {"p": [
    "Your work clothes provide a basic barrier to minimize pesticide contact with your skin.",
    "Always wear, at a minimum, a **long-sleeved shirt, long pants, closed-toed shoes, and socks** whenever you handle pesticides or work around pesticide residues.",
    "Select work clothes made of **tightly woven fabrics** to reduce pesticide penetration.",
    "Make sure they are free of holes and tears.",
    "**Fasten the shirt collar completely** to protect the lower part of your neck."]},
  {"p": [
    "Do not use these work clothes for anything other than handling pesticides.",
    "Store and launder fabric work clothing **separately from all other clothing** after each day's use.",
    "See \"Maintaining Clothing and Personal Protective Equipment\" at the end of this chapter for details on cleaning and disposing of pesticide-soiled work clothes."]},
  {"box": "Good work practices: basic work clothes", "list": [
    "Always wear at a minimum a long-sleeved shirt and long pants.",
    "Make sure work clothes are sufficiently durable.",
    "Wash work clothes at the end of the day, separate from other clothing."]},
], [
  mc("c06-s06-t1", "Why choose work clothes made of tightly woven fabrics?", [
     "They are cooler", "To reduce pesticide penetration", "They dry faster", "They are required by WPS"], 1,
     "p. 92, 'Work Clothing'", "Tightly woven fabric reduces pesticide penetration."),
  mc("c06-s06-t2", "Why fasten the shirt collar completely?", [
     "To protect the lower part of your neck", "To keep the respirator straps in place", "To look professional", "To keep the shirt from catching in equipment"], 0,
     "p. 92, 'Work Clothing'", "A fastened collar protects the lower part of the neck."),
  mc("c06-s06-t3", "Your pesticide work pants look clean, and you want to wear them to help a friend move on Saturday. What does the manual say?", [
     "Fine, if they look clean",
     "Do not use these work clothes for anything other than handling pesticides",
     "Fine, after one rinse",
     "Fine, if you wear coveralls over them"], 1,
     "p. 92, 'Work Clothing'", "Work clothes are for handling pesticides only.", "scenario"),
  tf("c06-s06-t4", "Lightly soiled pesticide work clothes can be laundered with the family wash.", False,
     "p. 92, 'Work Clothing'", "Store and launder work clothing separately from all other clothing."),
])

# ---------- s07 ----------
card(7, "Coveralls", [92, 93], [
  {"h": "Coveralls"},
  {"p": [
    "Some pesticide labels require **coveralls** (a second layer of clothing) over work clothes.",
    "According to regulations, coveralls must be **loose-fitting**, one- or two-piece garments that cover the **entire body except head, hands, and feet**.",
    "A coverall can be made of woven (like cotton or twill) or nonwoven fabrics.",
    "It should be either easy to clean and sturdy enough for laundering and repeated use, or disposable."]},
  {"p": [
    "Wearing a disposable coverall reduces decontamination time and lowers the risk of contaminating yourself, your application equipment, and your vehicle.",
    "Disposable coveralls **differ in their level of protection**.",
    "**Most importantly**, wearing coveralls lessens the chance that you will **take pesticides home**.",
    "Handle disposable coveralls carefully so as to not contaminate other people."]},
  {"p": [
    "Very few pesticides require a chemical-resistant coverall.",
    "If one is required, work with your PPE supplier to find a coverall that provides the necessary level of protection based on the tasks you perform, the product formulation, and exposure."]},
  {"fig": "p92-coverall"},
  {"box": "Good work practices: coveralls", "list": [
    "Make sure the coverall is durable and does not rip, tear, or puncture easily.",
    "Wash before reuse. Do not wash with other laundry.",
    "Protect from excess heat (conditioning, hydration, and cooling) when wearing additional layers of clothing."]},
], [
  mc("c06-s07-t1", "By regulation, coveralls must cover the entire body except:", [
     "Head, hands, and feet", "Arms and legs", "Neck and face only", "Nothing. They cover everything."], 0,
     "p. 92, 'Coveralls'", "Coveralls are loose-fitting and cover all but head, hands, and feet."),
  mc("c06-s07-t2", "According to the manual, the most important benefit of wearing coveralls is that it:", [
     "Keeps work clothes looking clean",
     "Lessens the chance that you will take pesticides home",
     "Replaces the need for gloves",
     "Lets you skip the shower at the end of the day"], 1,
     "p. 92, 'Coveralls'", "Most importantly, coveralls lessen the chance you take pesticides home."),
  mc("c06-s07-t3", "Which statement about disposable coveralls is NOT true?", [
     "They reduce decontamination time",
     "They lower the risk of contaminating your equipment and vehicle",
     "They must be handled carefully so you do not contaminate other people",
     "They all give the same level of protection"], 3,
     "p. 92, 'Coveralls'", "Disposable coveralls differ in their level of protection.", "not"),
  tf("c06-s07-t4", "Most pesticide labels require a chemical-resistant coverall.", False,
     "p. 92, 'Coveralls'", "Very few pesticides require a chemical-resistant coverall."),
  mc("c06-s07-t5", "It is a hot July afternoon and the label requires coveralls over your work clothes. What good work practice applies?", [
     "Skip the coveralls when it is over 90 degrees",
     "Protect yourself from excess heat with conditioning, hydration, and cooling",
     "Wear the coveralls without work clothes underneath",
     "Unzip the coveralls to the waist"], 1,
     "p. 93, 'Good work practices: coveralls'", "Extra layers call for heat protection: conditioning, hydration, cooling.", "scenario"),
], [
  img("p92-coverall", "A well-designed coverall makes it hard for pesticides to get through to your inner clothing or skin.", "p. 92", "p92-coverall"),
])

# ---------- s08 ----------
card(8, "Aprons and headgear", [93, 93], [
  {"h": "Apron for mixing"},
  {"p": [
    "Some pesticide labels require you to wear a **chemical-resistant apron** when **mixing or loading** a pesticide, or when **cleaning application equipment**.",
    "Select aprons that cover the front of your body **from the middle of the chest to the knees**."]},
  {"fig": "p93-apron"},
  {"h": "Headgear for overhead applications"},
  {"p": [
    "If an overhead application may result in exposure, a pesticide label may require **chemical-resistant headgear**.",
    "This headgear must protect against sprays so that no liquid breaks through the hat or hood.",
    "You may use either a **chemical-resistant hat with a wide brim** or a **hood**.",
    "Hoods attached to jackets or suits protect your **neck and back** from pesticide sprays that might otherwise run down your back.",
    "Wash headgear at the end of the day.",
    "When making overhead applications, **do not use headgear made of absorbent material**, such as cotton, leather, or straw."]},
  {"box": "Good work practices: headgear for overhead exposures", "list": [
    "**Cotton ball caps absorb pesticides.** Do not wear them if overhead exposure is a concern."]},
], [
  mc("c06-s08-t1", "A chemical-resistant apron should cover the front of your body from:", [
     "The waist to the ankles", "The middle of the chest to the knees", "The neck to the waist", "The shoulders to mid-thigh"], 1,
     "p. 93, 'Apron for Mixing'", "Middle of the chest to the knees. The photo caption says neck to at least the knees."),
  mc("c06-s08-t2", "Labels may require a chemical-resistant apron during which tasks?", [
     "Mixing or loading, or cleaning application equipment",
     "Only during aerial application",
     "Only when driving the sprayer",
     "Only when scouting fields"], 0,
     "p. 93, 'Apron for Mixing'", "Aprons are for mixing, loading, and cleaning application equipment."),
  mc("c06-s08-t3", "Which of these is NOT acceptable headgear for an overhead application when the label requires chemical-resistant headgear?", [
     "A chemical-resistant hat with a wide brim", "A chemical-resistant hood", "A hood attached to a chemical-resistant suit", "A straw hat"], 3,
     "p. 93, 'Headgear for Overhead Applications'", "Do not use absorbent headgear such as cotton, leather, or straw.", "not"),
  mc("c06-s08-t4", "You are spraying overhead in an orchard and your coworker is wearing a cotton ball cap. What should happen?", [
     "Nothing, any hat is fine",
     "Replace it. Cotton ball caps absorb pesticides and should not be worn when overhead exposure is a concern.",
     "Turn the cap backward",
     "Wash the cap at the end of the day and keep using it"], 1,
     "p. 93, 'Good work practices: headgear for overhead exposures'", "Cotton ball caps absorb pesticide. Do not wear them for overhead work.", "scenario"),
  tf("c06-s08-t5", "Hoods attached to jackets or suits protect your neck and back from spray that might run down your back.", True,
     "p. 93, 'Headgear for Overhead Applications'", "That is exactly why hoods are recommended."),
], [
  img("p93-apron", "Choose a chemical-resistant apron that extends from your neck to at least your knees.", "p. 93", "p93-apron"),
])

# ---------- s09 ----------
card(9, "Footwear", [93, 93], [
  {"h": "Footwear"},
  {"p": [
    "Many pesticide labels require you to wear shoes and socks.",
    "Make sure the shoes have closed toes.",
    "However, some product labels require you to wear **chemical-resistant footwear**.",
    "A heavy-duty pair of **unlined rubber boots** or shoe covers provides protection from pesticides.",
    "Wash them **inside and out** at the end of the day."]},
  {"p": [
    "**Leather and canvas absorb pesticides and cannot be decontaminated.**",
    "Regulations allow you to substitute leather for chemical-resistant boots **only** when the chemical-resistant footwear required by the pesticide label is **not durable enough for use in rough terrain**.",
    "Do not use these boots for other purposes."]},
  {"fig": "p93-nocotton"},
  {"box": "Good work practices: footwear", "list": [
    "Never wear open-toed shoes or sandals when applying pesticides.",
    "Wear heavy-duty rubber boots that extend **past your ankle and at least halfway up to your knee** if you will enter or walk through treated areas before spray has dried.",
    "Put your **pant legs outside your boots** to prevent pesticides from running down your legs and becoming trapped in your footwear.",
    "Do not use footwear used for applying pesticides for anything else.",
    "Do not wear work footwear home."]},
], [
  mc("c06-s09-t1", "When do regulations allow leather boots in place of chemical-resistant boots?", [
     "Whenever the weather is dry",
     "Only when the label's chemical-resistant footwear is not durable enough for rough terrain",
     "Whenever the pesticide is a dry formulation",
     "Never"], 1,
     "p. 93, 'Footwear'", "Leather substitutes only when required chemical-resistant footwear cannot handle rough terrain."),
  mc("c06-s09-t2", "Why wear your pant legs outside your boots?", [
     "So pesticide does not run down your legs and get trapped in your footwear",
     "So the boots stay cleaner",
     "So you can move more easily",
     "So the pants dry faster"], 0,
     "p. 93, 'Good work practices: footwear'", "Pants outside boots keep pesticide from running into the boots."),
  mc("c06-s09-t3", "You must walk through a treated area before the spray has dried. How tall should your rubber boots be?", [
     "Ankle height is enough",
     "Past your ankle and at least halfway up to your knee",
     "Up to the hip",
     "Height does not matter if they are rubber"], 1,
     "p. 93, 'Good work practices: footwear'", "Past the ankle and at least halfway to the knee.", "scenario"),
  tf("c06-s09-t4", "Leather boots can be decontaminated if you wash them inside and out.", False,
     "p. 93, 'Footwear'", "Leather and canvas absorb pesticides and cannot be decontaminated."),
  mc("c06-s09-t5", "Which of these is NOT a good work practice for footwear?", [
     "Never wear sandals when applying pesticides",
     "Do not wear work footwear home",
     "Wash rubber boots inside and out at the end of the day",
     "Wear your spray boots for yard work on weekends to get more use from them"], 3,
     "p. 93, 'Good work practices: footwear'", "Footwear used for applying pesticides is for nothing else.", "not"),
], [
  img("p93-nocotton", "Clothes made of cotton, leather, or canvas are not chemically resistant, even to dry formulations.", "p. 93", "p93-nocotton",
      ["The drawing shows a ball cap, a work boot, and a cloth glove crossed out."]),
])

# ---------- s10 ----------
card(10, "Gloves: where the exposure is", [94, 94], [
  {"h": "Gloves"},
  {"p": [
    "Pesticide handlers get **by far the most exposure** from pesticides on their **hands and forearms**.",
    "Research has shown that workers mixing pesticides received **85%** of the total exposure on their **hands** and **13%** on their **forearms** (see Figure 6.1).",
    "The same study showed that wearing protective gloves **reduced exposure by 99%**.",
    "Protective gloves are essential to dermal protection."]},
  {"fig": "fig-6-1"},
  {"p": [
    "Pesticide labels often require **waterproof gloves** or one of the following glove types: **nitrile rubber, butyl rubber, neoprene rubber, barrier laminate, and Viton®**.",
    "Each glove type varies significantly in how well it protects from the different solvents in formulated products.",
    "For this reason, it is important to read each label to determine which glove type is appropriate.",
    "The glove type varies from product to product, **even those with similar active ingredients**."]},
  {"box": "Follow the label carefully", "p": [
    "Know which particular gloves are required.",
    "For most products, a waterproof glove is sufficient.",
    "However, if the label requires a specific glove type and you wear the wrong one, the glove may degrade quickly from the solvents in the formulated product."]},
], [
  mc("c06-s10-t1", "In the study the manual cites, workers mixing pesticides received what share of their total exposure on their hands?", [
     "13%", "50%", "85%", "99%"], 2,
     "p. 94, 'Gloves'", "85% on the hands, 13% on the forearms."),
  mc("c06-s10-t2", "Wearing protective gloves reduced exposure by how much in that study?", [
     "13%", "50%", "85%", "99%"], 3,
     "p. 94, 'Gloves'", "Gloves cut exposure by 99%."),
  mc("c06-s10-t3", "Which of these is NOT one of the glove types the manual lists that labels often require?", [
     "Nitrile rubber", "Neoprene rubber", "Viton®", "Cotton"], 3,
     "p. 94, 'Gloves'", "Listed: nitrile, butyl, neoprene, barrier laminate, and Viton®.", "not"),
  tf("c06-s10-t4", "Two products with similar active ingredients will always call for the same glove type.", False,
     "p. 94, 'Gloves'", "Glove type varies from product to product, even with similar active ingredients."),
  mc("c06-s10-t5", "The label calls for butyl rubber gloves. You only have a different waterproof glove. What is the risk?", [
     "None, any waterproof glove works for every product",
     "The wrong glove may degrade quickly from the solvents in the formulated product",
     "The glove will be too thick to work in",
     "Only a fine from the employer"], 1,
     "p. 94, 'Follow the Label Carefully' box", "If the label names a glove type, the wrong one may break down fast.", "scenario"),
], [
  {"id": "fig-6-1", "title": "Figure 6.1: Farmers who wore gloves while applying pesticides reduced their risk of exposure (The Farm Family Exposure Study, John Acquavella).",
   "page": "p. 94", "svgFile": "fig-6-1.svg",
   "explain": ["The chart compares the amount of pesticide detected, in parts per billion, with gloves and without gloves, for glyphosate, chlorpyrifos, and 2,4-D.",
               "For all three pesticides, the no-gloves bar is higher. The bar heights here are read off the manual's chart, which prints no exact values.",
               "2,4-D uses a larger scale, up to 250, and shows the biggest gap."]},
])

# ---------- s11 ----------
card(11, "Gloves: solvents, categories, and thickness", [94, 95], [
  {"p": [
    "**The solvent in a pesticide formulation determines the protective glove type.**",
    "Pesticide labels require either **waterproof gloves** (for solid or water-based formulations) or **chemical-resistant gloves** for the various solvents (for example, alcohols, ketones, and petroleum distillates) used in different formulations.",
    "For liquid products with a solvent other than water, EPA requires the label to specify particular glove materials that provide protection.",
    "Note that labels that have not been recently updated may still refer to a **solvent category (A through H)** in the EPA Chemical Resistance Category Selection Chart for Gloves."]},
  {"box": "Reference chart for gloves (two or more hours contact)", "list": [
    "Category A: Any waterproof material.",
    "Category B: ONLY butyl rubber or barrier laminate.",
    "Category C: Butyl rubber, nitrile, neoprene, polyvinyl chloride, barrier laminate, or Viton®.",
    "Category D: ONLY butyl rubber or barrier laminate.",
    "Category E: Nitrile, neoprene, barrier laminate, or Viton®.",
    "Category F: Butyl rubber, nitrile, barrier laminate, or Viton®.",
    "Category G: ONLY barrier laminate or Viton®.",
    "Category H: ONLY barrier laminate or Viton®."]},
  {"p": [
    "Read the label carefully to make sure you have the correct protective glove material.",
    "Explain to your supplier which glove types you need."]},
  {"p": [
    "Some pesticide labels specify both the glove material and its thickness.",
    "As a general rule, **the thicker the glove** (of the same material under identical conditions), **the longer the breakthrough time**.",
    "A pesticide label's specification of glove type is generally based upon a thickness of **14 mils**, except for polyethylene and barrier laminate gloves.",
    "Use the 14 mils thickness as a rule of thumb when selecting glove materials that appear on the pesticide label."]},
  {"p": [
    "Glove durability is another important consideration.",
    "Select a glove that is protective, does not tear or puncture easily, and protects you for the duration of the task.",
    "Discard the gloves if there is any sign of wear or if the gloves leak."]},
], [
  mc("c06-s11-r2", "Which part of the product formulation determines what glove type is needed?", [
     "Active ingredient.", "Surfactants.", "Solvents."], 2,
     "p. 94, 'Gloves'", "The solvent in a formulation determines the protective glove type.", src="review"),
  mc("c06-s11-t1", "For solid or water-based formulations, labels require:", [
     "Waterproof gloves", "Only barrier laminate gloves", "Leather gloves", "No gloves"], 0,
     "p. 94, 'Gloves'", "Solid or water-based: waterproof gloves. Other solvents: chemical-resistant gloves."),
  mc("c06-s11-t2", "An older label says to use gloves from Category A. What does that allow?", [
     "Only butyl rubber or barrier laminate", "Any waterproof material", "Only barrier laminate or Viton®", "Only nitrile"], 1,
     "p. 94, 'Reference Chart for Gloves'", "Category A means any waterproof material.", "scenario"),
  mc("c06-s11-t3", "A label's glove specification is generally based on what thickness?", [
     "4 mils", "8 mils", "14 mils", "40 mils"], 2,
     "p. 94, 'Gloves'", "14 mils, except polyethylene and barrier laminate gloves."),
  tf("c06-s11-t4", "For the same material under identical conditions, a thicker glove has a longer breakthrough time.", True,
     "p. 94, 'Gloves'", "Thicker glove, longer breakthrough time."),
  mc("c06-s11-t5", "Which of these is NOT given as an example of a solvent that calls for chemical-resistant gloves?", [
     "Alcohols", "Ketones", "Petroleum distillates", "Water"], 3,
     "p. 94, 'Gloves'", "Water-based formulations need only waterproof gloves.", "not"),
])

# ---------- s12 ----------
card(12, "Gloves: materials to avoid, fit, and care", [95, 95], [
  {"p": [
    "Do not use gloves made of any kind of **absorbent material, lining, or flocking**, including **leather or cloth** (exception: **cloth gloves are used with fumigants**).",
    "These types of gloves absorb pesticide and trap it closely against your bare skin, greatly increasing skin absorption."]},
  {"p": [
    "Choose a glove size that fits you comfortably.",
    "Gloves that fit well provide increased dexterity for equipment maintenance or calibration.",
    "Gloves that are **too tight** stretch the material, allowing pesticides to break through.",
    "Gloves that are **too large** can get caught in equipment.",
    "And gloves that are **too loose** may allow pesticides to run down the inside and be directly absorbed by your skin."]},
  {"p": [
    "Select gloves designed to give you extra protection when needed for the job, such as **elbow-length gloves when mixing and loading**.",
    "Wear gloves according to how you are applying the pesticide.",
    "**Do not use a glove beyond the breakthrough time.**"]},
  {"p": [
    "When using reusable gloves, **rinse them at each break** and **wash them thoroughly at the end of the workday**.",
    "Absorbed pesticides will continue to permeate the material if not cleaned.",
    "Make sure your gloves are in top condition.",
    "Throw out any gloves showing wear.",
    "Check glove integrity before each use.",
    "Rinse disposable gloves before discarding them."]},
  {"fig": "p94-gloves"},
], [
  mc("c06-s12-t1", "Why should you not use leather or cloth-lined gloves with most pesticides?", [
     "They wear out too fast",
     "They absorb pesticide and trap it against your skin, greatly increasing skin absorption",
     "They are too hot",
     "They are not sold in all sizes"], 1,
     "p. 95, 'Gloves'", "Absorbent gloves hold pesticide against bare skin."),
  mc("c06-s12-t2", "Cloth gloves are the exception, and are used with which kind of pesticide?", [
     "Herbicides", "Fumigants", "Granular insecticides", "Rodenticide baits"], 1,
     "p. 95, 'Gloves'", "Cloth gloves are used with fumigants."),
  mc("c06-s12-t3", "Which glove fit problem allows pesticides to break through by stretching the material?", [
     "Too tight", "Too large", "Too loose", "Elbow-length"], 0,
     "p. 95, 'Gloves'", "Too tight stretches the material. Too large catches in equipment. Too loose lets pesticide run inside."),
  mc("c06-s12-t4", "You are about to mix and load a concentrate. What kind of glove gives the extra protection the manual names for this job?", [
     "Short disposable gloves", "Elbow-length gloves", "Cotton work gloves", "Leather gloves"], 1,
     "p. 95, 'Gloves'", "Elbow-length gloves when mixing and loading.", "scenario"),
  tf("c06-s12-t5", "Reusable gloves only need washing at the end of the workday.", False,
     "p. 95, 'Gloves'", "Rinse them at each break and wash them thoroughly at the end of the day."),
  mc("c06-s12-t6", "Which of these is NOT correct glove care?", [
     "Check glove integrity before each use", "Throw out gloves showing wear", "Rinse disposable gloves before discarding them", "Keep using a glove past its breakthrough time if it looks fine"], 3,
     "p. 95, 'Gloves'", "Do not use a glove beyond the breakthrough time.", "not"),
], [
  img("p94-gloves", "Nitrile and butyl rubber gloves.", "p. 94", "p94-gloves"),
])

# ---------- s13 ----------
card(13, "Good work practices for gloves", [95, 95], [
  {"box": "Good work practices: gloves", "list": [
    "Wear waterproof or chemical-resistant gloves when applying pesticides. Although pesticide labels do not always specifically require gloves, wearing them reduces your exposure (exception: when handling **fumigants**).",
    "Check gloves closely for holes by **filling the gloves with clean water and gently squeezing**. Discard them if you find any leakage.",
    "Wear gloves whenever you might get pesticides or residue on your hands, such as when cleaning sprayer nozzles or working around contaminated equipment or surfaces.",
    "Wear gloves according to the type of arm movements you make when handling pesticides (see Figure 6.2).",
    "Wash your gloves before taking them off between tasks.",
    "If pesticide is spilled, splashed, or gets inside your gloves, take them off immediately. Wash your hands and put on a clean pair of gloves.",
    "Replace your gloves immediately if they get cut, torn, or damaged.",
    "If making several applications during the day, change out gloves between jobs to avoid contaminating yourself and your vehicle.",
    "Rinse and slash used gloves before discarding."]},
  {"fig": "p95-fig62"},
], [
  mc("c06-s13-t1", "How does the manual say to check gloves for holes?", [
     "Hold them up to a light",
     "Fill them with clean water and gently squeeze",
     "Blow into them",
     "Soak them in detergent overnight"], 1,
     "p. 95, 'Good work practices: gloves'", "Fill with clean water and squeeze. Any leak means discard."),
  mc("c06-s13-t2", "You are spraying above your head. How should you wear your gloves?", [
     "Sleeves over gloves",
     "Gloves outside your sleeves, with the cuff folded up 1 or 2 inches",
     "No gloves, so you can grip better",
     "Gloves inside the sleeves, taped shut"], 1,
     "p. 95, Figure 6.2", "Overhead: gloves outside sleeves, cuff folded up 1 or 2 inches, so spray cannot run down your arm.", "scenario"),
  mc("c06-s13-t3", "For jobs where your hands are mostly lowered, how should you wear gloves?", [
     "Sleeves over gloves", "Gloves over sleeves with a folded cuff", "Two pairs of gloves", "Gloves taped to sleeves"], 0,
     "p. 95, Figure 6.2", "Hands lowered: sleeves over gloves, so runoff stays outside the glove."),
  mc("c06-s13-t4", "Pesticide splashes inside your glove. What do you do?", [
     "Finish the job, then wash",
     "Take the gloves off immediately, wash your hands, and put on a clean pair",
     "Wipe the inside with a rag",
     "Rinse the outside of the glove"], 1,
     "p. 95, 'Good work practices: gloves'", "Off immediately, wash hands, clean pair.", "scenario"),
  mc("c06-s13-t5", "Wearing gloves reduces your exposure even when the label does not require them. What is the manual's exception?", [
     "Granular products", "Handling fumigants", "Water-based products", "Ready-to-use products"], 1,
     "p. 95, 'Good work practices: gloves'", "The exception is when handling fumigants."),
], [
  img("p95-fig62", "Figure 6.2: Wear gloves according to how you are applying the pesticide: (1) sleeves over gloves for jobs where your hands are mostly lowered, (2) gloves outside your sleeves with cuff folded up 1 or 2 inches when spraying above your head.", "p. 95", "p95-fig62",
      ["Panel 1 shows a worker spraying downward with the sleeves pulled over the gloves.",
       "Panel 2 shows a worker spraying overhead with the gloves over the sleeves and the cuffs folded up."]),
])

# ---------- s14 ----------
card(14, "Protect your eyes", [95, 96], [
  {"h": "Protect your eyes"},
  {"p": [
    "**Eyes readily absorb pesticides.**",
    "When a label says to wear protective eyewear, you may use **goggles; a face shield; safety glasses with shields at the front, brow, and temple; or a full-face respirator**.",
    "Use common sense and select eyewear that protects you for the task at hand.",
    "Eyewear made of impact-resistant material, such as **polycarbonate**, can protect you from flying objects, such as granular pesticides.",
    "However, **safety glasses will not protect your eyes from pesticide splashes**."]},
  {"p": [
    "Products that are corrosive to the eyes (for example, those with the signal word Danger) require a particular type of eyewear.",
    "For example, goggles may be required when your eyes may be exposed to liquids or particulates during a certain application or use.",
    "Wear **tightly fitting goggles** when you are in high-exposure situations, such as an **open cab during an air-blast application**; applying **mists, fogs, or aerosols indoors**; or in any other location where you will be enveloped in a spray, mist, or dust.",
    "Make sure goggles are splash- and spray-proof and have an **air baffle system** for airflow and **no side vents**.",
    "If fogging is a problem, use anti-fog lens treatments or purchase low-fog goggles."]},
  {"fig": "p95-goggles"},
  {"p": [
    "If your eyewear has a headband that is made of pesticide-absorbent material, **change it often or use a rubber strap**.",
    "If possible, wear the strap under your hat or hood to protect it from becoming contaminated.",
    "Protective eyewear can be worn with a half-face respirator.",
    "If you wear eyeglasses, you can buy an eyeglass insert for your full-face respirator that is fitted with your prescription.",
    "People who wear **contact lenses** should consult an eye doctor or their medical professional before using pesticides or wearing respirators."]},
  {"box": "Good work practices: eyewear", "list": [
    "**Minimum eyewear** is safety glasses with shields at the front, brow, and temple.",
    "If goggles are required, have an **eyewash dispenser** immediately available.",
    "Consult an eye doctor if you wear contact lenses."]},
], [
  mc("c06-s14-t1", "When a label says protective eyewear, which of these is NOT one of the options the manual allows?", [
     "Goggles", "A face shield", "A full-face respirator", "Ordinary prescription eyeglasses"], 3,
     "p. 95, 'Protect Your Eyes'", "Allowed: goggles, face shield, safety glasses with front, brow, and temple shields, or a full-face respirator.", "not"),
  tf("c06-s14-t2", "Safety glasses will protect your eyes from pesticide splashes.", False,
     "p. 95, 'Protect Your Eyes'", "Safety glasses stop flying objects, not splashes."),
  mc("c06-s14-t3", "You will ride in an open cab during an air-blast application. What eye protection does the manual call for?", [
     "Sunglasses", "Tightly fitting goggles", "Safety glasses without side shields", "No eyewear if you wear a hat"], 1,
     "p. 96, 'Protect Your Eyes'", "High-exposure situations like an open cab air-blast call for tight goggles.", "scenario"),
  mc("c06-s14-t4", "Goggles for pesticide work should have:", [
     "Side vents for airflow", "An air baffle system for airflow and no side vents", "A cloth headband", "Tinted lenses"], 1,
     "p. 96, 'Protect Your Eyes'", "Air baffle system, no side vents, splash- and spray-proof."),
  mc("c06-s14-t5", "If goggles are required, what must be immediately available?", [
     "A spare respirator", "An eyewash dispenser", "Contact lens solution", "A first aid manual"], 1,
     "p. 96, 'Good work practices: eyewear'", "Goggles required means an eyewash dispenser on hand."),
  mc("c06-s14-t6", "What is the minimum eyewear according to the good work practices?", [
     "Safety glasses with shields at the front, brow, and temple", "Goggles", "A face shield", "A full-face respirator"], 0,
     "p. 96, 'Good work practices: eyewear'", "Minimum is safety glasses with front, brow, and temple shields."),
], [
  img("p95-goggles", "Tight-fitting goggles help protect your eyes from pesticide exposure.", "p. 95", "p95-goggles"),
])

# ---------- s15 ----------
card(15, "Respirators and NIOSH approval", [96, 97], [
  {"h": "Protect your respiratory system"},
  {"p": [
    "When you use pesticides, you may be exposed to toxic gases, vapors, particulates (solids or liquids), or all of these.",
    "A **respirator** is a safety device that protects you from inhaling contaminated air.",
    "The pesticide label states whether you must use a respirator and, if so, which type.",
    "The respirator type is based on the **pesticide formulation, application method, and environment** where the application is made."]},
  {"p": [
    "The **National Institute for Occupational Safety and Health (NIOSH)** certifies that respirators have been tested according to certain standards.",
    "The NIOSH approval of a respirator indicates that it protects the wearer against specified contaminants.",
    "All respirator manufacturers issue **approval certificates** with a chart of all of the components considered part of the approved assembly.",
    "Respirator approvals are **manufacturer-specific**: do not interchange parts, cartridges, or filters between different manufacturers' units.",
    "These certificates are typically package inserts with new respirators, cartridges, and filters.",
    "Find out if there are federal, state, tribal, or territorial health and safety regulations that stipulate proper respirator selection, care, and use."]},
  {"box": "Types of respirators", "list": [
    "**Atmosphere-supplying respirators:** supplied-air respirator, and self-contained breathing apparatus (SCBA).",
    "**Air-purifying respirators:** non-powered particulate respirators, powered air-purifying respirators (PAPR), chemical cartridge respirators (half facemask and full facemask), and gas masks with canisters."]},
  {"p": [
    "There are other respirators on the market that are **not NIOSH-approved**, such as **nuisance dust masks and some surgical masks**.",
    "When a respirator is required for working with pesticides, wear a **NIOSH-approved device that is listed on the label**."]},
], [
  mc("c06-s15-t1", "What does NIOSH stand for?", [
     "National Institute for Occupational Safety and Health",
     "National Inspection Office for Safety Hazards",
     "Northern Institute of Safety and Health",
     "National Institute of Spraying Hygiene"], 0,
     "p. 96, 'Protect Your Respiratory System'", "NIOSH certifies respirators."),
  mc("c06-s15-t2", "Your respirator is brand X. Brand Y cartridges fit the threads perfectly and are cheaper. What does the manual say?", [
     "Use them if they fit",
     "Do not interchange parts, cartridges, or filters between manufacturers. Approvals are manufacturer-specific.",
     "Use them only for dry formulations",
     "Use them if the label allows organic vapor cartridges"], 1,
     "p. 96, 'Protect Your Respiratory System'", "NIOSH approvals cover one manufacturer's whole assembly.", "scenario"),
  mc("c06-s15-t3", "Which of these is NOT something the respirator type is based on?", [
     "The pesticide formulation", "The application method", "The environment where the application is made", "The price of the respirator"], 3,
     "p. 96, 'Protect Your Respiratory System'", "Formulation, application method, and environment decide the type.", "not"),
  tf("c06-s15-t4", "A nuisance dust mask is acceptable when a label requires a respirator.", False,
     "p. 97, 'Protect Your Respiratory System'", "Dust masks are not NIOSH-approved. Use a NIOSH-approved device listed on the label."),
  mc("c06-s15-t5", "Where are respirator approval certificates usually found?", [
     "On the pesticide label", "As package inserts with new respirators, cartridges, and filters", "Only on the NIOSH website", "From the state agency on request"], 1,
     "p. 96, 'Protect Your Respiratory System'", "Certificates are typically package inserts."),
])

# ---------- s16 ----------
card(16, "Types of respirators", [97, 97], [
  {"h": "Types of respirators"},
  {"p": [
    "The two classes of respirators most often required for protection from pesticide exposure are **atmosphere-supplying** and **air-purifying** respirators."]},
  {"p": [
    "**Atmosphere-supplying respirators** provide clean, breathable air from an uncontaminated source.",
    "Examples are airline respirators and self-contained breathing apparatus.",
    "In very specific uses, such as using **phosphide fumigants in enclosed areas**, the environment may be **immediately dangerous to life and health**.",
    "In these cases, the only kind of atmosphere-supplying respirators that may be used are either a **pressure-demand self-contained breathing apparatus (SCBA) with a full facepiece** or a **pressure-demand full facepiece air-line respirator with an SCBA escape bottle** for emergencies."]},
  {"gallery": ["p96-scba", "p96-suppliedair"]},
  {"p": [
    "**Air-purifying respirators (APRs)** remove contaminants from the air that you breathe.",
    "These respirators **do not supply oxygen** and should never be used in an environment that has limited oxygen or is immediately dangerous to life or health.",
    "Air-purifying respirators may be either powered or nonpowered."]},
  {"list": [
    "**Powered air-purifying respirators (PAPRs)** use a **blower** to pass contaminated air through purifying elements. PAPRs are available with a tight-fitting facepiece or a loose-fitting hood.",
    "**Nonpowered air-purifying respirators** have tight-fitting facepieces that seal directly to your face. There are single-use particulate-filtering facepiece respirators, and half-masks and full facepiece masks with replaceable purifying elements.",
    "**Gas masks**, which use **canisters instead of cartridges**, are one type of APR."]},
], [
  mc("c06-s16-t1", "You will apply a phosphide fumigant in an enclosed area that may be immediately dangerous to life and health. Which respirator may be used?", [
     "A half-mask chemical cartridge respirator",
     "A pressure-demand SCBA with a full facepiece, or a pressure-demand full facepiece air-line respirator with an SCBA escape bottle",
     "A PAPR with an HE filter",
     "A gas mask with an organic vapor canister"], 1,
     "p. 97, 'Types of Respirators'", "In conditions immediately dangerous to life and health, only those two atmosphere-supplying options may be used.", "scenario"),
  tf("c06-s16-t2", "Air-purifying respirators supply oxygen, so they are safe in low-oxygen spaces.", False,
     "p. 97, 'Types of Respirators'", "APRs do not supply oxygen. Never use them where oxygen is limited."),
  mc("c06-s16-t3", "Which of these is NOT an air-purifying respirator?", [
     "Powered air-purifying respirator (PAPR)", "Chemical cartridge half-mask", "Gas mask with canister", "Self-contained breathing apparatus (SCBA)"], 3,
     "p. 96-97, 'Types of Respirators'", "SCBA supplies its own air. It is atmosphere-supplying.", "not"),
  mc("c06-s16-t4", "What makes a PAPR \"powered\"?", [
     "A battery-heated facepiece", "A blower that passes contaminated air through purifying elements", "A compressed oxygen tank", "An electric filter that destroys pesticide"], 1,
     "p. 97, 'Types of Respirators'", "A blower moves air through the purifying elements."),
  mc("c06-s16-t5", "Gas masks are a type of APR that use:", [
     "Canisters instead of cartridges", "Compressed air", "Cloth filters only", "No purifying element"], 0,
     "p. 97, 'Types of Respirators'", "Gas masks use canisters instead of cartridges."),
], [
  img("p96-scba", "Self-contained breathing apparatus (SCBA).", "p. 96", "p96-scba"),
  img("p96-suppliedair", "Supplied-air respirator.", "p. 96", "p96-suppliedair"),
])

# ---------- s17 ----------
card(17, "Particulate filters: HE, N, R, and P", [97, 98], [
  {"h": "Purifying elements for air-purifying respirators"},
  {"p": [
    "When selected and used appropriately, purifying elements for air-purifying respirators remove specific contaminants from the air passing through them.",
    "The pesticide label specifies which type of purifying element is required.",
    "Elements that remove particulates (for example, dusts or sprays) are called **filters**, while vapor- and gas-removing elements are called either **chemical cartridges** or **chemical canisters**."]},
  {"h": "Particulate filters"},
  {"p": [
    "Particulate filters remove dusts, aerosols, or sprays suspended in the air that you breathe.",
    "Particulate filters **DO NOT remove gases or vapors**.",
    "The type of filter required on the pesticide label depends on whether the respirator is powered or nonpowered."]},
  {"list": [
    "**PAPR particulate filters** are rated **\"High Efficiency.\"** When a PAPR with a particulate filter is required, the pesticide label will specify this by the acronym **\"HE.\"**",
    "**Nonpowered APR particulate filters** are NIOSH-rated for three levels of oil degradation resistance (**N, R, and P**) and three levels of filter efficiency (**95, 99, and 100**). A higher efficiency rating means lower filter leakage."]},
  {"box": "Oil ratings", "list": [
    "**N**-series filters are **not oil-resistant**.",
    "**R**-series filters are **oil-resistant for up to eight hours**.",
    "**P**-series filters are **oil-proof**."]},
  {"p": [
    "For a nonpowered APR, the pesticide label specifies an N, R, or P filter to be used with your respirator.",
    "N-series filters must not be used with pesticide mixes that contain oil because the filter's efficiency may become degraded with use and fail to protect you.",
    "If you add an **adjuvant** to a tank mix, **do not use an N-series filter**, as the adjuvant may either contain oil or act like an oil.",
    "The pesticide label may also specify the filter efficiency (95, 99, or 100) needed.",
    "For example, if the pesticide label specified a filter efficiency of 100 for all three oil degradation ratings, you could select an N100, R100, or P100 filter.",
    "The class of the filter (such as N95) will be clearly marked on the filter, filter package, or respirator box."]},
  {"fig": "p98-papr"},
], [
  mc("c06-s17-r4", "When oil may be present, which particulate filter must be used?", [
     "N-series.", "P-series.", "Dust mask."], 1,
     "p. 98, 'Particulate Filters'", "N-series is not oil-resistant. P-series is oil-proof.", src="review"),
  mc("c06-s17-t1", "On a label, the acronym \"HE\" refers to:", [
     "A high efficiency particulate filter for a PAPR", "A half-mask respirator", "A heavy-duty organic vapor cartridge", "A hood with eye protection"], 0,
     "p. 97, 'Particulate Filters'", "HE means a High Efficiency filter for a powered APR."),
  mc("c06-s17-t2", "How long are R-series filters oil-resistant?", [
     "Up to one hour", "Up to four hours", "Up to eight hours", "Indefinitely"], 2,
     "p. 98, 'Particulate Filters'", "R: oil-resistant for up to eight hours. P: oil-proof."),
  mc("c06-s17-t3", "You add an adjuvant to the tank mix. Which filter series must you avoid?", [
     "N-series", "R-series", "P-series", "HE"], 0,
     "p. 98, 'Particulate Filters'", "An adjuvant may contain oil or act like an oil, so no N-series.", "scenario"),
  tf("c06-s17-t4", "Particulate filters remove gases and vapors as well as dusts and sprays.", False,
     "p. 97, 'Particulate Filters'", "Particulate filters DO NOT remove gases or vapors."),
  mc("c06-s17-t5", "In a rating like N95, what does a higher number mean?", [
     "More oil resistance", "Higher efficiency, meaning lower filter leakage", "Longer service life in hours", "A larger facepiece size"], 1,
     "p. 97, 'Particulate Filters'", "95, 99, 100 are efficiency levels. Higher means less leakage."),
], [
  img("p98-papr", "Powered air-purifying respirator (PAPR) with particulate filter (TC-21C).", "p. 98", "p98-papr"),
])

# ---------- s18 ----------
card(18, "Changing filters, and chemical cartridges", [98, 98], [
  {"h": "When to change particulate filters"},
  {"p": [
    "Always change particulate filters (HE, N, R, and P) for PAPR or nonpowered APR respirators whenever they are **damaged, torn, soiled, or it becomes too difficult to breathe**.",
    "As you use a particulate filter, pesticides load on its surface.",
    "Use caution when handling soiled filters.",
    "Once a particulate filter becomes dirty, **it cannot be cleaned**.",
    "To avoid spreading pesticide contamination to you or your respirator, discard particulate filters when they become soiled.",
    "EPA regulations require that you replace particulate filters according to respirator manufacturer recommendations or pesticide labeling (**whichever is more frequent**).",
    "If there are no other use directions, dispose of particulate filters at the end of **eight hours of cumulative use**."]},
  {"h": "Chemical cartridges or canisters"},
  {"p": [
    "Chemical cartridges or canisters use **sorbents** to remove contaminant-specific gases and vapors.",
    "**They do not remove particulates!**",
    "The most typical chemical cartridge or canister specified by the label for pesticide applications is an **organic vapor removing (OV)** cartridge or canister.",
    "Always use the type of chemical cartridge or canister purifying element required by the pesticide label!",
    "Keep purifying elements sealed until ready to use.",
    "Although it is not a requirement, some respirator manufacturers stamp the expiration date of purifying elements on the outside of the product package.",
    "Do not use a purifying element after the expiration date, **even if it was never opened**.",
    "The service life of a chemical cartridge or canister depends on the **type and concentration of pesticide, the user's breathing rate, and humidity**."]},
  {"p": [
    "Chemical cartridge respirators, when selected appropriately, are essentially 100% efficient until the gas or vapor breaks through.",
    "**Any taste, smell, or irritation indicates that breakthrough of the pesticide has occurred.**",
    "Cartridges should be changed immediately whenever you detect breakthrough in the mask.",
    "And once used, an organic vapor cartridge must be **disposed of at the end of the day**.",
    "The pesticide trapped by the sorbent in the cartridge may **desorb** very easily overnight.",
    "If you were to use the cartridge the next day, you could breathe in the desorbed pesticide vapors.",
    "Always dispose of chemical cartridges at the end of a workday unless the manufacturer directs otherwise."]},
  {"box": "Good working practice", "p": [
    "Make sure that the respirator protects you for the duration of use.",
    "Replace cartridges if necessary.",
    "Always dispose of chemical cartridges at the end of the workday unless the manufacturer directs otherwise and as allowed by state, tribe, or territory regulations."]},
  {"gallery": ["p98-halfface", "p98-gasmask"]},
], [
  mc("c06-s18-r3", "If there are no manufacturer use recommendations, a pesticide applicator should replace the chemical cartridges of his or her respirator:", [
     "At the end of each season.", "After one week of use.", "At the end of each workday."], 2,
     "p. 98, 'Chemical Cartridges or Canisters'", "Trapped pesticide can desorb overnight, so cartridges go at the end of each workday.", src="review"),
  mc("c06-s18-r5", "Air-purifying respirators protect applicators from pesticide exposure by:", [
     "Filtering and/or absorbing the pesticide.", "Breaking down the pesticide.", "Neutralizing the pesticide."], 0,
     "p. 97-98, 'Purifying Elements' and 'Chemical Cartridges or Canisters'", "Filters trap particulates and sorbents in cartridges take up vapors.", src="review"),
  mc("c06-s18-t1", "With no other use directions, particulate filters are disposed of after how much cumulative use?", [
     "Two hours", "Four hours", "Eight hours", "One week"], 2,
     "p. 98, 'Particulate Filters'", "Eight hours of cumulative use, absent other directions."),
  mc("c06-s18-t2", "Halfway through a job you notice a faint smell of the pesticide inside your mask with an organic vapor cartridge. What does that mean, and what do you do?", [
     "Normal. Finish the job.",
     "Breakthrough has occurred. Change the cartridges immediately.",
     "The filter is loaded. Tap it clean.",
     "The mask is too tight. Loosen the straps."], 1,
     "p. 98, 'Chemical Cartridges or Canisters'", "Any taste, smell, or irritation means breakthrough. Change cartridges now.", "scenario"),
  mc("c06-s18-t3", "Which of these does NOT affect the service life of a chemical cartridge?", [
     "Type and concentration of pesticide", "The user's breathing rate", "Humidity", "The color of the respirator"], 3,
     "p. 98, 'Chemical Cartridges or Canisters'", "Service life depends on pesticide type and concentration, breathing rate, and humidity.", "not"),
  tf("c06-s18-t4", "An unopened purifying element is fine to use after its expiration date.", False,
     "p. 98, 'Chemical Cartridges or Canisters'", "Do not use it after the expiration date, even if never opened."),
  mc("c06-s18-t5", "EPA requires replacing particulate filters according to:", [
     "The manufacturer's recommendations or the pesticide labeling, whichever is more frequent",
     "The manufacturer only",
     "Whatever schedule the applicator prefers",
     "The labeling or the manufacturer, whichever is less frequent"], 0,
     "p. 98, 'Particulate Filters'", "Whichever is more frequent."),
], [
  img("p98-halfface", "Half face mask chemical cartridge and particulate filter (TC-84A).", "p. 98", "p98-halfface",
      ["The labels point to the OV cartridge and the particulate filter on the side of the mask."]),
  img("p98-gasmask", "Gas mask with canister (TC-14G).", "p. 98", "p98-gasmask"),
])

# ---------- s19 ----------
card(19, "Combination cartridges and NIOSH TC numbers", [97, 99], [
  {"h": "Combination chemical cartridge and particulate filters"},
  {"p": [
    "The pesticide label may direct you to use both a chemical cartridge or canister and a particulate filter.",
    "You have two options."]},
  {"list": [
    "A chemical cartridge or canister with a disposable N, R, or P filter using a retaining ring.",
    "A single combination cartridge or canister."]},
  {"p": [
    "The combination chemical cartridge or canister for **nonpowered** air-purifying respirators will include **N-, R-, or P-rated** filters.",
    "The combination chemical cartridges for **powered** air-purifying respirators will include an **HE** filter.",
    "Follow the same change-out practices listed individually for particulate filters and chemical cartridges.",
    "For example, if you were using a combo chemical cartridge with a P100 filter and detected breakthrough in your mask, you would **change out your cartridges immediately** even though the filter was still useable."]},
  {"h": "Identifying the respirator type from the pesticide label"},
  {"p": [
    "The respiratory protection required by the pesticide label is **product- and task-specific**.",
    "The pesticide label will typically cite respiratory protection required using a NIOSH **\"TC\" (Testing and Certification)** designation.",
    "The NIOSH designations correspond to the types of respirators that may be specified by the pesticide label and include: TC-84A, TC-21C, TC-23C, TC-14G, TC-13F, and TC-19C."]},
  {"box": "NIOSH designations for respirators", "list": [
    "**TC-84A:** Filtering facepiece respirators (N, R, or P). APR with particulate filters (N, R, or P). APR with combination chemical cartridge and particulate filter (N, R, or P).",
    "**TC-21C:** Powered air-purifying respirator with particulate filter (HE).",
    "**TC-23C:** APR with chemical cartridges. PAPR with chemical cartridges. PAPR with combination chemical cartridge and particulate filter (HE).",
    "**TC-14G:** Gas mask with or without particulate filter (N, R, or P). Tight-fitting PAPR with gas canister with or without particulate filter (HE).",
    "**TC-13F:** Self-contained breathing apparatus. Supplied-air respirator with a self-contained escape bottle.",
    "**TC-19C:** Supplied-air respirator."]},
  {"box": "Sample pesticide label language", "p": [
    "Wear a NIOSH-approved respirator with an organic vapor (OV) cartridge with any combination N, R, or P filter with NIOSH approval number prefix TC-84A; or a NIOSH-approved powered air-purifying respirator with OV cartridge and combination HE filter with NIOSH approval number prefix TC-23C; or a NIOSH-approved gas mask with an OV canister with NIOSH approval number prefix TC-14G."]},
], [
  mc("c06-s19-t1", "What does \"TC\" stand for in a NIOSH designation such as TC-84A?", [
     "Toxic Control", "Testing and Certification", "Total Coverage", "Tight Contact"], 1,
     "p. 99, 'Identifying the Respirator Type from the Pesticide Label'", "TC means Testing and Certification."),
  mc("c06-s19-t2", "Which NIOSH designation is a self-contained breathing apparatus?", [
     "TC-84A", "TC-21C", "TC-13F", "TC-23C"], 2,
     "p. 99, 'NIOSH Designations for Respirators'", "TC-13F: SCBA, or supplied-air with a self-contained escape bottle."),
  mc("c06-s19-t3", "TC-21C is a:", [
     "Gas mask", "Powered air-purifying respirator with particulate filter (HE)", "Supplied-air respirator", "Filtering facepiece respirator"], 1,
     "p. 99, 'NIOSH Designations for Respirators'", "TC-21C is a PAPR with an HE particulate filter."),
  mc("c06-s19-t4", "You use a combination cartridge with a P100 filter and taste the pesticide in your mask. The filter looks clean. What do you do?", [
     "Keep working, since the filter is still useable",
     "Change out the cartridges immediately",
     "Swap only the filter",
     "Wait until the end of the day"], 1,
     "p. 99, 'Combination Chemical Cartridge and Particulate Filters'", "Breakthrough means change the cartridges now, even if the filter is fine.", "scenario"),
  mc("c06-s19-t5", "A combination cartridge for a powered air-purifying respirator will include which filter?", [
     "N95", "R99", "HE", "P100"], 2,
     "p. 99, 'Combination Chemical Cartridge and Particulate Filters'", "Powered: HE. Nonpowered: N, R, or P."),
  tf("c06-s19-t6", "The respiratory protection on a pesticide label is product- and task-specific.", True,
     "p. 99, 'Identifying the Respirator Type from the Pesticide Label'", "That is word for word from the manual."),
])

# ---------- s20 ----------
card(20, "Medical evaluation and fit tests", [99, 100], [
  {"h": "Use tight-fitting respirators properly"},
  {"p": [
    "Before selecting and using any respirator, get a **medical evaluation** to make sure wearing a respirator does not endanger your health.",
    "Next, read and understand the manufacturer's instructions and NIOSH approval certificate that accompany the respirator and its components.",
    "For full protection, conduct a **fit test** before wearing a tight-fitting particulate-filtering facepiece, half mask, or full-face mask.",
    "When wearing a tight-fitting respirator, nothing must interfere with the seal between the surface of the mask and your face, **including beards and stubble**."]},
  {"box": "Fit tests", "p": [
    "**Fit testing** is a method to select the right size and type of tight-fitting respirator for your face.",
    "Perform a qualitative or quantitative fit test of a given mask type on a user's face to select the best-fitting respirator.",
    "It is important to get a fit test **annually** and **whenever you use a different respirator facepiece**.",
    "Get fit tested again whenever something physically changes that could affect the fit of your respirator (for example, **facial scarring, dental work, cosmetic surgery, or a significant change in body weight**).",
    "A respirator cannot protect you from pesticide exposure if it does not fit your face."]},
  {"list": [
    "**Qualitative fit test:** a method that uses a **test agent** outside the mask to check for leakage at the seal to the face. Kits for qualitative testing are available and easy to use.",
    "**Quantitative fit test:** a method that uses **instrumentation** to numerically measure leakage into the respirator."]},
  {"fig": "p99-fittest"},
], [
  mc("c06-s20-r6", "You should do a qualitative fit test of your respirator:", [
     "Every five years.", "Semiannually.", "If you have a significant change in weight."], 2,
     "p. 99-100, 'Fit Tests'", "Refit whenever something physical changes, such as a significant weight change. Routine tests are annual.", src="review"),
  mc("c06-s20-t1", "What should you do before selecting and using any respirator?", [
     "Get a medical evaluation", "Buy two of them", "Shave your head", "Test it with the pesticide"], 0,
     "p. 99, 'Use Tight-Fitting Respirators Properly'", "First a medical evaluation, then read the instructions and certificate."),
  mc("c06-s20-t2", "How often should you get a fit test, at a minimum?", [
     "Annually", "Every five years", "Only once", "Every day"], 0,
     "p. 99, 'Fit Tests'", "Annually, plus any time you change facepieces or your face changes."),
  mc("c06-s20-t3", "Which kind of fit test uses instrumentation to numerically measure leakage?", [
     "Qualitative", "Quantitative", "Positive-pressure seal check", "Negative-pressure seal check"], 1,
     "p. 100, 'Fit Tests'", "Quantitative uses an instrument. Qualitative uses a test agent outside the mask."),
  mc("c06-s20-t4", "Which of these is NOT listed as a reason to get fit tested again?", [
     "Dental work", "Facial scarring", "Cosmetic surgery", "A new pair of boots"], 3,
     "p. 99-100, 'Fit Tests'", "Retest for physical changes that affect fit: scarring, dental work, surgery, weight.", "not"),
  mc("c06-s20-t5", "An applicator has two days of stubble and wants to wear a half-mask respirator. What does the manual say?", [
     "Stubble is fine. Only full beards matter.",
     "Nothing must interfere with the seal, including beards and stubble",
     "Use extra strap tension to compensate",
     "Stubble only matters for full-face masks"], 1,
     "p. 99, 'Use Tight-Fitting Respirators Properly'", "Beards and stubble break the seal.", "scenario"),
], [
  img("p99-fittest", "In a quantitative fit test, a particle-counting instrument is used to measure respirator fit.", "p. 99", "p99-fittest"),
])

# ---------- s21 ----------
card(21, "Seal checks, and when to use a PAPR", [100, 100], [
  {"box": "User seal checks for tight-fitting respirators", "p": [
    "Perform either a positive or negative user seal check, **preferably both, every time you put on your mask** to make sure that it is properly seated on your face.",
    "This also ensures that all inhalation and exhalation valves are functioning properly."]},
  {"list": [
    "**Positive-pressure user seal check:** Cover the **exhalation port** with the palm of your hand and lightly **exhale** into the mask. You will feel air escaping through any gaps in your seal. Readjust the mask until there is no leakage.",
    "**Negative-pressure user seal check:** Cover or seal off the surface or hose where air is **inhaled** and **suck in**. If your mask is properly sealed, it should **collapse on your face** with no signs of leakage in the facepiece or hoses. If you cannot get a seal, readjust the mask until there is no leakage."]},
  {"fig": "p100-sealcheck"},
  {"p": [
    "If you cannot get a proper fit with a tight-fitting respirator, you can use a **PAPR with a loose-fitting helmet or hoodlike head covering** that does not have to form a seal on your face.",
    "**PAPRs do not need a fit test, and people with facial hair can use them.**"]},
  {"p": [
    "Always consult the pesticide label for the appropriate respirator and purifying elements.",
    "If you have any questions about your respirator, consult the manufacturer or use online resources.",
    "Be sure to review the manufacturer approved labels for use limitations of the respirator.",
    "Contact your Cooperative Extension pesticide safety education program or your state, tribal, territorial, or federal safety and health agency for help in selecting the correct respirator and any of its component parts."]},
], [
  mc("c06-s21-r7", "Every time you wear any tight-fitting respirator to apply pesticides, you should first:", [
     "Perform seal check(s).", "Do a qualitative fit test.", "Put Vaseline® on the edges of the respirator to enhance the seal."], 0,
     "p. 100, 'User Seal Checks for Tight-Fitting Respirators'", "Seal checks every time you put the mask on. Fit tests are annual.", src="review"),
  mc("c06-s21-t1", "In a positive-pressure user seal check, you:", [
     "Cover the exhalation port with your palm and lightly exhale",
     "Cover the inhalation surfaces and suck in",
     "Spray a test agent outside the mask",
     "Hook the mask to a particle counter"], 0,
     "p. 100, 'User Seal Checks'", "Positive: block exhalation port, breathe out, feel for leaks."),
  mc("c06-s21-t2", "During a negative-pressure seal check, what tells you the mask is properly sealed?", [
     "Air escapes at the chin", "The mask collapses on your face with no leakage", "You smell the test agent", "The valves click"], 1,
     "p. 100, 'User Seal Checks'", "Suck in with inlets covered: a sealed mask collapses onto your face."),
  mc("c06-s21-t3", "A worker has a full beard and cannot get a seal with a half-mask. What does the manual offer?", [
     "Tighten the straps",
     "A PAPR with a loose-fitting helmet or hoodlike covering, which needs no fit test",
     "Skip the respirator if the label allows goggles",
     "A nuisance dust mask"], 1,
     "p. 100, 'User Seal Checks'", "Loose-fitting PAPRs need no seal, no fit test, and work with facial hair.", "scenario"),
  tf("c06-s21-t4", "A seal check is the same thing as a fit test.", False,
     "p. 99-100, 'Fit Tests' and 'User Seal Checks'", "A fit test picks the right mask (annually). A seal check confirms it is seated each time you put it on."),
  mc("c06-s21-t5", "Besides checking the seal, a user seal check also makes sure that:", [
     "The cartridges are not expired", "All inhalation and exhalation valves are functioning properly", "The filter is the right N, R, or P series", "The label allows the respirator"], 1,
     "p. 100, 'User Seal Checks'", "It also confirms the valves work."),
], [
  img("p100-sealcheck", "Be sure to perform a seal check each time you use your respirator.", "p. 100", "p100-sealcheck",
      ["The top drawing shows a positive pressure seal check: a palm covering the exhalation port.",
       "The bottom drawing shows a negative pressure seal check: both palms covering the cartridges."]),
])

# ---------- s22 ----------
card(22, "Washing work clothes and coveralls", [100, 101], [
  {"h": "Maintaining clothing and personal protective equipment"},
  {"p": [
    "At the end of each workday, **wash all work clothes and PPE**.",
    "Some items, such as clothes and coveralls, can be washed using a washer and dryer.",
    "Other items, such as gloves, protective suits, goggles, aprons, boots, and eyewear, require **hand washing**.",
    "Wear protective gloves when handling contaminated items.",
    "Rinse and discard disposable items.",
    "Dispose of any nonreusable contaminated item carefully to prevent cross-contamination or contamination of others who might handle the discarded item.",
    "Dispose of heavily contaminated items as **household hazardous waste**."]},
  {"h": "Woven work clothes and coveralls"},
  {"p": [
    "Launder fabric coveralls and work clothing **after each day's use**.",
    "Some commonsense guidelines for cleaning pesticide-soiled clothing follow."]},
  {"ol": [
    "Outdoors, shake any dry material from cuffs and pockets and then hang garments to air them out.",
    "Wash work clothes and coveralls worn when handling pesticides **separately from other laundry**.",
    "Load only a few items into the washing machine so there is plenty of agitation and water for dilution.",
    "Use **hot water** and the **highest water level**.",
    "Prerinse items by using the prewash cycle.",
    "Use **heavy-duty liquid detergent**.",
    "Run the washer on the **longest wash cycle**. Use **two entire machine cycles** for lightly or moderately contaminated items.",
    "Properly handle and discard heavily contaminated clothing.",
    "Line dry laundered items outdoors if possible.",
    "Run **one additional empty cycle** without clothing, using detergent and hot water, before using the washer for your household laundry."]},
  {"p": [
    "If using a laundry service, notify them the clothing may be contaminated with pesticides.",
    "**Never wash** any garments made of absorbent materials that have been splashed or soaked with **undiluted pesticide** or large quantities of diluted pesticide.",
    "Remember to remove them immediately and dispose of them carefully."]},
  {"gallery": ["p100-wash", "p101-dispose"]},
], [
  mc("c06-s22-r8", "Which statement about washing work clothes soaked with a pesticide concentrate is true?", [
     "Use cold water and one wash cycle.", "Wash separately from other laundry items.", "Do not attempt to wash it. Dispose of it immediately."], 2,
     "p. 101, 'Woven Work Clothes and Coveralls'", "Never wash absorbent garments soaked with undiluted pesticide. Remove and dispose of them.", src="review"),
  mc("c06-s22-r9", "Work clothes worn to apply pesticides should be laundered with a suitable detergent:", [
     "After each day's use.", "After they get wet with spray.", "When they have a strong odor like the pesticide."], 0,
     "p. 100, 'Woven Work Clothes and Coveralls'", "Launder fabric coveralls and work clothing after each day's use.", src="review"),
  mc("c06-s22-t1", "Which water setting does the manual call for when washing pesticide-soiled clothing?", [
     "Cold water, low level", "Warm water, medium level", "Hot water, highest water level", "Any setting with bleach"], 2,
     "p. 101, 'Woven Work Clothes and Coveralls'", "Hot water and the highest water level."),
  mc("c06-s22-t2", "Which detergent does the manual name?", [
     "Powdered detergent", "Heavy-duty liquid detergent", "Dish soap", "Any detergent with fabric softener"], 1,
     "p. 101, 'Woven Work Clothes and Coveralls'", "Heavy-duty liquid detergent."),
  mc("c06-s22-t3", "You just finished washing your spray clothes at home. Before washing the family's laundry, you should:", [
     "Wipe the drum with a towel",
     "Run one additional empty cycle with detergent and hot water",
     "Nothing, the rinse cycle cleaned it",
     "Leave the lid open overnight"], 1,
     "p. 101, 'Woven Work Clothes and Coveralls'", "One empty hot cycle with detergent clears the washer.", "scenario"),
  mc("c06-s22-t4", "Which of these is NOT one of the manual's laundering guidelines?", [
     "Shake dry material from cuffs and pockets outdoors",
     "Load only a few items at a time",
     "Line dry outdoors if possible",
     "Wash pesticide clothes with towels to add agitation"], 3,
     "p. 100-101, 'Woven Work Clothes and Coveralls'", "Pesticide clothes always go separately from other laundry.", "not"),
  mc("c06-s22-t5", "For lightly or moderately contaminated items, how many machine cycles does the manual call for?", [
     "One", "Two entire cycles", "Three", "Only a prewash"], 1,
     "p. 101, 'Woven Work Clothes and Coveralls'", "Longest wash cycle, two entire machine cycles."),
  mc("c06-s22-t6", "Heavily contaminated items that cannot be reused should be disposed of as:", [
     "Regular trash", "Household hazardous waste", "Recycling", "Compost"], 1,
     "p. 100, 'Maintaining Clothing and Personal Protective Equipment'", "Heavily contaminated items go out as household hazardous waste."),
], [
  img("p100-wash", "Wash pesticide-contaminated items separately from other laundry.", "p. 100", "p100-wash"),
  img("p101-dispose", "Discard contaminated PPE in the appropriate container.", "p. 101", "p101-dispose",
      ["The drawing shows a gloved worker dropping a garment into a can marked \"Dispose of PPE here.\""]),
])

# ---------- s23 ----------
card(23, "Caring for nonwoven garments, boots, gloves, eyewear, and respirators", [101, 102], [
  {"h": "Nonwoven clothing"},
  {"p": [
    "Coveralls may be either a one-day disposable item or a reusable garment.",
    "For reusables, make sure to check the PPE manufacturer's use limitations and laundering instructions.",
    "Replace these garments regularly and at any sign of wear.",
    "If any PPE cannot be cleaned properly, dispose of it according to applicable federal, state, tribal, and local regulations.",
    "Follow manufacturers' instructions, if any, for the service life of reusable nonwoven garments.",
    "Pay close attention when reusing these items, and be ready to change them whenever you think that the inside surface may be contaminated.",
    "If using disposable garments, **render them unusable and discard**.",
    "If they are heavily contaminated with high-risk pesticides, handle them appropriately and take them to a **household hazardous waste facility**."]},
  {"h": "Boots and gloves"},
  {"p": [
    "Be sure to clean boots and gloves, **even if they are worn only briefly**.",
    "Before taking your gloves off, wash them thoroughly.",
    "Wash both the **inside and outside** of boots and gloves once removed.",
    "Inspect these items and discard if there is any sign of wear or if they leak.",
    "Hang or leave to dry.",
    "Gloves are not designed to be reused over and over again. Replace them often to ensure protection of your hands.",
    "Properly cared for, boots should last multiple seasons.",
    "**Sun will degrade rubber materials quickly**, so store gloves and boots out of the sun."]},
  {"h": "Eyewear and respirators"},
  {"p": [
    "Most eyewear, respirator bodies, facepieces, and helmets are designed to be cleaned and reused.",
    "These items can last many years if they are good quality and are maintained according to the manufacturer's directions.",
    "**Respirators require more maintenance than most PPE.**",
    "When you have finished using your respirator, remove and properly dispose of any expendable components, such as filters, cartridges, or canisters.",
    "Wash the facepiece according to the respirator manufacturer's directions.",
    "Take care to clean under and around gaskets and valves. Allow to air dry.",
    "Store cleaned respirators, as well as replacement purifying elements, in a **clean, dry place that is not exposed to sunlight or extreme temperatures**.",
    "Make sure the rubber facepiece is not distorted when stored so that it maintains its shape.",
    "**Do not store any protective equipment, including respirators, with or near pesticides or other chemicals.**"]},
  {"fig": "p102-clean"},
], [
  mc("c06-s23-t1", "Why store rubber gloves and boots out of the sun?", [
     "Sun makes them sticky", "Sun will degrade rubber materials quickly", "Sun activates pesticide residues", "It is a WPS rule for storage sheds"], 1,
     "p. 101, 'Boots and Gloves'", "Sunlight breaks down rubber quickly."),
  mc("c06-s23-t2", "What should you do with used disposable garments?", [
     "Wash and reuse them once", "Render them unusable and discard", "Give them to coworkers", "Store them with the pesticides"], 1,
     "p. 101, 'Nonwoven Clothing'", "Render disposables unusable, then discard."),
  mc("c06-s23-t3", "At the end of the day you are putting your respirator away. Which of these is NOT correct?", [
     "Remove and dispose of the cartridges and filters",
     "Clean under and around gaskets and valves, then air dry",
     "Store it so the rubber facepiece is not distorted",
     "Store it on the shelf in the pesticide storage room so it is handy"], 3,
     "p. 102, 'Eyewear and Respirators'", "Never store PPE, including respirators, with or near pesticides.", "not"),
  tf("c06-s23-t4", "Boots and gloves worn only briefly do not need cleaning.", False,
     "p. 101, 'Boots and Gloves'", "Clean boots and gloves even if worn only briefly."),
  mc("c06-s23-t5", "Where should cleaned respirators and replacement purifying elements be stored?", [
     "In the truck cab", "In a clean, dry place not exposed to sunlight or extreme temperatures", "In the pesticide storage room", "In a sealed bag with the used cartridges"], 1,
     "p. 102, 'Eyewear and Respirators'", "Clean, dry, out of sunlight and extreme temperatures."),
  mc("c06-s23-t6", "You reuse a nonwoven coverall and suspect the inside surface got contaminated. What does the manual say?", [
     "Turn it inside out and keep using it", "Be ready to change it whenever you think the inside may be contaminated", "Wash it with household laundry", "Keep it until the manufacturer's service life runs out"], 1,
     "p. 101, 'Nonwoven Clothing'", "Change reusable nonwovens whenever the inside may be contaminated.", "scenario"),
], [
  img("p102-clean", "Clean goggles, face shields, and respirator bodies and facepieces in detergent and hot water.", "p. 102", "p102-clean"),
])

# ---------- s24 ----------
card(24, "Chapter 6 summary", [102, 102], [
  {"h": "Summary"},
  {"p": [
    "Wearing PPE can reduce the potential for dermal, inhalation, ocular, and oral exposure, thereby lowering the chances of pesticide injury, illness, or poisoning.",
    "Consult the pesticide label for the **minimum PPE required by law**.",
    "In order to appropriately select and wear PPE, you must understand both its **protections and its limitations**.",
    "Then determine what protective equipment you need for the pesticide task at hand.",
    "Personal protective equipment reduces your exposure to pesticides but does not necessarily eliminate it.",
    "Maximize your safety by following certain good work practices when using pesticides."]},
  {"p": [
    "Contact your Cooperative Extension pesticide safety education program for assistance in the selection, use, and maintenance of PPE for handling pesticides.",
    "Check the \"Agricultural Use Requirements\" box on the label and the WPS requirements for any other statements about PPE use in farms, forests, nurseries, or greenhouses."]},
  {"box": "Personal hygiene", "p": [
    "**Personal hygiene is critical.**",
    "Wash your hands every time you remove your gloves.",
    "Shower at the end of the day."]},
], [
  mc("c06-s24-t1", "Where do you find the minimum PPE required by law for a product?", [
     "The pesticide label", "The dealer's catalog", "The manufacturer's website", "Your coworkers"], 0,
     "p. 102, 'Summary'", "The label sets the legal minimum PPE."),
  mc("c06-s24-t2", "The manual's personal hygiene box says to wash your hands:", [
     "Once at the end of the day", "Every time you remove your gloves", "Only if you feel exposed", "Before putting on gloves only"], 1,
     "p. 102, 'Summary' box", "Wash hands every time gloves come off, and shower at the end of the day."),
  mc("c06-s24-t3", "You manage a nursery crew and want help choosing respirators and gloves. Who does the manual tell you to contact?", [
     "The pesticide dealer only", "Your Cooperative Extension pesticide safety education program", "The EPA hotline", "The local fire department"], 1,
     "p. 102, 'Summary'", "Cooperative Extension pesticide safety education helps with PPE selection, use, and maintenance.", "scenario"),
  mc("c06-s24-t4", "Which of these is NOT a route of exposure that PPE reduces, according to the summary?", [
     "Dermal", "Inhalation", "Ocular", "Genetic"], 3,
     "p. 102, 'Summary'", "Dermal, inhalation, ocular, and oral.", "not"),
])

def addq(sid, q):
    for s in S:
        if s["id"] == sid: s["questions"].append(q); return
    raise KeyError(sid)
addq("c06-s17", mc("c06-s17-t6", "Which of these is NOT one of the three NIOSH filter efficiency levels for nonpowered APR filters?", [
     "95", "99", "100", "50"], 3,
     "p. 97, 'Particulate Filters'", "The levels are 95, 99, and 100. A higher rating means lower filter leakage.", "not"))
addq("c06-s19", mc("c06-s19-t7", "Which of these is NOT one of the NIOSH designations the manual lists?", [
     "TC-84A", "TC-23C", "TC-19C", "TC-50X"], 3,
     "p. 99, 'Identifying the Respirator Type from the Pesticide Label'", "Listed: TC-84A, TC-21C, TC-23C, TC-14G, TC-13F, and TC-19C.", "not"))
addq("c06-s21", mc("c06-s21-t6", "Which statement about a PAPR with a loose-fitting helmet or hood is NOT true?", [
     "It does not have to form a seal on your face", "It does not need a fit test", "People with facial hair can use it", "It must be fit tested annually"], 3,
     "p. 100, 'User Seal Checks'", "Loose-fitting PAPRs need no fit test.", "not"))

BYID = {s["id"]: s for s in S}
DROP = {"c06-s17-t5", "c06-s19-t3", "c06-s21-t5", "c06-s03-t4", "c06-s14-t4", "c06-s19-t6", "c06-s22-t2", "c06-s23-t4",
        "c06-s06-t2", "c06-s06-t4", "c06-s07-t4", "c06-s07-t5",
        "c06-s08-t2", "c06-s08-t3", "c06-s08-t5", "c06-s09-t2", "c06-s09-t4",
        "c06-s12-t2", "c06-s12-t4", "c06-s12-t5", "c06-s13-t3", "c06-s13-t4", "c06-s13-t5"}
MERGE = {"c06-s06": ("c06-s07", "Work clothing and coveralls"),
         "c06-s08": ("c06-s09", "Aprons, headgear, and footwear"),
         "c06-s12": ("c06-s13", "Gloves: what to avoid, fit, and good practices")}
out = []
skip = set()
for s in S:
    if s["id"] in skip: continue
    if s["id"] in MERGE:
        other, title = MERGE[s["id"]]; o = BYID[other]; skip.add(other)
        s = dict(s, title=title, pages=[s["pages"][0], o["pages"][1]], body=s["body"] + o["body"],
                 figures=s.get("figures", []) + o.get("figures", []), questions=s["questions"] + o["questions"])
        if not s["figures"]: del s["figures"]
    out.append(s)
for i, s in enumerate(out, 1):
    sid = f"c06-s{i:02d}"
    qs = [q for q in s["questions"] if q["id"] not in DROP]
    rev = [q for q in qs if q["src"] == "review"]; tst = [q for q in qs if q["src"] == "test"]
    assert 3 <= len(tst) <= 5, (sid, len(tst))
    for q in rev: q["id"] = sid + "-" + q["id"].split("-")[-1]
    for k, q in enumerate(tst, 1): q["id"] = f"{sid}-t{k}"
    q = s.pop("questions"); figs = s.pop("figures", None)
    s["id"] = sid
    s = {"id": sid, **{k: v for k, v in s.items() if k != "id"}}
    if figs: s["figures"] = figs
    s["questions"] = rev + tst
    out[i - 1] = s
res = {"chapter": CH, "pages": [89, 103], "sections": out}
p = pathlib.Path("/home/user/Studdy-Pest-Applicators-/content/chapters/ch06.json")
p.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(out), "cards", sum(len(s["questions"]) for s in out), "questions")
for s in out:
    print(s["id"], s["pages"], s["title"], [q["id"].split("-")[-1] + (":" + q.get("style", "")[:1] if q.get("style") else "") for q in s["questions"]])
