curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/ -d '{
        "name": "postgres_sink02",
        "config": {
                "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
                "connection.user":"chetna",
                "connection.password":"d0nt@sk",
                "key.converter": "org.apache.kafka.connect.storage.StringConverter",
                "key.converter.schema.registry.url": "http://schema-registry:8081",
                "value.converter": "io.confluent.connect.avro.AvroConverter",
                "value.converter.schema.registry.url": "http://schema-registry:8081",
                "connection.url": "jdbc:postgresql://localhost:5432/etl",
                "topics": "sample-etl.orders",
                "table.name.format": "etl.orders",
                "pk.mode": "none",
                "insert.mode": "insert",
                "auto.create": "true"
        }
}'

curl -i -X GET -H "Accept:application/json" -H "Content-Type:application/json" localhost:8083/connectors/postgres_sink