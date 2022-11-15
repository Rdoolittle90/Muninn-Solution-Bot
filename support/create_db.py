import mysql.connector

from os import getenv
from dotenv import load_dotenv



def create_db():
    """ Check to see if the database has already been setup if not.. set it up. """

    load_dotenv()
    mydb = mysql.connector.connect(
                host=getenv("SQL_HOST"),
                user=getenv("SQL_USER"),
                passwd=getenv("SQL_PASSWORD"),
                database=getenv("SQL_DB")
            )

    mycursor = mydb.cursor()

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS discordusers (
            DUID BIGINT NOT NULL UNIQUE,
            Name VARCHAR(30),
            Nick VARCHAR(30),
            Image VARCHAR(200),
            PRIMARY KEY (DUID)
        )
        """)
    
    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS scusers (
            UID INT NOT NULL AUTO_INCREMENT UNIQUE,
            DUID BIGINT,
            Handle VARCHAR(50) NOT NULL UNIQUE,
            Badge VARCHAR(50),
            Enlisted DATETIME NOT NULL,
            Image VARCHAR(200),
            PRIMARY KEY (UID, Handle),
            FOREIGN KEY (DUID) REFERENCES discordusers(DUID)
        )
        """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS orgs (
            SID VARCHAR(25) NOT NULL UNIQUE,
            Name VARCHAR(50) NOT NULL UNIQUE,
            Logo VARCHAR(200) NOT NULL,
            URL VARCHAR(200) NOT NULL,
            MemberCount MEDIUMINT,
            IsRecruiting BOOLEAN,
            IsRoleplay BOOLEAN,
            PrimaryFocus VARCHAR(20),
            SecondaryFocus VARCHAR(20),
            CommitmentLevel VARCHAR(20),
            PRIMARY KEY (SID)
        )
        """)

    mycursor.execute("""
        CREATE TABLE IF NOT EXISTS orgmembers (
            MID INT NOT NULL AUTO_INCREMENT UNIQUE,
            UID INT NOT NULL,
            SID VARCHAR(25) NOT NULL,
            IsPrimary BOOLEAN,
            MemberRank VARCHAR(30) NOT NULL,
            Stars TINYINT NOT NULL,
            PRIMARY KEY (SID, UID),
            FOREIGN KEY (SID) REFERENCES orgs(SID)
        )
        """)
