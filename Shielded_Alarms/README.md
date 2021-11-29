Problem:Alarms that is shielded locally on LTE sites by Field workers cannot be detected by Monitring systems. 

Solution:-created MML command script that runs on LTE nodes to unshield all alarms.
         -used Regex patterns to detect shielded alarms.
         -raise alarm by detected alarms on monitring system and send it to monitring team by SMS.

Technolgies:-CentOS
            -Regex
            -Python
            -urllib
            -Pandas