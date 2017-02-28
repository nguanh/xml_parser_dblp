IMPORT_CSV=("LOAD DATA INFILE '{}' INTO TABLE {} "
            "FIELDS TERMINATED BY ',' ENCLOSED BY \" "
            "LINES TERMINATED BY '\\n' "
            "IGNORE 1 LINES;")
