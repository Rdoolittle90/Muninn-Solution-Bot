sql_select_affiliations = \
"""
SELECT 
    DM.Name, O.Name, OM.MemberRank, OM.Stars
FROM
    affiliations AF
        INNER JOIN
    discordmembers DM ON DM.PID = AF.PID
        INNER JOIN
    orgmembers OM ON OM.MID = AF.MID
        INNER JOIN
    orgs O ON O.SID = OM.SID
ORDER BY O.SID , OM.Stars DESC;
"""
