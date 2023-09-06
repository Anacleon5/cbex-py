from datetime import timedelta
import time

# needed for any cluster connection
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster

# needed for options -- cluster, timeout, SQL++ (N1QL) query, etc.
from couchbase.options import ClusterOptions
from couchbase.diagnostics import ServiceType
from couchbase.options import WaitUntilReadyOptions
import couchbase.subdocument as SD

# Connect options - authentication
auth = PasswordAuthenticator(
    "Administrator",
    "password",
)
# Get a reference to our cluster
# NOTE: For TLS/SSL connection use 'couchbases://<your-ip-address>' instead
cluster = Cluster(f"couchbase://localhost", ClusterOptions(auth))

# Wait until the cluster is ready for use.
cluster.wait_until_ready(timedelta(seconds=3),
         WaitUntilReadyOptions(service_types=[ServiceType.KeyValue, ServiceType.Query]))

bucket_name = "cbex"

call_time = time.time()

def test():
    results = cluster.query(
        f"SELECT symbol,price,starting_price FROM {bucket_name} WHERE symbol IS NOT MISSING AND price IS NOT MISSING",
    )
    print(results)
    for row in results.rows():
        print(row)

    LATEST_TS = 0
    results2 = cluster.query(
        f"SELECT * FROM {bucket_name} WHERE type='order' and ts > {LATEST_TS} ORDER BY ts ASC LIMIT 50;",
    )
    print(results2)
    for row2 in results2.rows():
        print(row2)

    cluster.bucket(bucket_name).default_collection().mutate_in(
                'stock:AAL', [SD.replace("price", 56.07)]
            )
test()