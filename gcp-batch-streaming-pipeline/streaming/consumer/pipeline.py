import json
from dataclasses import asdict

import apache_beam as beam
from apache_beam.io.gcp.bigquery import WriteToBigQuery
from apache_beam.io.gcp.pubsub import ReadFromPubSub
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
from streaming.bq_schema import CURATED_SCHEMA, QUARANTINE_SCHEMA
from streaming.config import (
    BG_TABLE_STREAMING_CURATED,
    BG_TABLE_STREAMING_QUARANTINE,
    BQ_DATASET_STREAMING,
    PROJECT_ID,
    SUBSCRIPTION_PATH,
)
from streaming.consumer.log import LogEvent
from streaming.consumer.transformer import TaxiTransformer
from streaming.consumer.validator import EventValidator
from streaming.consumer.zone_lookup import TaxiZoneLookup


def decode_message(message: bytes):
    return json.loads(message.decode("utf-8"))

def run():
    options = PipelineOptions()
    standard_opt = options.view_as(StandardOptions)
    standard_opt.runner = "DirectRunner"
    standard_opt.streaming = True
    
    zone_lookup = TaxiZoneLookup()
    transformer = TaxiTransformer(zone_lookup)
    validator = EventValidator()
    
    with beam.Pipeline(options=standard_opt) as pipeline:
        messages = (
            pipeline
            
            | "Read From PubSub"
            >> ReadFromPubSub(subscription=SUBSCRIPTION_PATH)
            
            | "Decode Json"
            >> beam.Map(decode_message)
        )
        
        transformed = (
            messages
            
            | "Transform Event"
            >> beam.Map(transformer.transform)
        )
        
        validated = (
            transformed
            
            | "Validate Event"
            >> beam.Map(validator.validate)
        )
        
        curated, quarantine = (
            validated
            
            | "Partition Event"
            >> beam.Partition(validator.partition, 2)
        )
        
        (
            curated
            
            | "Curated To Dict"
            >> beam.Map(lambda x: asdict(x["trip"]))

            | "Print Event Curated"
            >> beam.ParDo(LogEvent("CURATED"))
        
            | "Write curated to Big Query"
            >> WriteToBigQuery(
                table=BG_TABLE_STREAMING_CURATED,
                dataset=BQ_DATASET_STREAMING,
                project=PROJECT_ID,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                schema=CURATED_SCHEMA,
                method=WriteToBigQuery.Method.STREAMING_INSERTS,
            )
        )
        
        (
            quarantine
            
            | "Quarantine to Dict"
            >> beam.Map(
                lambda x: {
                    **asdict(x["trip"]),
                    "issue_description": x["issue_description"]
                }
            )
            
            | "Print Event Quarantine"
            >> beam.ParDo(LogEvent("QUARANTINE"))
        
            | "Write quarantine to Big Query"
            >> WriteToBigQuery(
                table=BG_TABLE_STREAMING_QUARANTINE,
                dataset=BQ_DATASET_STREAMING,
                project=PROJECT_ID,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                schema=QUARANTINE_SCHEMA,
                method=WriteToBigQuery.Method.STREAMING_INSERTS,
            )
        )
        
if __name__ == "__main__":
    run()