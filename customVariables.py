"""
Author: Quinn Cabooter
Date: 14-01-2025
Last updated: 15-01-2025

In this file you will define your protocols, garment types and inner garment types. Each protocol should have a name, a list of annotations and a list of times. 

"""

#Define your protocols here
protocols = {#Protocol used when you want to test the functionality of the python script.
    # Standard protocol used in bodybox with the 3 exercises of 5 minutes

    "Standaard": {  # Name of the protocol
        "annotations": ["baseline", "2_min_stilstaan", "eerste_oefening", "stilstaan_1", "tweede_oefening",
                        "stilstaan_2", "derde_oefening", "stilstaan_3", "einde"],  # List of annotations
        "times": [120, 120, 300, 60, 300, 60, 60, 60, 0]  # List of times in seconds
    },

    "Custom": {
        "annotations": ["baseline", "2_min_stilstaan", "eerste_oefening", "stilstaan_1", "tweede_oefening",
                        "stilstaan_2", "derde_oefening", "stilstaan_3", "einde"],
        "times": [1, 1, 1, 1, 1, 1, 1, 1, 1]
    },
    "Supersnel": {
        "annotations": ["baseline", "2_min_stilstaan", "eerste_oefening", "stilstaan_1", "tweede_oefening",
                        "stilstaan_2", "derde_oefening", "stilstaan_3", "einde"],
        "times": [1, 1, 1, 1, 1, 1, 1, 1, 1]
    },
}

#Define your garment types here
garments = [ "Garment1", "Garment2", "Garment3" ]
inner_garments = [ "InnerGarment1", "InnerGarment2", "InnerGarment3" ]
goggle_types = [ "Goggle1", "Goggle2", "Goggle3" ]
fabric_types = [ "Fabric1", "Fabric2", "Fabric3" ]

