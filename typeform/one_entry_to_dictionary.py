def one_entry_to_dictionary(person):
    '''
    transforms JSON from Typescript into dictionary
    '''

    # declare empty dictionary to save no-entries with "0"
    d = {
    "id": 0,
    "submitted_at": 0,
    "gender": 0,
    "age": 0,
    "ethnicity": 0,
    "live_alone": 0,
    "live_friends": 0,
    "live_partner": 0,
    "live_parents": 0,
    "live_siblings": 0,
    "live_otherfamily": 0,
    "live_children": 0,
    "live_other": 0,
    "location": 0,
    "safety_level": 0,
    "safety_change": 0,
    "safety_why": 0,
    "mental_scale": 0,
    "mental_problems_repetitive": 0,
    "mental_problems_lonely": 0,
    "mental_problems_stressed": 0,
    "mental_problems_anxious": 0,
    "mental_problems_worriedhealth": 0,
    "mental_problems_scaredfuture": 0,
    "mental_problems_relationship": 0,
    "mental_problems_other": 0,
    "mental_problems_none": 0,
    "positive_impact_support_housework" : 0,
    "positive_impact_support_childcare" : 0,
    "positive_impact_connect" : 0,
    "positive_impact_leisure" : 0,
    "positive_impact_wfh" : 0,
    "positive_impact_other" : 0,
    "positive_impact_none" : 0,
    "work_situation": 0,
    "financial_situation": 0,
    "housework_amount": 0,
    "housework_change": 0,
    "testimonial" : 0
    }

    d["id"] = person["landing_id"]
    d['submitted_at'] = person["submitted_at"]

    for entry in person["answers"]:
    

        
        if entry["field"]["id"] == "Xa2T0bcZ5VnY":
            d["gender"] = entry["choice"]["label"]

        elif entry["field"]["id"] == "QUtA6k0gcrZf":
            d["age"] = entry["choice"]["label"]

        elif entry["field"]["id"] == "ZNZyNVwMtwID":
            d["ethnicity"] = entry["choice"]["label"]

        #"who do you live with"
        elif entry["field"]["id"] == "azlKRkvdcc7O":

            for label in entry["choices"]["labels"]:

                if label == "Alone":
                    d["live_alone"] = 1

                if label == "With friend(s) / housemates":
                    d["live_friends"] = 1

                if label == "My partner":
                    d["live_partner"] = 1

                if label == "My parent(s) / caregivers":
                    d["live_parents"] = 1

                if label == "My siblings":
                    d["live_siblings"] = 1

                if label == "Other family members (e.g. grandparents, aunts, cousins)":
                    d["live_otherfamily"] = 1

                if label == "My children":
                    d["live_children"] = 1

                if label == "Other":
                    d["live_other"] = 1


        elif entry["field"]["id"] == "Vrzj2uv0i29C":
            d["location"] = entry["text"]

        elif entry["field"]["id"] == "Xh2W1d6FhXyK":
            d["safety_level"] = entry["number"]

        elif entry["field"]["id"] == "t9EaTsONnJfR":
            d["safety_change"] = entry["choice"]["label"]

        elif entry["field"]["id"] == "OaujoVSY6NaS":
            d["safety_why"] = entry["text"]

        elif entry["field"]["id"] == "ASolp4v3adZK":
            d["mental_scale"] = entry["number"]

        #list of mental problems 
        elif entry["field"]["id"] == "erHBE6gKxycf":

            for label in entry["choices"]["labels"]:
                if label == "It has been repetitive / boring":
                    d["mental_problems_repetitive"] = 1

                if label == "I feel lonely" : 
                    d["mental_problems_lonely"] = 1

                if label == "I feel stressed" :
                    d["mental_problems_stressed"] = 1

                if label == "I feel anxious" :
                    d["mental_problems_anxious"] = 1

                if label == "I feel worried about my health" :
                    d["mental_problems_worriedhealth"] = 1

                if label == "I feel scared about the future" :
                    d["mental_problems_scaredfuture"] = 1

                if label == "I’m having conflicts in my relationship" :
                    d["mental_problems_relationship"] = 1

                if label == "Other" :
                    d["mental_problems_other"] = 1

                if label == "None" :
                    d["mental_problems_none"] = 1


        # LIST OF POSITIVE IMPACTS
        elif entry["field"]["id"] == "ASQmq4h3vxRt":
            for label in entry["choices"]["labels"]:
                if label == "I have had more support in my daily tasks in the house" :
                        d["positive_impact_support_housework"] == 1

                if label == "I have had more support in my childcare responsibilities" :
                        d["positive_impact_support_childcare"] == 1

                if label == "I have had more time to connect with loved ones" :
                        d["positive_impact_connect"] == 1

                if label == "I have more time for leisure, e.g. to explore new activities, develop skills" :
                        d["positive_impact_leisure"] == 1

                if label == "I have enjoyed working from home" :
                        d["positive_impact_wfh"] == 1

                if label == "Other" :
                        d["positive_impact_other"] == 1

                if label == "None" :
                        d["positive_impact_none"] == 1


        elif entry["field"]["id"] == "KEGztC8iYfyy":
            # here we have a OTHER that can be filled
            if "label" in entry["choice"]:
                d["work_situation"] = entry["choice"]["label"]
            if "other" in entry["choice"]:
                d["work_situation"] = "other"
                print(person["landing_id"],"has entered in column other_work:",entry["choice"]["other"],"// THIS ENTRY WAS DISCARDED AND SAVED AS OTHER" )

        elif entry["field"]["id"] == "kWb7LUjdJyhb":
            d["financial_situation"] = entry["choice"]["label"]

        elif entry["field"]["id"] == "g9goY6hIxmC9":
           
            d["housework_amount"] = entry["choice"]["label"]

        elif entry["field"]["id"] == "jG2wzvAmOWxq":
            if "label" in entry["choice"]:
                d["housework_change"] = entry["choice"]["label"]

        elif entry["field"]["id"] == "HNqA7BK7ZDFl":
            d["testimonial"] = entry["text"]

    return d