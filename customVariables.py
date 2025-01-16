"""
Author: Quinn Cabooter
Date: 14-01-2025
Last updated: 15-01-2025

In this file you will define your protocols, garment types and inner garment types. Each protocol should have a name, a list of annotations and a list of times. 

"""

TODO: Add goggle types


#Define your protocols here
protocols = {
    #Standard protocol used in bodybox with the 3 exercises of 5 minutes
    "Standaard_protocol": { #Name of the protocol
        "annotations": ["baseline", "2_min_stilstaan", "eerste_oefening", "stilstaan_1", "tweede_oefening",
                        "stilstaan_2", "derde_oefening", "stilstaan_3", "einde"], #List of annotations
        "times": [300, 120, 300, 60, 300, 60, 60, 60, 0] #List of times in seconds
    },

    #Protocol used when you want to test the functionality of the python script.
    "Supersnel_protocol": {
        "annotations": ["baseline", "2_min_stilstaan", "eerste_oefening", "stilstaan_1", "tweede_oefening",
                        "stilstaan_2", "derde_oefening", "stilstaan_3", "einde"],
        "times": [1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
}

#Define your garment types here
garments = [ "Garment1", "Garment2", "Garment3" ]
inner_garments = [ "InnerGarment1", "InnerGarment2", "InnerGarment3" ]

