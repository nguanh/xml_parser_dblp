INSERT_LOCAL_URL = "INSERT INTO local_url(url,global_url_id) VALUES (%s, %s)"
CHECK_LOCAL_URL = "SELECT id FROM local_url WHERE url = %s AND global_url_id = %s"

INSERT_CLUSTER = "INSERT INTO cluster(cluster_name) VALUES (%s)"
CHECK_CLUSTER = "SELECT id FROM cluster WHERE cluster_name = %s"
