"""
In this file you will define your protocols. Each protocol should have a name, a list of annotations and a list of times.

The code looks as follows:
    protocols = {
        "Protocol_name": {
            "annotations": ["annotation1", "annotation2", "annotation3", ...],
            "times": [Interval1, Interval2, Interval3, ...] #how long a certain segment accompanying the annotation should last.
        }
    }
"""

#Define your protocols here
protocols = {
    "Standaard_protocol": {
        "annotations": ["baseline", "2 min stilstaan", "eerste oefening", "stilstaan 1", "tweede oefening",
                        "stilstaan 2", "derde oefening", "stilstaan 3", "einde"],
        "times": [300, 120, 300, 60, 300, 60, 60, 60, 0]
    },
    "Supersnel_protocol": {
        "annotations": ["baseline", "2 min stilstaan", "eerste oefening", "stilstaan 1", "tweede oefening",
                        "stilstaan 2", "derde oefening", "stilstaan 3", "einde"],
        "times": [10, 9, 8, 7, 6, 5, 4, 3, 2]
    }
}